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


from eos import eos as eos_module
from eos.const.eos import State
from eos.const.eve import Type
from eos.util.volatile_cache import VolatileMixin
from .attribute_calculator import LinkTracker
from .exception import HolderAlreadyAssignedError, HolderFitMismatchError
from .holder.container import HolderList, HolderRestrictedSet, HolderSet, ModuleRacks
from .holder.item import *
from .restriction_tracker import RestrictionTracker
from .stat_tracker import StatTracker


class Fit:
    """
    Fit holds all fit items and facilities to calculate their attributes.

    Keyword arguments:
    eos -- eos instance within which fit will operate. If not specified,
    eos.default_instance is used.
    """

    def __init__(self, eos=None):
        # Eos instance within which this fit exists; use default
        # if not specified explicitly
        if eos is None:
            self.__eos = eos_module.default_instance
        else:
            self.__eos = eos
        # Attributes to store holders directly assigned to fit
        self._ship = None
        self._character = None
        self._effect_beacon = None
        # Character-related holder containers
        self.skills = HolderRestrictedSet(self, Skill)
        self.implants = HolderSet(self, Implant)
        self.boosters = HolderSet(self, Booster)
        # Ship-related containers
        self.subsystems = HolderSet(self, Subsystem)
        self.modules = ModuleRacks(high=HolderList(self, Module),
                                   med=HolderList(self, Module),
                                   low=HolderList(self, Module))
        self.rigs = HolderList(self, Rig)
        self.drones = HolderSet(self, Drone)
        # Service containers
        self._holders = set()
        self._volatile_holders = set()
        # Initialize services
        self._link_tracker = LinkTracker(self)  # Tracks links between holders assigned to fit
        self._restriction_tracker = RestrictionTracker(self)  # Tracks various restrictions related to given fitting
        self.stats = StatTracker(self)  # Access point for all the fitting stats
        # As character object shouldn't change in any sane
        # cases, initialize it here
        self.character = Character(Type.character_static)

    def validate(self, skip_checks=()):
        """
        Run fit validation.

        Keyword arguments:
        skip_checks -- iterable with checks to be skipped

        Possible exceptions:
        ValidationError -- raised when validation fails
        """
        self._restriction_tracker.validate(skip_checks)

    def _clear_volatile_data(self):
        """
        Clear all the 'cached', but volatile stats, which should
        be no longer actual on any fit/holder changes.
        """
        self.stats._clear_volatile_attrs()
        for holder in self._volatile_holders:
            holder._clear_volatile_attrs()

    def _add_holder(self, holder):
        """Handle adding of holder to fit."""
        # Make sure the holder isn't used already
        if holder._fit is not None:
            raise HolderAlreadyAssignedError(holder)
        self._clear_volatile_data()
        holder._fit = self
        self._holders.add(holder)
        if isinstance(holder, VolatileMixin):
            self._volatile_holders.add(holder)
        if self.eos is not None:
            self._enable_services(holder)
        # If holder has charge, register it too
        charge = getattr(holder, 'charge', None)
        if charge is not None:
            self._add_holder(charge)

    def _remove_holder(self, holder):
        """Handle removal of holder from fit."""
        # Check that removed holder belongs to fit
        # it's removed from
        if holder._fit is not self:
            raise HolderFitMismatchError(holder)
        # Start from
        self._clear_volatile_data()
        # If there's charge in target holder, unset it before
        # removing holder itself
        charge = getattr(holder, 'charge', None)
        if charge is not None:
            self._remove_holder(charge)
        if self.eos is not None:
            self._disable_services(holder)
        self._holders.remove(holder)
        self._volatile_holders.discard(holder)
        holder._fit = None

    def _enable_services(self, holder):
        """
        Make all of the fit services aware of passed holder.
        Should be called when fit has valid Eos instance,
        as services cannot work without it.
        """
        self._link_tracker.add_holder(holder)
        # Switch states upwards up to holder's state
        enabled_states = set(filter(lambda s: s <= holder.state, State))
        if len(enabled_states) > 0:
            self._link_tracker.enable_states(holder, enabled_states)
            self._restriction_tracker.enable_states(holder, enabled_states)
            self.stats._enable_states(holder, enabled_states)

    def _disable_services(self, holder):
        """Remove holder from all Eos-relying services."""
        # Switch states downwards from current holder's state
        disabled_states = set(filter(lambda s: s <= holder.state, State))
        if len(disabled_states) > 0:
            self.stats._disable_states(holder, disabled_states)
            self._restriction_tracker.disable_states(holder, disabled_states)
            self._link_tracker.disable_states(holder, disabled_states)
        self._link_tracker.remove_holder(holder)

    def _holder_state_switch(self, holder, new_state):
        """
        Handle fit-specific part of holder state switch.

        Positional arguments:
        holder -- holder, for which state should be switched
        new_state -- state, which holder should take
        """
        # At the moment only Eos-dependent services are affected
        # by state switch, thus we have nothing to do if fit
        # doesn't have Eos assigned
        if self.eos is None:
            return
        # Get states which are passed during enabling/disabling
        # into single set (other should stay empty)
        enabled_states = set(filter(lambda s: holder.state < s <= new_state, State))
        disabled_states = set(filter(lambda s: new_state < s <= holder.state, State))
        # Ask trackers to perform corresponding actions
        if len(enabled_states) > 0:
            self._link_tracker.enable_states(holder, enabled_states)
            self._restriction_tracker.enable_states(holder, enabled_states)
            self.stats._enable_states(holder, enabled_states)
        elif len(disabled_states) > 0:
            self._link_tracker.disable_states(holder, disabled_states)
            self._restriction_tracker.disable_states(holder, disabled_states)
            self.stats._disable_states(holder, disabled_states)

    @property
    def character(self):
        return self._character

    @character.setter
    def character(self, new_character):
        self.__set_single_holder('_character', new_character, Character)

    @property
    def ship(self):
        return self._ship

    @ship.setter
    def ship(self, new_ship):
        self.__set_single_holder('_ship', new_ship, Ship)

    @property
    def effect_beacon(self):
        return self._effect_beacon

    @effect_beacon.setter
    def effect_beacon(self, new_effect_beacon):
        self.__set_single_holder('_effect_beacon', new_effect_beacon, EffectBeacon)

    def __set_single_holder(self, attr_name, new_holder, expected_class):
        """
        Handle setting of holder as fit's attribute,
        including removal of old holder assigned to it.

        Possible exceptions:
        TypeError -- raised when holder to be set is not
        holder of expected class and is not None
        ValueError -- raised when holder cannot be used
        (e.g. already belongs to some fit)
        """
        if new_holder is not None and not isinstance(new_holder, expected_class):
            msg = 'only {} and None are accepted, not {}'.format(
                expected_class, type(new_holder))
            raise TypeError(msg)
        old_holder = getattr(self, attr_name)
        if old_holder is not None:
            self._remove_holder(old_holder)
        setattr(self, attr_name, new_holder)
        if new_holder is not None:
            try:
                self._add_holder(new_holder)
            except HolderAlreadyAssignedError as e:
                setattr(self, attr_name, old_holder)
                if old_holder is not None:
                    self._add_holder(old_holder)
                raise ValueError(*e.args) from e

    @property
    def eos(self):
        return self.__eos

    @eos.setter
    def eos(self, new_eos):
        self._clear_volatile_data()
        # Disable everything dependent on old eos prior to switch
        if self.__eos is not None:
            for holder in self._holders:
                self._disable_services(holder)
        # Reassign new eos and feed new data to all holders
        self.__eos = new_eos
        for holder in self._holders:
            holder._refresh_context()
        # Enable eos-dependent services for new instance
        if new_eos is not None:
            for holder in self._holders:
                self._enable_services(holder)