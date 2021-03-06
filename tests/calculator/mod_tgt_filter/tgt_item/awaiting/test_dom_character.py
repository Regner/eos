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


from eos.const.eos import State, ModifierTargetFilter, ModifierDomain, ModifierOperator
from eos.const.eve import EffectCategory
from eos.data.cache_object.modifier import DogmaModifier
from tests.calculator.calculator_testcase import CalculatorTestCase
from tests.calculator.environment import IndependentItem


class TestTgtItemAwaitingDomainChar(CalculatorTestCase):

    def test_character(self):
        tgt_attr = self.ch.attribute(attribute_id=1)
        src_attr = self.ch.attribute(attribute_id=2)
        modifier = DogmaModifier()
        modifier.state = State.offline
        modifier.tgt_filter = ModifierTargetFilter.item
        modifier.tgt_domain = ModifierDomain.character
        modifier.tgt_attr = tgt_attr.id
        modifier.operator = ModifierOperator.post_percent
        modifier.src_attr = src_attr.id
        effect = self.ch.effect(effect_id=1, category=EffectCategory.passive)
        effect.modifiers = (modifier,)
        influence_source = IndependentItem(self.ch.type(
            type_id=1, effects=(effect,), attributes={src_attr.id: 20}
        ))
        self.fit.items.add(influence_source)
        influence_target = IndependentItem(self.ch.type(
            type_id=2, attributes={tgt_attr.id: 100}
        ))
        # Action
        # Here we add influence target after adding source, to make sure
        # modifiers wait for target to appear, and then are applied onto it
        self.fit.character = influence_target
        # Verification
        self.assertAlmostEqual(influence_target.attributes[tgt_attr.id], 120)
        # Cleanup
        self.fit.character = None
        self.fit.items.remove(influence_source)
        self.assertEqual(len(self.log), 0)
        self.assert_calculator_buffers_empty(self.fit)
