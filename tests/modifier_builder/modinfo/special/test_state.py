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


import logging

from eos.const.eos import EffectBuildStatus, State
from eos.const.eve import EffectCategory
from tests.modifier_builder.modbuilder_testcase import ModBuilderTestCase


class TestBuilderModinfoState(ModBuilderTestCase):
    """Test parsing of YAML describing modifiers applied at different states"""

    def make_effect(self, effect_category):
        self.effect_row = {
            'effect_category': effect_category,
            'modifier_info': (
                '- domain: shipID\n  func: ItemModifier\n  modifiedAttributeID: 22\n'
                '  modifyingAttributeID: 11\n  operator: 6\n'
            )
        }

    def test_passive(self):
        self.make_effect(EffectCategory.passive)
        modifiers, status = self.run_builder(self.effect_row)
        self.assertEqual(status, EffectBuildStatus.success)
        self.assertEqual(len(modifiers), 1)
        modifier = modifiers[0]
        self.assertEqual(modifier.state, State.offline)
        self.assertEqual(len(self.log), 0)

    def test_active(self):
        self.make_effect(EffectCategory.active)
        modifiers, status = self.run_builder(self.effect_row)
        self.assertEqual(status, EffectBuildStatus.success)
        self.assertEqual(len(modifiers), 1)
        modifier = modifiers[0]
        self.assertEqual(modifier.state, State.active)
        self.assertEqual(len(self.log), 0)

    def test_target(self):
        self.make_effect(EffectCategory.target)
        modifiers, status = self.run_builder(self.effect_row)
        self.assertEqual(status, EffectBuildStatus.success)
        self.assertEqual(len(modifiers), 1)
        modifier = modifiers[0]
        self.assertEqual(modifier.state, State.active)
        self.assertEqual(len(self.log), 0)

    def test_area(self):
        self.make_effect(EffectCategory.area)
        modifiers, status = self.run_builder(self.effect_row)
        self.assertEqual(status, EffectBuildStatus.error)
        self.assertEqual(len(modifiers), 0)
        log_record = self.log[0]
        self.assertEqual(log_record.name, 'eos.data.cache_generator.modifier_builder.builder')
        self.assertEqual(log_record.levelno, logging.ERROR)
        expected = 'failed to build 1/1 modifiers of effect 1'
        self.assertEqual(log_record.msg, expected)

    def test_online(self):
        self.make_effect(EffectCategory.online)
        modifiers, status = self.run_builder(self.effect_row)
        self.assertEqual(status, EffectBuildStatus.success)
        self.assertEqual(len(modifiers), 1)
        modifier = modifiers[0]
        self.assertEqual(modifier.state, State.online)
        self.assertEqual(len(self.log), 0)

    def test_overload(self):
        self.make_effect(EffectCategory.overload)
        modifiers, status = self.run_builder(self.effect_row)
        self.assertEqual(status, EffectBuildStatus.success)
        self.assertEqual(len(modifiers), 1)
        modifier = modifiers[0]
        self.assertEqual(modifier.state, State.overload)
        self.assertEqual(len(self.log), 0)

    def test_dungeon(self):
        self.make_effect(EffectCategory.dungeon)
        modifiers, status = self.run_builder(self.effect_row)
        self.assertEqual(status, EffectBuildStatus.error)
        self.assertEqual(len(modifiers), 0)
        log_record = self.log[0]
        self.assertEqual(log_record.name, 'eos.data.cache_generator.modifier_builder.builder')
        self.assertEqual(log_record.levelno, logging.ERROR)
        expected = 'failed to build 1/1 modifiers of effect 1'
        self.assertEqual(log_record.msg, expected)

    def test_system(self):
        self.make_effect(EffectCategory.system)
        modifiers, status = self.run_builder(self.effect_row)
        self.assertEqual(status, EffectBuildStatus.success)
        self.assertEqual(len(modifiers), 1)
        modifier = modifiers[0]
        self.assertEqual(modifier.state, State.offline)
        self.assertEqual(len(self.log), 0)
