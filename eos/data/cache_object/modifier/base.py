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


from abc import ABCMeta, abstractmethod

from eos.const.eos import State, ModifierTargetFilter, ModifierDomain


class BaseModifier(metaclass=ABCMeta):
    """
    Modifiers are part of effects; one modifier describes one
    modification - when it should be applied, on which items,
    how to apply it, and so on.
    """

    def __init__(self, state, tgt_filter, tgt_domain, tgt_filter_extra_arg, tgt_attr):
        self.state = state
        self.tgt_filter = tgt_filter
        self.tgt_domain = tgt_domain
        self.tgt_filter_extra_arg = tgt_filter_extra_arg
        self.tgt_attr = tgt_attr

    @abstractmethod
    def _get_modification(self, carrier_item, fit):
        ...

    # Validation-related methods
    def _validate_base(self):
        validators = {
            ModifierTargetFilter.item: self.__validate_item_modifer,
            ModifierTargetFilter.domain: self.__validate_domain_modifer,
            ModifierTargetFilter.domain_group: self.__validate_domain_group_modifer,
            ModifierTargetFilter.domain_skillrq: self.__validate_domain_skillrq_modifer,
            ModifierTargetFilter.owner_skillrq: self.__validate_owner_skillrq_modifer
        }
        try:
            validator = validators[self.tgt_filter]
        except KeyError:
            return False
        else:
            return validator()

    def __validate_item_modifer(self):
        return all((
            self.__validate_common(),
            self.tgt_domain in (
                ModifierDomain.self, ModifierDomain.character, ModifierDomain.ship,
                ModifierDomain.target, ModifierDomain.other
            ),
            self.tgt_filter_extra_arg is None
        ))

    def __validate_domain_modifer(self):
        return all((
            self.__validate_common(),
            self.tgt_domain in (
                ModifierDomain.self, ModifierDomain.character,
                ModifierDomain.ship, ModifierDomain.target
            ),
            self.tgt_filter_extra_arg is None
        ))

    def __validate_domain_group_modifer(self):
        return all((
            self.__validate_common(),
            self.tgt_domain in (
                ModifierDomain.self, ModifierDomain.character,
                ModifierDomain.ship, ModifierDomain.target
            ),
            # References group via ID
            isinstance(self.tgt_filter_extra_arg, int)
        ))

    def __validate_domain_skillrq_modifer(self):
        return all((
            self.__validate_common(),
            self.tgt_domain in (
                ModifierDomain.self, ModifierDomain.character,
                ModifierDomain.ship, ModifierDomain.target
            ),
            # References skill via ID
            isinstance(self.tgt_filter_extra_arg, int)
        ))

    def __validate_owner_skillrq_modifer(self):
        return all((
            self.__validate_common(),
            self.tgt_domain == ModifierDomain.character,
            # References skill via ID
            isinstance(self.tgt_filter_extra_arg, int)
        ))

    def __validate_common(self):
        return all((
            self.state in State.__members__.values(),
            self.tgt_filter in ModifierTargetFilter.__members__.values(),
            self.tgt_domain in ModifierDomain.__members__.values(),
            isinstance(self.tgt_attr, int)
        ))