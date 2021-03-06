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


from logging import getLogger

from eos.const.eos import EffectBuildStatus, State, ModifierTargetFilter, ModifierDomain, ModifierOperator
from eos.const.eve import Attribute
from eos.data.cache_object import DogmaModifier
from eos.data.cache_object.modifier.custom import PropulsionModuleVelocityBoostModifier


logger = getLogger(__name__)


def add_mwd_modifiers(effect):
    if len(effect.modifiers) > 0:
        msg = 'microwarpdrive effect has modifiers, overwriting them'
        logger.info(msg)
    mass_modifier = DogmaModifier(
        tgt_filter=ModifierTargetFilter.item,
        tgt_domain=ModifierDomain.ship,
        state=State.active,
        src_attr=Attribute.mass_addition,
        operator=ModifierOperator.mod_add,
        tgt_attr=Attribute.mass
    )
    signature_modifier = DogmaModifier(
        tgt_filter=ModifierTargetFilter.item,
        tgt_domain=ModifierDomain.ship,
        state=State.active,
        src_attr=Attribute.signature_radius_bonus,
        operator=ModifierOperator.post_percent,
        tgt_attr=Attribute.signature_radius
    )
    velocity_modifier = PropulsionModuleVelocityBoostModifier()
    effect.modifiers = (mass_modifier, signature_modifier, velocity_modifier)
    effect.build_status = EffectBuildStatus.custom
