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


from collections import namedtuple

from eos.const.eos import Restriction
from eos.fit.item import Booster
from .base import BaseRestrictionRegister
from ..exception import RegisterValidationError


BoosterEffectErrorData = namedtuple('BoosterEffectErrorData', ('illegally_disabled', 'disablable'))


class BoosterEffectRestrictionRegister(BaseRestrictionRegister):
    """
    Implements restriction:
    Booster must have all of its non-side-effects enabled.

    If booster item has some side-effect disabled, it may become
    disabled regular effect when fit source is switched. Regular
    effects are hidden from booster side-effect API. Such effects
    are raised as an issue by this register.

    Details:
    Uses set of actually disabled effects during validation,
    rather than set of IDs of effects which are not allowed
    to be active on the booster (see __disabled_effects vs
    _disabled_effects comments on BaseItemMixin class).
    """

    def __init__(self):
        self.__boosters = set()

    def register_item(self, item):
        if isinstance(item, Booster):
            self.__boosters.add(item)

    def unregister_item(self, item):
        self.__boosters.discard(item)

    def validate(self):
        tainted_items = {}
        for booster in self.__boosters:
            # Check if any disabled effects cannot be found in
            # side-effect list
            disablable = set(booster.side_effects)
            illegal = booster._disabled_effects.difference(disablable)
            if len(illegal) == 0:
                continue
            tainted_items[booster] = BoosterEffectErrorData(
                illegally_disabled=illegal,
                disablable=disablable
            )
        if tainted_items:
            raise RegisterValidationError(tainted_items)

    @property
    def restriction_type(self):
        return Restriction.booster_effect
