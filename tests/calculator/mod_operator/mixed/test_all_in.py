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
from tests.calculator.environment import IndependentItem, ShipDomainItem


class TestOperatorAllIn(CalculatorTestCase):
    """Test interaction of all operators, besides post-assignment"""

    def test_all_in(self):
        tgt_attr = self.ch.attribute(attribute_id=1, stackable=0)
        src_attr = self.ch.attribute(attribute_id=2)
        modifier_pre_ass = DogmaModifier()
        modifier_pre_ass.state = State.offline
        modifier_pre_ass.tgt_filter = ModifierTargetFilter.domain
        modifier_pre_ass.tgt_domain = ModifierDomain.ship
        modifier_pre_ass.tgt_attr = tgt_attr.id
        modifier_pre_ass.operator = ModifierOperator.pre_assign
        modifier_pre_ass.src_attr = src_attr.id
        effect_pre_ass = self.ch.effect(effect_id=1, category=EffectCategory.passive)
        effect_pre_ass.modifiers = (modifier_pre_ass,)
        value_pre_ass = 5
        influence_source_pre_ass = IndependentItem(self.ch.type(
            type_id=1, effects=(effect_pre_ass,),
            attributes={src_attr.id: value_pre_ass}
        ))
        self.fit.items.add(influence_source_pre_ass)
        modifier_pre_mul = DogmaModifier()
        modifier_pre_mul.state = State.offline
        modifier_pre_mul.tgt_filter = ModifierTargetFilter.domain
        modifier_pre_mul.tgt_domain = ModifierDomain.ship
        modifier_pre_mul.tgt_attr = tgt_attr.id
        modifier_pre_mul.operator = ModifierOperator.pre_mul
        modifier_pre_mul.src_attr = src_attr.id
        effect_pre_mul = self.ch.effect(effect_id=2, category=EffectCategory.passive)
        effect_pre_mul.modifiers = (modifier_pre_mul,)
        value_pre_mul = 50
        influence_source_pre_mul = IndependentItem(self.ch.type(
            type_id=2, effects=(effect_pre_mul,),
            attributes={src_attr.id: value_pre_mul}
        ))
        self.fit.items.add(influence_source_pre_mul)
        modifier_pre_div = DogmaModifier()
        modifier_pre_div.state = State.offline
        modifier_pre_div.tgt_filter = ModifierTargetFilter.domain
        modifier_pre_div.tgt_domain = ModifierDomain.ship
        modifier_pre_div.tgt_attr = tgt_attr.id
        modifier_pre_div.operator = ModifierOperator.pre_div
        modifier_pre_div.src_attr = src_attr.id
        effect_pre_div = self.ch.effect(effect_id=3, category=EffectCategory.passive)
        effect_pre_div.modifiers = (modifier_pre_div,)
        value_pre_div = 0.5
        influence_source_pre_div = IndependentItem(self.ch.type(
            type_id=3, effects=(effect_pre_div,),
            attributes={src_attr.id: value_pre_div}
        ))
        self.fit.items.add(influence_source_pre_div)
        modifier_mod_add = DogmaModifier()
        modifier_mod_add.state = State.offline
        modifier_mod_add.tgt_filter = ModifierTargetFilter.domain
        modifier_mod_add.tgt_domain = ModifierDomain.ship
        modifier_mod_add.tgt_attr = tgt_attr.id
        modifier_mod_add.operator = ModifierOperator.mod_add
        modifier_mod_add.src_attr = src_attr.id
        effect_mod_add = self.ch.effect(effect_id=4, category=EffectCategory.passive)
        effect_mod_add.modifiers = (modifier_mod_add,)
        value_mod_add = 10
        influence_source_mod_add = IndependentItem(self.ch.type(
            type_id=4, effects=(effect_mod_add,),
            attributes={src_attr.id: value_mod_add}
        ))
        self.fit.items.add(influence_source_mod_add)
        modifier_mod_sub = DogmaModifier()
        modifier_mod_sub.state = State.offline
        modifier_mod_sub.tgt_filter = ModifierTargetFilter.domain
        modifier_mod_sub.tgt_domain = ModifierDomain.ship
        modifier_mod_sub.tgt_attr = tgt_attr.id
        modifier_mod_sub.operator = ModifierOperator.mod_sub
        modifier_mod_sub.src_attr = src_attr.id
        effect_mod_sub = self.ch.effect(effect_id=5, category=EffectCategory.passive)
        effect_mod_sub.modifiers = (modifier_mod_sub,)
        value_mod_sub = 63
        influence_source_mod_sub = IndependentItem(self.ch.type(
            type_id=5, effects=(effect_mod_sub,),
            attributes={src_attr.id: value_mod_sub}
        ))
        self.fit.items.add(influence_source_mod_sub)
        modifier_post_mul = DogmaModifier()
        modifier_post_mul.state = State.offline
        modifier_post_mul.tgt_filter = ModifierTargetFilter.domain
        modifier_post_mul.tgt_domain = ModifierDomain.ship
        modifier_post_mul.tgt_attr = tgt_attr.id
        modifier_post_mul.operator = ModifierOperator.post_mul
        modifier_post_mul.src_attr = src_attr.id
        effect_post_mul = self.ch.effect(effect_id=6, category=EffectCategory.passive)
        effect_post_mul.modifiers = (modifier_post_mul,)
        value_post_mul = 1.35
        influence_source_post_mul = IndependentItem(self.ch.type(
            type_id=6, effects=(effect_post_mul,),
            attributes={src_attr.id: value_post_mul}
        ))
        self.fit.items.add(influence_source_post_mul)
        modifier_post_div = DogmaModifier()
        modifier_post_div.state = State.offline
        modifier_post_div.tgt_filter = ModifierTargetFilter.domain
        modifier_post_div.tgt_domain = ModifierDomain.ship
        modifier_post_div.tgt_attr = tgt_attr.id
        modifier_post_div.operator = ModifierOperator.post_div
        modifier_post_div.src_attr = src_attr.id
        effect_post_div = self.ch.effect(effect_id=7, category=EffectCategory.passive)
        effect_post_div.modifiers = (modifier_post_div,)
        value_post_div = 2.7
        influence_source_post_div = IndependentItem(self.ch.type(
            type_id=7, effects=(effect_post_div,),
            attributes={src_attr.id: value_post_div}
        ))
        self.fit.items.add(influence_source_post_div)
        modifier_post_perc = DogmaModifier()
        modifier_post_perc.state = State.offline
        modifier_post_perc.tgt_filter = ModifierTargetFilter.domain
        modifier_post_perc.tgt_domain = ModifierDomain.ship
        modifier_post_perc.tgt_attr = tgt_attr.id
        modifier_post_perc.operator = ModifierOperator.post_percent
        modifier_post_perc.src_attr = src_attr.id
        effect_post_perc = self.ch.effect(effect_id=8, category=EffectCategory.passive)
        effect_post_perc.modifiers = (modifier_post_perc,)
        value_post_perc = 15
        influence_source_post_perc = IndependentItem(self.ch.type(
            type_id=8, effects=(effect_post_perc,),
            attributes={src_attr.id: value_post_perc}
        ))
        self.fit.items.add(influence_source_post_perc)
        influence_target = ShipDomainItem(self.ch.type(type_id=9, attributes={tgt_attr.id: 100}))
        # Action
        self.fit.items.add(influence_target)
        # Verification
        # Operators shouldn't be penalized and should go in this order
        exp_value = (
            ((value_pre_ass * value_pre_mul / value_pre_div) + value_mod_add - value_mod_sub) *
            value_post_mul / value_post_div * (1 + value_post_perc / 100)
        )
        self.assertAlmostEqual(influence_target.attributes[tgt_attr.id], exp_value)
        # Cleanup
        self.fit.items.remove(influence_source_pre_ass)
        self.fit.items.remove(influence_source_pre_mul)
        self.fit.items.remove(influence_source_pre_div)
        self.fit.items.remove(influence_source_mod_add)
        self.fit.items.remove(influence_source_mod_sub)
        self.fit.items.remove(influence_source_post_mul)
        self.fit.items.remove(influence_source_post_div)
        self.fit.items.remove(influence_source_post_perc)
        self.fit.items.remove(influence_target)
        self.assertEqual(len(self.log), 0)
        self.assert_calculator_buffers_empty(self.fit)
