#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import caesar
import os
import argparse

class TestCaesar(unittest.TestCase):
    def test__args(self):
        args = caesar._args(['-m', 'encrypt', '-s', '1'])
        self.assertEqual(args.mode, 'encrypt')
        self.assertEqual(args.shift, 1)

    def test__args_bad_mode(self):
        with self.assertRaises(SystemExit):
            self.assertRaises(argparse.ArgumentError, caesar._args, ['-m', 'unsupported mode'])

    def test__is_char_shiftable_true(self):
        c = 'a'
        self.assertEqual(caesar._is_char_shiftable(c), True)

    def test__is_char_shiftable_false(self):
        c = 'Ö'
        self.assertEqual(caesar._is_char_shiftable(c), False)

    def test__unicode_value(self):
        c = 'a'
        self.assertEqual(caesar._unicode_value(c), 97)

    def test_check_shift_pass(self):
        shift = 14
        self.assertEqual(caesar.check_shift(shift), 14)

    def test_check_shift_fail(self):
        shift = 100
        self.assertRaises(argparse.ArgumentTypeError, caesar.check_shift, shift)

    def test__shift_character(self):
        c = 'a'
        self.assertEqual(caesar._shift_character(c, 2), "c")

    def test__shift_character_wrap(self):
        c = 'z'
        self.assertEqual(caesar._shift_character(c, 90), "u")

    def test_caesar_shift(self):
        string = 'a b c d e f'
        shift = 14
        self.assertEqual(caesar.caesar_shift(string,shift), "o.p.q.r.s.t")

    def test__analyse_character_frequency(self):
        string = 'ffffffeeeeeddddcccbba '
        self.assertEqual(caesar._analyse_character_frequency(string), ['f', 'e', 'd', 'c', 'b', 'a', ' '])

    def test__probably_english_true(self):
        string = """This is a test of the probably english function.
It needs to be a certain length for an good guess to be made."""
        self.assertEqual(caesar._probably_english(string), True)

    def test__probably_english_false(self):
        string = """Dies ist ein Test der wahrscheinlich englischen Funktion.
Es muss eine bestimmte Länge haben, damit eine gute Vermutung angestellt werden kann."""
        self.assertEqual(caesar._probably_english(string), False)

    def test_brute_force_caesar(self):
        cipher_text = """aur r-%n!-n-p|z}#"r -"un"-p vrq9
/Z'-"rpu{vpny-ov"!-un$r-nyy-orr{-s vrq9
V-"||x-"||-zn{'-w|y"!
S |z-"||-zn{'-$|y"!;;;/
5[|-%|{qr -"ur- #qq'-"uv{t-qvrq6."""
        plain_text = """There was a computer that cried,
"My technical bits have all been fried,
I took too many jolts
From too many volts..."
(No wonder the ruddy thing died)!"""
        self.assertEqual(caesar.brute_force_caesar(cipher_text), plain_text)

if __name__ == '__main__':
    unittest.main()
