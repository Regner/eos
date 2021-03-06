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

from eos.const.eos import EffectBuildStatus
from eos.const.eve import EffectCategory, Operand
from tests.modifier_builder.modbuilder_testcase import ModBuilderTestCase


class TestBuilderEtreeErrorsHandlerFailure(ModBuilderTestCase):

    def setUp(self):
        super().setUp()
        e_tgt = self.ef.make(1, operandID=Operand.def_dom, expressionValue='UnknownDomain')
        e_tgt_attr = self.ef.make(2, operandID=Operand.def_attr, expressionAttributeID=9)
        e_optr = self.ef.make(3, operandID=Operand.def_optr, expressionValue='PostPercent')
        e_src_attr = self.ef.make(4, operandID=Operand.def_attr, expressionAttributeID=327)
        e_tgt_spec = self.ef.make(
            5, operandID=Operand.itm_attr,
            arg1=e_tgt['expressionID'],
            arg2=e_tgt_attr['expressionID']
        )
        e_optr_tgt = self.ef.make(
            6, operandID=Operand.optr_tgt,
            arg1=e_optr['expressionID'],
            arg2=e_tgt_spec['expressionID']
        )
        self.e_add_mod_error = self.ef.make(
            7, operandID=Operand.add_itm_mod,
            arg1=e_optr_tgt['expressionID'],
            arg2=e_src_attr['expressionID']
        )
        self.e_rm_mod_error = self.ef.make(
            8, operandID=Operand.rm_itm_mod,
            arg1=e_optr_tgt['expressionID'],
            arg2=e_src_attr['expressionID']
        )

    def test_single(self):
        effect_row = {
            'pre_expression': self.e_add_mod_error['expressionID'],
            'post_expression': self.e_rm_mod_error['expressionID'],
            'effect_category': EffectCategory.passive
        }
        modifiers, status = self.run_builder(effect_row)
        self.assertEqual(status, EffectBuildStatus.error)
        self.assertEqual(len(modifiers), 0)
        self.assertEqual(len(self.log), 1)
        log_record = self.log[0]
        self.assertEqual(log_record.name, 'eos.data.cache_generator.modifier_builder.builder')
        self.assertEqual(log_record.levelno, logging.ERROR)
        expected = '1 build failure out of 1 modifiers for effect 1'
        self.assertEqual(log_record.msg, expected)

    def test_partial_error_first(self):
        e_tgt = self.ef.make(9, operandID=Operand.def_dom, expressionValue='Ship')
        e_tgt_attr = self.ef.make(10, operandID=Operand.def_attr, expressionAttributeID=9)
        e_optr = self.ef.make(11, operandID=Operand.def_optr, expressionValue='PostPercent')
        e_src_attr = self.ef.make(12, operandID=Operand.def_attr, expressionAttributeID=327)
        e_tgt_spec = self.ef.make(
            13, operandID=Operand.itm_attr,
            arg1=e_tgt['expressionID'],
            arg2=e_tgt_attr['expressionID']
        )
        e_optr_tgt = self.ef.make(
            14, operandID=Operand.optr_tgt,
            arg1=e_optr['expressionID'],
            arg2=e_tgt_spec['expressionID']
        )
        e_add_mod_valid = self.ef.make(
            15, operandID=Operand.add_itm_mod,
            arg1=e_optr_tgt['expressionID'],
            arg2=e_src_attr['expressionID']
        )
        e_rm_mod_valid = self.ef.make(
            16, operandID=Operand.rm_itm_mod,
            arg1=e_optr_tgt['expressionID'],
            arg2=e_src_attr['expressionID']
        )
        e_add_splice = self.ef.make(
            17, operandID=Operand.splice,
            arg1=self.e_add_mod_error['expressionID'],
            arg2=e_add_mod_valid['expressionID']
        )
        e_rm_splice = self.ef.make(
            18, operandID=Operand.splice,
            arg1=self.e_rm_mod_error['expressionID'],
            arg2=e_rm_mod_valid['expressionID']
        )
        effect_row = {
            'pre_expression': e_add_splice['expressionID'],
            'post_expression': e_rm_splice['expressionID'],
            'effect_category': EffectCategory.passive
        }
        modifiers, status = self.run_builder(effect_row)
        self.assertEqual(status, EffectBuildStatus.success_partial)
        self.assertEqual(len(modifiers), 1)
        self.assertEqual(len(self.log), 1)
        log_record = self.log[0]
        self.assertEqual(log_record.name, 'eos.data.cache_generator.modifier_builder.builder')
        self.assertEqual(log_record.levelno, logging.ERROR)
        expected = '1 build failure out of 2 modifiers for effect 1'
        self.assertEqual(log_record.msg, expected)

    def test_partial_error_last(self):
        e_tgt = self.ef.make(9, operandID=Operand.def_dom, expressionValue='Ship')
        e_tgt_attr = self.ef.make(10, operandID=Operand.def_attr, expressionAttributeID=9)
        e_optr = self.ef.make(11, operandID=Operand.def_optr, expressionValue='PostPercent')
        e_src_attr = self.ef.make(12, operandID=Operand.def_attr, expressionAttributeID=327)
        e_tgt_spec = self.ef.make(
            13, operandID=Operand.itm_attr,
            arg1=e_tgt['expressionID'],
            arg2=e_tgt_attr['expressionID']
        )
        e_optr_tgt = self.ef.make(
            14, operandID=Operand.optr_tgt,
            arg1=e_optr['expressionID'],
            arg2=e_tgt_spec['expressionID']
        )
        e_add_mod_valid = self.ef.make(
            15, operandID=Operand.add_itm_mod,
            arg1=e_optr_tgt['expressionID'],
            arg2=e_src_attr['expressionID']
        )
        e_rm_mod_valid = self.ef.make(
            16, operandID=Operand.rm_itm_mod,
            arg1=e_optr_tgt['expressionID'],
            arg2=e_src_attr['expressionID']
        )
        e_add_splice = self.ef.make(
            17, operandID=Operand.splice,
            arg1=e_add_mod_valid['expressionID'],
            arg2=self.e_add_mod_error['expressionID']
        )
        e_rm_splice = self.ef.make(
            18, operandID=Operand.splice,
            arg1=e_rm_mod_valid['expressionID'],
            arg2=self.e_rm_mod_error['expressionID']
        )
        effect_row = {
            'pre_expression': e_add_splice['expressionID'],
            'post_expression': e_rm_splice['expressionID'],
            'effect_category': EffectCategory.passive
        }
        modifiers, status = self.run_builder(effect_row)
        self.assertEqual(status, EffectBuildStatus.success_partial)
        self.assertEqual(len(modifiers), 1)
        self.assertEqual(len(self.log), 1)
        log_record = self.log[0]
        self.assertEqual(log_record.name, 'eos.data.cache_generator.modifier_builder.builder')
        self.assertEqual(log_record.levelno, logging.ERROR)
        expected = '1 build failure out of 2 modifiers for effect 1'
        self.assertEqual(log_record.msg, expected)
