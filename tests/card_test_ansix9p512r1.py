"""
card_test_ansix9p512r1.py - test ansix9p512r1 support

Copyright (C) 2021  Vincent Pelletier <plr.vincent@gmail.com>

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

from func_pso_auth import assert_ec_pso
from card_const import *

class Test_Card_AnsiX9P512R1(object):
    def test_ECDH_reference_vectors(self, card):
        assert card.verify(3, FACTORY_PASSPHRASE_PW3)
        assert card.verify(2, FACTORY_PASSPHRASE_PW1)
        # https://tools.ietf.org/html/rfc5903#section-8.3
        assert_ec_pso(
            card=card,
            key_index=1,
            key_attributes=KEY_ATTRIBUTES_ECDH_ANSIX9P521R1,
            key_attribute_caption='ECDH ansix9p521r1',
            private_key=(
                b'\x00\x37\xAD\xE9\x31\x9A\x89\xF4\xDA\xBD\xB3\xEF\x41\x1A\xAC\xCC'
                b'\xA5\x12\x3C\x61\xAC\xAB\x57\xB5\x39\x3D\xCE\x47\x60\x81\x72\xA0'
                b'\x95\xAA\x85\xA3\x0F\xE1\xC2\x95\x2C\x67\x71\xD9\x37\xBA\x97\x77'
                b'\xF5\x95\x7B\x26\x39\xBA\xB0\x72\x46\x2F\x68\xC2\x7A\x57\x38\x2D'
                b'\x4A\x52'
            ),
            expected_public_key=(
                b'\x04'
                b'\x00\x15\x41\x7E\x84\xDB\xF2\x8C\x0A\xD3\xC2\x78\x71\x33\x49\xDC'
                b'\x7D\xF1\x53\xC8\x97\xA1\x89\x1B\xD9\x8B\xAB\x43\x57\xC9\xEC\xBE'
                b'\xE1\xE3\xBF\x42\xE0\x0B\x8E\x38\x0A\xEA\xE5\x7C\x2D\x10\x75\x64'
                b'\x94\x18\x85\x94\x2A\xF5\xA7\xF4\x60\x17\x23\xC4\x19\x5D\x17\x6C'
                b'\xED\x3E'
                b'\x01\x7C\xAE\x20\xB6\x64\x1D\x2E\xEB\x69\x57\x86\xD8\xC9\x46\x14'
                b'\x62\x39\xD0\x99\xE1\x8E\x1D\x5A\x51\x4C\x73\x9D\x7C\xB4\xA1\x0A'
                b'\xD8\xA7\x88\x01\x5A\xC4\x05\xD7\x79\x9D\xC7\x5E\x7B\x7D\x5B\x6C'
                b'\xF2\x26\x1A\x6A\x7F\x15\x07\x43\x8B\xF0\x1B\xEB\x6C\xA3\x92\x6F'
                b'\x95\x82'
            ),
            pso_input=(
                b'\xa6\x81\x8c\x7f\x49\x81\x88\x86\x81\x85'
                b'\x04'
                b'\x00\xD0\xB3\x97\x5A\xC4\xB7\x99\xF5\xBE\xA1\x6D\x5E\x13\xE9\xAF'
                b'\x97\x1D\x5E\x9B\x98\x4C\x9F\x39\x72\x8B\x5E\x57\x39\x73\x5A\x21'
                b'\x9B\x97\xC3\x56\x43\x6A\xDC\x6E\x95\xBB\x03\x52\xF6\xBE\x64\xA6'
                b'\xC2\x91\x2D\x4E\xF2\xD0\x43\x3C\xED\x2B\x61\x71\x64\x00\x12\xD9'
                b'\x46\x0F'
                b'\x01\x5C\x68\x22\x63\x83\x95\x6E\x3B\xD0\x66\xE7\x97\xB6\x23\xC2'
                b'\x7C\xE0\xEA\xC2\xF5\x51\xA1\x0C\x2C\x72\x4D\x98\x52\x07\x7B\x87'
                b'\x22\x0B\x65\x36\xC5\xC4\x08\xA1\xD2\xAE\xBB\x8E\x86\xD6\x78\xAE'
                b'\x49\xCB\x57\x09\x1F\x47\x32\x29\x65\x79\xAB\x44\xFC\xD1\x7F\x0F'
                b'\xC5\x6A'
            ),
            expected_pso_output=(
                b'\x01\x14\x4C\x7D\x79\xAE\x69\x56\xBC\x8E\xDB\x8E\x7C\x78\x7C\x45'
                b'\x21\xCB\x08\x6F\xA6\x44\x07\xF9\x78\x94\xE5\xE6\xB2\xD7\x9B\x04'
                b'\xD1\x42\x7E\x73\xCA\x4B\xAA\x24\x0A\x34\x78\x68\x59\x81\x0C\x06'
                b'\xB3\xC7\x15\xA3\xA8\xCC\x31\x51\xF2\xBE\xE4\x17\x99\x6D\x19\xF3'
                b'\xDD\xEA'
            ),
        )