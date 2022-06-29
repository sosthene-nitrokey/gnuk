"""
card_test_personalize_admin_less_1.py - test admin-less mode

Copyright (C) 2016, 2018, 2019  g10 Code GmbH
Author: NIIBE Yutaka <gniibe@fsij.org>

This file is a part of Gnuk, a GnuPG USB Token implementation.

Gnuk is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Gnuk is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from struct import pack
from re import match, DOTALL
from util import *
from pubkey_crypto import get_PK_Crypto, get_key
from card_const import *
from constants_for_test import *

class Test_Card_Personalize_Adminless_FIRST(object):
    def test_verify_pw3_0(self, card):
        v = card.verify(3, FACTORY_PASSPHRASE_PW3)
        assert v

    def test_import_key_1(self, card):
        key = get_key(card)
        t = key[0].build_privkey_template(card.is_yubikey)
        r = card.cmd_put_data_odd(0x3f, 0xff, t)
        assert r

    def test_import_key_2(self, card):
        key = get_key(card)
        t = key[1].build_privkey_template(card.is_yubikey)
        r = card.cmd_put_data_odd(0x3f, 0xff, t)
        assert r

    def test_import_key_3(self, card):
        key = get_key(card)
        t = key[2].build_privkey_template(card.is_yubikey)
        r = card.cmd_put_data_odd(0x3f, 0xff, t)
        assert r

    def test_fingerprint_1_put(self, card):
        key = get_key(card)
        fpr1 = key[0].get_fpr()
        r = card.cmd_put_data(0x00, 0xc7, fpr1)
        assert r

    def test_fingerprint_2_put(self, card):
        key = get_key(card)
        fpr2 = key[1].get_fpr()
        r = card.cmd_put_data(0x00, 0xc8, fpr2)
        assert r

    def test_fingerprint_3_put(self, card):
        key = get_key(card)
        fpr3 = key[2].get_fpr()
        r = card.cmd_put_data(0x00, 0xc9, fpr3)
        assert r

    def test_timestamp_1_put(self, card):
        key = get_key(card)
        timestamp1 = key[0].get_timestamp()
        r = card.cmd_put_data(0x00, 0xce, timestamp1)
        assert r

    def test_timestamp_2_put(self, card):
        key = get_key(card)
        timestamp2 = key[1].get_timestamp()
        r = card.cmd_put_data(0x00, 0xcf, timestamp2)
        assert r

    def test_timestamp_3_put(self, card):
        key = get_key(card)
        timestamp3 = key[2].get_timestamp()
        r = card.cmd_put_data(0x00, 0xd0, timestamp3)
        assert r

    def test_ds_counter_0(self, card):
        c = get_data_object(card, 0x7a)
        assert c == b'\x93\x03\x00\x00\x00'

    def test_pw1_status(self, card):
        s = get_data_object(card, 0xc4)
        assert match(b'\x00...\x03[\x00\x03]\x03', s, DOTALL)

    def test_app_data(self, card):
        app_data = get_data_object(card, 0x6e)
        hist_len = app_data[20]
        # FIXME: parse and check DO of C0, C1, C2, C3, C4, and C6
        assert app_data[0:8] == b"\x4f\x10\xd2\x76\x00\x01\x24\x01" and \
               app_data[18:18+2] == b"\x5f\x52"

    def test_public_key_1(self, card):
        key = get_key(card)
        PK_Crypto = get_PK_Crypto(card)
        pk_info = card.cmd_get_public_key(1)
        assert key[0].get_pk() == PK_Crypto.pk_from_pk_info(pk_info)

    def test_public_key_2(self, card):
        key = get_key(card)
        PK_Crypto = get_PK_Crypto(card)
        pk_info = card.cmd_get_public_key(2)
        assert key[1].get_pk() == PK_Crypto.pk_from_pk_info(pk_info)

    def test_public_key_3(self, card):
        key = get_key(card)
        PK_Crypto = get_PK_Crypto(card)
        pk_info = card.cmd_get_public_key(3)
        assert key[2].get_pk() == PK_Crypto.pk_from_pk_info(pk_info)

    # Changing PW1 to admin-less mode

    def test_setup_pw1_0(self, card):
        r = card.change_passwd(1, FACTORY_PASSPHRASE_PW1, PW1_TEST0)
        assert r

    # Now, it's admin-less mode, auth-status admin cleared

    def test_verify_pw3_fail_1(self, card):
        try:
            v = card.verify(3, FACTORY_PASSPHRASE_PW3)
        except ValueError as e:
            v = False
        assert not v

    def test_verify_pw1_0(self, card):
        v = card.verify(1, PW1_TEST0)
        assert v

    def test_verify_pw1_0_2(self, card):
        v = card.verify(2, PW1_TEST0)
        assert v

    def test_setup_pw1_1(self, card):
        r = card.change_passwd(1, PW1_TEST0, PW1_TEST1)
        assert r

    def test_verify_pw1_1(self, card):
        v = card.verify(1, PW1_TEST1)
        assert v

    def test_verify_pw1_1_2(self, card):
        v = card.verify(2, PW1_TEST1)
        assert v

    def test_verify_pw3_admin_less_1(self, card):
        v = card.verify(3, PW1_TEST1)
        assert v

    # Reset code is not allowed in admin-less mode
    def test_setup_reset_code(self, card):
        if card.is_gnuk2:
            try:
                r = card.setup_reset_code(RESETCODE_TEST)
            except ValueError as e:
                r = e.args[0]
            assert r == "6f00"
        else:
            r = card.setup_reset_code(RESETCODE_TEST)
            assert r

    def test_reset_code(self, card):
        if card.is_gnuk2:
            r = card.change_passwd(1, PW1_TEST1, PW1_TEST2)
        else:
            r = card.reset_passwd_by_resetcode(RESETCODE_TEST, PW1_TEST2)
        assert r

    # Changing PW1, auth status for admin cleared
    def test_login_put_fail(self, card):
        try:
            r = card.cmd_put_data(0x00, 0x5e, b"gpg_user")
        except ValueError as e:
            r = e.args[0]
        assert r == "6982"

    def test_verify_pw1_2(self, card):
        v = card.verify(1, PW1_TEST2)
        assert v

    def test_verify_pw1_2_2(self, card):
        v = card.verify(2, PW1_TEST2)
        assert v

    def test_verify_pw3_fail_2(self, card):
        try:
            v = card.verify(3, FACTORY_PASSPHRASE_PW3)
        except ValueError as e:
            v = e.args[0]
        assert v == "6982"
