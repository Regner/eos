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
from eos.const.eve import Attribute
from .base import BaseRestrictionRegister
from ..exception import RegisterValidationError


RigSizeErrorData = namedtuple('RigSizeErrorData', ('item_size', 'allowed_size'))


class RigSizeRestrictionRegister(BaseRestrictionRegister):
    """
    Implements restriction:
    If ship requires rigs of certain size, rigs of other size cannot
    be used.

    Details:
    For validation, rig_size attribute value of eve type is taken.
    """

    def __init__(self, fit):
        self._fit = fit
        # Container for items which have rig size restriction
        self.__restricted_items = set()

    def register_item(self, item):
        # Register only items which have attribute,
        # which restricts rig size
        if Attribute.rig_size not in item._eve_type.attributes:
            return
        self.__restricted_items.add(item)

    def unregister_item(self, item):
        self.__restricted_items.discard(item)

    def validate(self):
        ship_item = self._fit.ship
        # Do not apply restriction when fit doesn't
        # have ship
        try:
            ship_eve_type = ship_item._eve_type
        except AttributeError:
            return
        # If ship doesn't have restriction attribute,
        # allow all rigs - skip validation
        try:
            allowed_rig_size = ship_eve_type.attributes[Attribute.rig_size]
        except KeyError:
            return
        tainted_items = {}
        for item in self.__restricted_items:
            item_rig_size = item._eve_type.attributes[Attribute.rig_size]
            # If rig size specification on item and ship differs,
            # then item is tainted
            if item_rig_size != allowed_rig_size:
                tainted_items[item] = RigSizeErrorData(
                    item_size=item_rig_size,
                    allowed_size=allowed_rig_size
                )
        if tainted_items:
            raise RegisterValidationError(tainted_items)

    @property
    def restriction_type(self):
        return Restriction.rig_size
