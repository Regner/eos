# ===============================================================================
# Copyright (C) 2011 Diego Duclos
# Copyright (C) 2011-2017 Anton Vorobyov
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
# ===============================================================================


from eos.const.eos import State, ModifierDomain
from eos.const.eve import Attribute
from eos.util.repr import make_repr_str
from .mixin.chargeable import ChargeableMixin
from .mixin.damage_dealer import DamageDealerMixin
from .mixin.misc import DefaultEffectAttribMixin
from .mixin.state import MutableStateMixin


class Module(
    MutableStateMixin, ChargeableMixin,
    DamageDealerMixin, DefaultEffectAttribMixin
):
    def __init__(self, type_id, state=State.offline, charge=None, **kwargs):
        super().__init__(type_id=type_id, state=state, charge=charge, **kwargs)

    @property
    def reactivation_delay(self):
        delay_ms = self.attributes.get(Attribute.module_reactivation_delay)
        if delay_ms is None:
            return None
        return delay_ms / 1000

    # Attribute calculation-related properties
    _parent_modifier_domain = ModifierDomain.ship
    _owner_modifiable = False

    # Auxiliary methods
    def __repr__(self):
        spec = [['type_id', '_type_id'], 'state', 'charge']
        return make_repr_str(self, spec)


class ModuleHigh(Module):
    """
    Ship's module from high slot.

    Required arguments:
    type_id -- ID of eve type which should serve as base
        for this module.

    Optional arguments:
    state -- initial state this module takes, default is
        offline
    charge -- charge object to load into module, default
        is None

    Cooperative methods:
    __init__
    """
    pass


class ModuleMed(Module):
    """
    Ship's module from medium slot.

    Required arguments:
    type_id -- ID of eve type which should serve as base
        for this module.

    Optional arguments:
    state -- initial state this module takes, default is
        offline
    charge -- charge object to load into module, default
        is None

    Cooperative methods:
    __init__
    """
    pass


class ModuleLow(Module):
    """
    Ship's module from low slot.

    Required arguments:
    type_id -- ID of eve type which should serve as base
        for this module.

    Optional arguments:
    state -- initial state this module takes, default is
        offline
    charge -- charge object to load into module, default
        is None

    Cooperative methods:
    __init__
    """
    pass
