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


from eos.const.eos import ModifierOperator
from eos.util.repr import make_repr_str
from .base import BaseModifier
from .exception import ModificationCalculationError


class DogmaModifier(BaseModifier):
    """
    Dogma modifiers are the most typical modifier type. They always
    take attribute value which describes modification strength from
    item which carries modifier - it makes them less flexible, but
    they can be processed efficiently.
    """

    def __init__(
            self, modifier_id=None, state=None, tgt_filter=None, tgt_domain=None,
            tgt_filter_extra_arg=None, tgt_attr=None, operator=None, src_attr=None
    ):
        BaseModifier.__init__(
            self, state=state, tgt_filter=tgt_filter, tgt_domain=tgt_domain,
            tgt_filter_extra_arg=tgt_filter_extra_arg, tgt_attr=tgt_attr
        )
        self.id = modifier_id
        # Class-specific attributes
        self.operator = operator
        self.src_attr = src_attr

    def get_modification(self, carrier_item, _):
        try:
            mod_value = carrier_item.attributes[self.src_attr]
        # In case attribute value cannot be fetched, just raise error,
        # all error logging is handled in attribute container
        except KeyError as e:
            raise ModificationCalculationError from e
        else:
            return self.operator, mod_value

    # Validation-related methods
    @property
    def _valid(self):
        return all((
            self._validate_base(),
            self.operator in ModifierOperator.__members__.values(),
            isinstance(self.src_attr, int)
        ))

    # Auxiliary methods
    def __repr__(self):
        spec = ['id']
        return make_repr_str(self, spec)
