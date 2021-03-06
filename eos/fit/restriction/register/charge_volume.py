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


ChargeVolumeErrorData = namedtuple('ChargeVolumeErrorData', ('item_volume', 'max_allowed_volume'))


class ChargeVolumeRestrictionRegister(BaseRestrictionRegister):
    """
    Implements restriction:
    Volume of single charge loaded into container should not
    excess its capacity.

    Details:
    Charge volume and container capacity are taken from
        eve type attributes.
    If not specified, volume and/or capacity are assumed
        to be 0.
    """

    def __init__(self):
        self.__containers = set()

    def register_item(self, item):
        # Ignore container items without charge attribute
        if not hasattr(item, 'charge'):
            return
        self.__containers.add(item)

    def unregister_item(self, item):
        self.__containers.discard(item)

    def validate(self):
        tainted_items = {}
        for container in self.__containers:
            charge = container.charge
            if charge is None:
                continue
            # Get volume and capacity with 0 as fallback, and
            # compare them, raising error when charge can't fit
            charge_volume = charge._eve_type.attributes.get(Attribute.volume, 0)
            container_capacity = container._eve_type.attributes.get(Attribute.capacity, 0)
            if charge_volume > container_capacity:
                tainted_items[charge] = ChargeVolumeErrorData(
                    item_volume=charge_volume,
                    max_allowed_volume=container_capacity
                )
        if tainted_items:
            raise RegisterValidationError(tainted_items)

    @property
    def restriction_type(self):
        return Restriction.charge_volume
