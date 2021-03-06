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


from unittest.mock import Mock

from eos.fit.item import Ship
from tests.stats.stat_testcase import StatTestCase


class TestResistances(StatTestCase):

    def test_relay(self):
        # Check that stats service relays resistance stats properly
        ship_eve_type = self.ch.type(type_id=1)
        ship_item = self.make_item_mock(Ship, ship_eve_type)
        ship_item.resistances.hull.em = 5
        ship_item.resistances.hull.thermal = 6
        ship_item.resistances.hull.kinetic = 7
        ship_item.resistances.hull.explosive = 8
        ship_item.resistances.armor.em = 15
        ship_item.resistances.armor.thermal = 16
        ship_item.resistances.armor.kinetic = 17
        ship_item.resistances.armor.explosive = 18
        ship_item.resistances.shield.em = 25
        ship_item.resistances.shield.thermal = 26
        ship_item.resistances.shield.kinetic = 27
        ship_item.resistances.shield.explosive = 28
        self.set_ship(ship_item)
        self.assertEqual(self.ss.resistances.hull.em, 5)
        self.assertEqual(self.ss.resistances.hull.thermal, 6)
        self.assertEqual(self.ss.resistances.hull.kinetic, 7)
        self.assertEqual(self.ss.resistances.hull.explosive, 8)
        self.assertEqual(self.ss.resistances.armor.em, 15)
        self.assertEqual(self.ss.resistances.armor.thermal, 16)
        self.assertEqual(self.ss.resistances.armor.kinetic, 17)
        self.assertEqual(self.ss.resistances.armor.explosive, 18)
        self.assertEqual(self.ss.resistances.shield.em, 25)
        self.assertEqual(self.ss.resistances.shield.thermal, 26)
        self.assertEqual(self.ss.resistances.shield.kinetic, 27)
        self.assertEqual(self.ss.resistances.shield.explosive, 28)
        self.set_ship(None)
        self.assertEqual(len(self.log), 0)
        self.assert_stat_buffers_empty()

    def test_no_ship(self):
        # Check that something sane is returned in case of no ship
        self.assertIsNone(self.ss.resistances.hull.em)
        self.assertIsNone(self.ss.resistances.hull.thermal)
        self.assertIsNone(self.ss.resistances.hull.kinetic)
        self.assertIsNone(self.ss.resistances.hull.explosive)
        self.assertIsNone(self.ss.resistances.armor.em)
        self.assertIsNone(self.ss.resistances.armor.thermal)
        self.assertIsNone(self.ss.resistances.armor.kinetic)
        self.assertIsNone(self.ss.resistances.armor.explosive)
        self.assertIsNone(self.ss.resistances.shield.em)
        self.assertIsNone(self.ss.resistances.shield.thermal)
        self.assertIsNone(self.ss.resistances.shield.kinetic)
        self.assertIsNone(self.ss.resistances.shield.explosive)
        self.assertEqual(len(self.log), 0)
        self.assert_stat_buffers_empty()

    def test_cache(self):
        ship_eve_type = self.ch.type(type_id=1)
        ship_item = self.make_item_mock(Ship, ship_eve_type)
        self.set_ship(ship_item)
        hull = Mock(em=5, thermal=6, kinetic=7, explosive=8)
        armor = Mock(em=15, thermal=16, kinetic=17, explosive=18)
        shield = Mock(em=25, thermal=26, kinetic=27, explosive=28)
        ship_item.resistances = Mock(hull=hull, armor=armor, shield=shield)
        self.assertEqual(self.ss.resistances.hull.em, 5)
        self.assertEqual(self.ss.resistances.hull.thermal, 6)
        self.assertEqual(self.ss.resistances.hull.kinetic, 7)
        self.assertEqual(self.ss.resistances.hull.explosive, 8)
        self.assertEqual(self.ss.resistances.armor.em, 15)
        self.assertEqual(self.ss.resistances.armor.thermal, 16)
        self.assertEqual(self.ss.resistances.armor.kinetic, 17)
        self.assertEqual(self.ss.resistances.armor.explosive, 18)
        self.assertEqual(self.ss.resistances.shield.em, 25)
        self.assertEqual(self.ss.resistances.shield.thermal, 26)
        self.assertEqual(self.ss.resistances.shield.kinetic, 27)
        self.assertEqual(self.ss.resistances.shield.explosive, 28)
        hull = Mock(em=15, thermal=16, kinetic=17, explosive=18)
        armor = Mock(em=25, thermal=26, kinetic=27, explosive=28)
        shield = Mock(em=35, thermal=36, kinetic=37, explosive=38)
        ship_item.resistances = Mock(hull=hull, armor=armor, shield=shield)
        self.assertEqual(self.ss.resistances.hull.em, 5)
        self.assertEqual(self.ss.resistances.hull.thermal, 6)
        self.assertEqual(self.ss.resistances.hull.kinetic, 7)
        self.assertEqual(self.ss.resistances.hull.explosive, 8)
        self.assertEqual(self.ss.resistances.armor.em, 15)
        self.assertEqual(self.ss.resistances.armor.thermal, 16)
        self.assertEqual(self.ss.resistances.armor.kinetic, 17)
        self.assertEqual(self.ss.resistances.armor.explosive, 18)
        self.assertEqual(self.ss.resistances.shield.em, 25)
        self.assertEqual(self.ss.resistances.shield.thermal, 26)
        self.assertEqual(self.ss.resistances.shield.kinetic, 27)
        self.assertEqual(self.ss.resistances.shield.explosive, 28)
        self.set_ship(None)
        self.assertEqual(len(self.log), 0)
        self.assert_stat_buffers_empty()

    def test_volatility(self):
        ship_eve_type = self.ch.type(type_id=1)
        ship_item = self.make_item_mock(Ship, ship_eve_type)
        self.set_ship(ship_item)
        hull = Mock(em=5, thermal=6, kinetic=7, explosive=8)
        armor = Mock(em=15, thermal=16, kinetic=17, explosive=18)
        shield = Mock(em=25, thermal=26, kinetic=27, explosive=28)
        ship_item.resistances = Mock(hull=hull, armor=armor, shield=shield)
        self.assertEqual(self.ss.resistances.hull.em, 5)
        self.assertEqual(self.ss.resistances.hull.thermal, 6)
        self.assertEqual(self.ss.resistances.hull.kinetic, 7)
        self.assertEqual(self.ss.resistances.hull.explosive, 8)
        self.assertEqual(self.ss.resistances.armor.em, 15)
        self.assertEqual(self.ss.resistances.armor.thermal, 16)
        self.assertEqual(self.ss.resistances.armor.kinetic, 17)
        self.assertEqual(self.ss.resistances.armor.explosive, 18)
        self.assertEqual(self.ss.resistances.shield.em, 25)
        self.assertEqual(self.ss.resistances.shield.thermal, 26)
        self.assertEqual(self.ss.resistances.shield.kinetic, 27)
        self.assertEqual(self.ss.resistances.shield.explosive, 28)
        hull = Mock(em=15, thermal=16, kinetic=17, explosive=18)
        armor = Mock(em=25, thermal=26, kinetic=27, explosive=28)
        shield = Mock(em=35, thermal=36, kinetic=37, explosive=38)
        ship_item.resistances = Mock(hull=hull, armor=armor, shield=shield)
        self.ss._clear_volatile_attrs()
        self.assertEqual(self.ss.resistances.hull.em, 15)
        self.assertEqual(self.ss.resistances.hull.thermal, 16)
        self.assertEqual(self.ss.resistances.hull.kinetic, 17)
        self.assertEqual(self.ss.resistances.hull.explosive, 18)
        self.assertEqual(self.ss.resistances.armor.em, 25)
        self.assertEqual(self.ss.resistances.armor.thermal, 26)
        self.assertEqual(self.ss.resistances.armor.kinetic, 27)
        self.assertEqual(self.ss.resistances.armor.explosive, 28)
        self.assertEqual(self.ss.resistances.shield.em, 35)
        self.assertEqual(self.ss.resistances.shield.thermal, 36)
        self.assertEqual(self.ss.resistances.shield.kinetic, 37)
        self.assertEqual(self.ss.resistances.shield.explosive, 38)
        self.set_ship(None)
        self.assertEqual(len(self.log), 0)
        self.assert_stat_buffers_empty()
