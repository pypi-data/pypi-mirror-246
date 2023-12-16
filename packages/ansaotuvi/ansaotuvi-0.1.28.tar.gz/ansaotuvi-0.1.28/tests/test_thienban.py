from __future__ import absolute_import

import unittest

import pytest

from ansaotuvi.App import lapDiaBan
from ansaotuvi.DiaBan import diaBan
from ansaotuvi.ThienBan import lapThienBan


@pytest.mark.thienban
class TestThienBan(unittest.TestCase):
    def test_thienban_initializable(self):
        diaban = lapDiaBan(diaBan, nn=24, tt=10, nnnn=1991, gioSinh=7, gioiTinh=1, duongLich=1, timeZone=7)
        thienban = lapThienBan(24, 10, 1991, 7, 1, 'asdf', diaban)
