#===============================================================================
# Copyright (C) 2011 Diego Duclos
# Copyright (C) 2011-2013 Anton Vorobyov
#
# This file is part of Eos.
#
# Eos is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Eos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Eos. If not, see <http://www.gnu.org/licenses/>.
#===============================================================================


from eos.const.eve import Attribute
from eos.fit.tuples import Hitpoints, TankingLayers, DamageTypes
from eos.util.override import OverrideDescriptor
from eos.util.volatile_cache import CooperativeVolatileMixin, VolatileProperty
from .holder import HolderBase


class BufferTankingMixin(HolderBase, CooperativeVolatileMixin):
    """
    Mixin intended to use with all entities which are able
    to sustain damage (ships, drones, maybe some charges).

    Cooperative methods:
    __init__
    """

    def __init__(self, **kwargs):
        self.hp = OverridableHp(self)
        super().__init__(**kwargs)

    @VolatileProperty
    def resistances(self):
        """
        Access point to fetch resistances of item. Provides following data:
        .hull.em, .hull.thermal, .hull.kinetic, .hull.explosive,
        .armor.em, .armor.thermal, .armor.kinetic, .armor.explosive,
        .shield.em, .shield.thermal, .shield.kinetic, .shield.explosive
        When resistance data can't be fetched, returns None for requested
        resistance.
        """
        hull = DamageTypes(
            em=self.__get_resistance_by_attr(Attribute.em_damage_resonance),
            thermal=self.__get_resistance_by_attr(Attribute.thermal_damage_resonance),
            kinetic=self.__get_resistance_by_attr(Attribute.kinetic_damage_resonance),
            explosive=self.__get_resistance_by_attr(Attribute.explosive_damage_resonance)
        )
        armor = DamageTypes(
            em=self.__get_resistance_by_attr(Attribute.armor_em_damage_resonance),
            thermal=self.__get_resistance_by_attr(Attribute.armor_thermal_damage_resonance),
            kinetic=self.__get_resistance_by_attr(Attribute.armor_kinetic_damage_resonance),
            explosive=self.__get_resistance_by_attr(Attribute.armor_explosive_damage_resonance)
        )
        shield = DamageTypes(
            em=self.__get_resistance_by_attr(Attribute.shield_em_damage_resonance),
            thermal=self.__get_resistance_by_attr(Attribute.shield_thermal_damage_resonance),
            kinetic=self.__get_resistance_by_attr(Attribute.shield_kinetic_damage_resonance),
            explosive=self.__get_resistance_by_attr(Attribute.shield_explosive_damage_resonance)
        )
        return TankingLayers(hull=hull, armor=armor, shield=shield)

    def __get_resistance_by_attr(self, attribute):
        """
        Get resonance by attribute ID and if there's any
        value, convert it to resistance.
        """
        try:
            resonance = self.attributes[attribute]
        except KeyError:
            return None
        else:
            return 1 - resonance

    def get_ehp(self, damage_profile):
        """
        Get effective HP of item against passed damage profile.

        Required arguments:
        damage_profile -- object which has following numbers as its attibutes:
        em, thermal, kinetic and explosive

        Object with following attributes is returned:
        .hull, .armor, .shield -- number, or None if HP for layer can't be fetched
        .total -- total effective HP, if data for some layer is not available,
        defaults effective hp of this layer to 0.
        """
        hull_ehp = self.__get_layer_ehp(self.hp.hull, self.resistances.hull, damage_profile)
        armor_ehp = self.__get_layer_ehp(self.hp.armor, self.resistances.armor, damage_profile)
        shield_ehp = self.__get_layer_ehp(self.hp.shield, self.resistances.shield, damage_profile)
        total_ehp = (hull_ehp or 0) + (armor_ehp or 0) + (shield_ehp or 0)
        return Hitpoints(hull=hull_ehp, armor=armor_ehp, shield=shield_ehp, total=total_ehp)

    def __get_layer_ehp(self, layer_hp, layer_resistances, damage_profile):
        """
        Calculate layer EHP according to passed data.

        If layer raw HP is None, None is returned
        """
        if not layer_hp:
            return layer_hp
        return layer_hp * self.__get_tanking_efficiency(damage_profile, layer_resistances)

    def __get_tanking_efficiency(self, dmg, res):
        """
        Get tanking efficiency for passed damage/resistance
        profiles.

        If any of layer resistances are not specified,
        they're assumed to be 0.
        """
        dealt = dmg.em + dmg.thermal + dmg.kinetic + dmg.explosive
        absorbed = (dmg.em * (res.em or 0) +
                    dmg.thermal * (res.thermal or 0) +
                    dmg.kinetic * (res.kinetic or 0) +
                    dmg.explosive * (res.explosive or 0))
        received = dealt - absorbed
        return dealt / received

    @VolatileProperty
    def worst_case_ehp(self):
        """
        Get EVE-style effective HP for item.

        EVE takes the worst resistance and calculates EHP against it,
        on a per-layer basis.

        Object with following attributes is returned:
        .hull, .armor, .shield -- number, or None if HP for layer can't be fetched
        .total -- total effective HP, if data for some layer is not available,
        defaults effective hp of this layer to 0.
        """
        hull_ehp = self.__get_layer_worst_case_ehp(self.hp.hull, self.resistances.hull)
        armor_ehp = self.__get_layer_worst_case_ehp(self.hp.armor, self.resistances.armor)
        shield_ehp = self.__get_layer_worst_case_ehp(self.hp.shield, self.resistances.shield)
        total_ehp = (hull_ehp or 0) + (armor_ehp or 0) + (shield_ehp or 0)
        return Hitpoints(hull=hull_ehp, armor=armor_ehp, shield=shield_ehp, total=total_ehp)

    def __get_layer_worst_case_ehp(self, layer_hp, layer_resistances):
        """
        Calculate layer EHP according to passed data.

        If layer raw HP is None, None is returned
        """
        if not layer_hp:
            return layer_hp
        resistance = min(layer_resistances.em or 0,
                         layer_resistances.thermal or 0,
                         layer_resistances.kinetic or 0,
                         layer_resistances.explosive or 0)
        return layer_hp / (1 - resistance)


class OverridableHp:
    """
    Access point to fetch hp of item. Provides following data:

    .hull, .armor, .shield -- number (overridable), or None if data can't
    be fetched
    .hull_max, .armor_max, .shield_max -- number, or None if data can't
    be fetched
    .total -- total amount of HP based on overridable data, if data for
    some layer is not available, defaults hp of this layer to 0
    """

    def __init__(self, holder):
        self.__holder = holder

    @property
    def hull_max(self):
        return self.__holder.attributes.get(Attribute.hp, None)

    @property
    def armor_max(self):
        return self.__holder.attributes.get(Attribute.armor_hp, None)

    @property
    def shield_max(self):
        return self.__holder.attributes.get(Attribute.shield_capacity, None)

    hull = OverrideDescriptor('hull_max', class_check=(int, float))
    armor = OverrideDescriptor('armor_max', class_check=(int, float))
    shield = OverrideDescriptor('shield_max', class_check=(int, float))

    @property
    def total(self):
        return (self.hull or 0) + (self.armor or 0) + (self.shield or 0)

    def _request_volatile_cleanup(self):
        self.__holder._request_volatile_cleanup()
