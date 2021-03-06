# ===============================================================================
# Copyright (C) 2017 Anton Vorobyov
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


import yaml

from eos.const.eos import ModifierTargetFilter, ModifierDomain, ModifierOperator
from eos.data.cache_object import DogmaModifier
from .shared import STATE_CONVERSION_MAP
from ..exception import YamlParsingError


class ModifierInfoConverter:
    """
    Parse modifierInfos into actual Modifier objects.
    """

    def convert(self, effect_row):
        """
        Parse YAML and handle overall workflow and error handling
        flow for modifier info-to-modifier conversion process.
        """
        # Parse modifierInfo field (which is in YAML format)
        modifier_infos_yaml = effect_row['modifier_info']
        try:
            modifier_infos = yaml.safe_load(modifier_infos_yaml)
        except KeyboardInterrupt:
            raise
        # We cannot recover any data in case of YAML parsing
        # failure, thus return empty list
        except Exception as e:
            raise YamlParsingError('failed to parse YAML') from e
        # Go through modifier objects and attempt to convert them one-by-one
        modifiers = []
        build_failures = 0
        # Get handler according to function specified in info
        for modifier_info in modifier_infos:
            try:
                modifier_func = modifier_info['func']
            except (KeyError, TypeError):
                build_failures += 1
                continue
            handler_map = {
                'ItemModifier': self._handle_item_modifier,
                'LocationModifier': self._handle_domain_modifier,
                'LocationGroupModifier': self._handle_domain_group_modifier,
                'LocationRequiredSkillModifier': self._handle_domain_skillrq_modifer,
                'OwnerRequiredSkillModifier': self._handle_owner_skillrq_modifer
            }
            # Compose and verify handler, record if we failed to do so
            try:
                handler = handler_map[modifier_func]
            except KeyError:
                build_failures += 1
            else:
                effect_category = effect_row['effect_category']
                try:
                    modifier = handler(modifier_info, effect_category)
                except KeyboardInterrupt:
                    raise
                except Exception:
                    build_failures += 1
                else:
                    modifiers.append(modifier)
        return modifiers, build_failures

    def _handle_item_modifier(self, modifier_info, effect_category):
        return DogmaModifier(
            state=self._get_state(effect_category),
            tgt_filter=ModifierTargetFilter.item,
            tgt_domain=self._get_domain(modifier_info),
            tgt_attr=int(modifier_info['modifiedAttributeID']),
            operator=self._get_operator(modifier_info),
            src_attr=int(modifier_info['modifyingAttributeID'])
        )

    def _handle_domain_modifier(self, modifier_info, effect_category):
        return DogmaModifier(
            state=self._get_state(effect_category),
            tgt_filter=ModifierTargetFilter.domain,
            tgt_domain=self._get_domain(modifier_info),
            tgt_attr=int(modifier_info['modifiedAttributeID']),
            operator=self._get_operator(modifier_info),
            src_attr=int(modifier_info['modifyingAttributeID'])
        )

    def _handle_domain_group_modifier(self, modifier_info, effect_category):
        return DogmaModifier(
            state=self._get_state(effect_category),
            tgt_filter=ModifierTargetFilter.domain_group,
            tgt_domain=self._get_domain(modifier_info),
            tgt_filter_extra_arg=int(modifier_info['groupID']),
            tgt_attr=int(modifier_info['modifiedAttributeID']),
            operator=self._get_operator(modifier_info),
            src_attr=int(modifier_info['modifyingAttributeID'])
        )

    def _handle_domain_skillrq_modifer(self, modifier_info, effect_category):
        return DogmaModifier(
            state=self._get_state(effect_category),
            tgt_filter=ModifierTargetFilter.domain_skillrq,
            tgt_domain=self._get_domain(modifier_info),
            tgt_filter_extra_arg=int(modifier_info['skillTypeID']),
            tgt_attr=int(modifier_info['modifiedAttributeID']),
            operator=self._get_operator(modifier_info),
            src_attr=int(modifier_info['modifyingAttributeID'])
        )

    def _handle_owner_skillrq_modifer(self, modifier_info, effect_category):
        return DogmaModifier(
            state=self._get_state(effect_category),
            tgt_filter=ModifierTargetFilter.owner_skillrq,
            tgt_domain=self._get_domain(modifier_info),
            tgt_filter_extra_arg=int(modifier_info['skillTypeID']),
            tgt_attr=int(modifier_info['modifiedAttributeID']),
            operator=self._get_operator(modifier_info),
            src_attr=int(modifier_info['modifyingAttributeID'])
        )

    def _get_state(self, effect_category):
        return STATE_CONVERSION_MAP[effect_category]

    def _get_domain(self, modifier_info):
        conversion_map = {
            None: ModifierDomain.self,
            'itemID': ModifierDomain.self,
            'charID': ModifierDomain.character,
            'shipID': ModifierDomain.ship,
            'targetID': ModifierDomain.target,
            'otherID': ModifierDomain.other
        }
        return conversion_map[modifier_info['domain']]

    def _get_operator(self, modifier_info):
        # Format: {CCP operator ID: eos operator ID}
        conversion_map = {
            -1: ModifierOperator.pre_assign,
            0: ModifierOperator.pre_mul,
            1: ModifierOperator.pre_div,
            2: ModifierOperator.mod_add,
            3: ModifierOperator.mod_sub,
            4: ModifierOperator.post_mul,
            5: ModifierOperator.post_div,
            6: ModifierOperator.post_percent,
            7: ModifierOperator.post_assign,
        }
        return conversion_map[modifier_info['operator']]
