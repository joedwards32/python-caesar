#!/usr/bin/env python3
# -*- coding: utf-8 -*-
##############################################################################
# caesar.py
# A python application for encoding, decoding and brute forcing caesar ciphers
#
# Author: John Edwards <joedwards32@gmail.com>
# Date: 2020-01-21
# Version: 1.0
##############################################################################

### Imports
import os
import sys
import argparse
import random

### Constants

### Functions
def _is_char_shiftable(character):
    """Private function to determine if the specified character is valid for caesar shift"""
    if _unicode_value(character) >= 32 and _unicode_value(character) <= 126:
        return True
    else:
        return False

def _unicode_value(character):
    """Private function to convert a character to its integer value"""
    return ord(character)

def check_shift(shift):
    """Custom arg parse type check for shift value"""
    if int(shift) > 94 or int(shift) < -94:
        raise argparse.ArgumentTypeError("Shift must be between +94 and -94")
    return int(shift)

def _shift_character(character, shift):
    """Private function to caesar shift a single character"""
    check_shift(shift)
    if _is_char_shiftable(character):
        shifted_cha_value = _unicode_value(character) + shift
        # Ensure we only shift printable characters and that shifted
        # characters are always printable
        if shifted_cha_value > 126:
            shifted_cha_value = shifted_cha_value - 95
        elif shifted_cha_value < 32:
            shifted_cha_value = shifted_cha_value + 95
    else:
        shifted_cha_value = _unicode_value(character)
    return chr(shifted_cha_value)

def caesar_shift(plain_text, shift):
    """Cipher the supplied plain text using a basic caesar shift
    Inputs:
        plain_text - string to cipher
        shift - integer value to shift by
    Returns:
        Success - ciphered string
        Failure - exception"""
    cipher_text = ""
    for cha in plain_text:
        cipher_text = cipher_text + _shift_character(cha, shift)

    return cipher_text

def _analyse_character_frequency(cipher_text):
    """Private function to analyse the frequency of shiftable characters. Returns a list in order of frequency."""
    character_frequency = {}
    for cha in cipher_text:
        if _is_char_shiftable(cha):
            try:
                character_frequency[cha] += 1
            except KeyError:
                character_frequency[cha] = 0
    characters_by_frequency = sorted(character_frequency, key=character_frequency.__getitem__, reverse=True)
    return characters_by_frequency

def _probably_english(plain_text):
    """Private function to ascertain if the supplied plain text is likely to be valid english or not"""
    punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~' + "\n"
    plain_words = list(dict.fromkeys(plain_text.split(" ")))
    total_words = float(len(plain_words))
    english_words = float(0)
    words = _load_word_list()

    for plain_word in plain_words:
        for word in words:
            clean_plain_word = plain_word.strip(punctuation).lower()
            clean_word = word.lower()
            if len(clean_plain_word) > 1 and clean_plain_word == clean_word:
                english_words += 1
    probability_english = english_words / total_words
    # If at least 60% of the words are in our dictionary then this is probably plain english
    if probability_english < 0.6:
        return False
    else:
        return True

def brute_force_caesar(cipher_text):
    """Attempts to brute force caesar shifted cipher text using freqency analysis to improve performance
    Inputs:
        cipher_text - string of caesar ciphered text
    Outputs:
        plain_text - most likley plain text based on frequency analysis and dictionary check"""
    frequent_letters = [" ", "e", "t", "a", "o", "i", "n", "s", "r", "h", "l", "d", "c", "u", "m", "f", "p", "g", "w", "y", "b", "v", "k", "x", "j", "q", "z"]
    character_frequency = _analyse_character_frequency(cipher_text)
    plain_text = None
    # Loop through most common characters and attempt to make shift assumptions based on known english letter frequencies
    # Test assumptions against a dictionary of english words to see when we have hit the correct shift value.
    for cha in character_frequency:
        for letter in frequent_letters:
            probable_shift = _unicode_value(letter) - _unicode_value(cha)
            possible_plain_text = caesar_shift(cipher_text, probable_shift)
            if _probably_english(possible_plain_text):
                plain_text = possible_plain_text
                break
        if plain_text != None:
            break
    return plain_text

def _load_word_list(path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "words")):
    with open(path,"r") as f:
        words = f.read().splitlines()
    return words

def _args(argv):
    "Private function to handle CLI argument parsing."
    # Get Args
    parser = argparse.ArgumentParser(description='Encrypt, decrypt or brute force using a simple Caesar cipher.')
    parser.add_argument('-m', '--mode', nargs='?', choices=('encrypt', 'decrypt', 'force'), default="encrypt", help="Encrypt, decrypt or brute force input text.")
    parser.add_argument('-i', '--input-file', type=argparse.FileType('r'), default=(None if sys.stdin.isatty() else sys.stdin), help="Input file, defaults to stdin" )
    parser.add_argument('-o', '--output-file', type=argparse.FileType('w'), default=sys.stdout, help="Output file, defaults to stdout")
    parser.add_argument('-s', '--shift', type=check_shift, default=random.randint(1,93), help='Caesar shift value, defaults to a random number between 1 and 93')
    return parser.parse_args(argv)

### Main
def main(argv):
    # Parse arguments
    args = _args(argv)
    input = None
    output = None
    shift = args.shift
    mode = args.mode

    # Read input
    if args.input_file is sys.stdin:
        inf = sys.stdin
    else:
        try:
            inf = args.input_file
        except Exception as e:
            print("Input file can not be read: " + str(e), file=sys.stderr)
            return 1
    if inf != None:
        input = inf.read()
        if inf is not sys.stdin:
            inf.close()
    else:
        input = ""

    # Process input
    if mode == 'encrypt':
        output = caesar_shift(input,shift)
    elif mode == 'decrypt':
        output = caesar_shift(input,(shift - ( shift * 2 )))
    elif mode == 'force':
        output = brute_force_caesar(input)

    # Write output
    if args.output_file is sys.stdout:
        if output != None:
            sys.stdout.write(output)
    else:
        outf = args.output_file
        try:
            outf.write(output)
            outf.close()
        except Exception as e:
            print("Error writing output: " + str(e), file=sys.stderr)
            return 1
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
