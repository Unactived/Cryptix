# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#####################################################################

# FrenchMasterSword, Cryptix, 2018
#####################################################################

# Encrypting functions
# Each should take at least three first arguments :
# the window instance : self (mostly for error messages)
# a boolean : True => encrypt, False => decrypt
# the text to process
#
# depending of the cypher, one or two keys may also be necessary
# this is used to control how many line fields should be editable.
# they should then be called key and key2
#
# They should return a string, or an exception to be processed

import json
import re
from functools import wraps
from itertools import cycle
from string import ascii_letters
# from math import ceil
from PySide2.QtWidgets import QMessageBox

with open('settings.json', 'r') as file:
    settingsDict = json.load(file)

UNUSED = settingsDict["removed letter"]
REPLACED = settingsDict["replace letter"]

# catched is a dict {"ExceptionName": "Warning text"}
def catch(catched={}):
    def catch_decorator(func):
        @wraps(func)
        def func_wrapper(*args):
            try:
                return func(*args)
            except Exception as e:
                name = e.__class__.__name__
                if name in catched:
                    return QMessageBox.warning(args[0], "Warning", catched[name].replace('ERROR', e.args[0]))
                else:
                    return QMessageBox.critical(args[0], "Error", repr(e))
        return func_wrapper
    return catch_decorator

def _isascii(string: str):
    return all((char in ascii_letters for char in string))

def _create_alphabet(key: str, remove=True) -> list:
    """
    generate a transposition alphabet

    """
    key = re.sub(r'[^a-zA-Z]', '', key).upper # remove non alphabetical

    alphabet = ''
    for char in key:
        if _isascii(char) and not char in alphabet:
            alphabet += char
    for i in range(65, 91):
        if not chr(i) in alphabet:
            alphabet += chr(i)

    if not remove:
        return alphabet

    return alphabet.replace(UNUSED, '')

@catch()
def simple(self, encrypt: bool, text: str, key: str):
    """
    Simply replace letters in the alphabet with those in the key. 
    You don't have to enter a complete one, as it will be generated from it.

    """

    key = _create_alphabet(key, False)
    pass

@catch({'ValueError': 'You should enter a valid integer as the key.'})
def caesar(self, encrypt: bool, text: str, key: str):
    """
    Shifts the text's letter in the alphabet of the number given as key.

    """

    key = int(key)

    if not encrypt:
        key = - key
    result = ''
    for char in text:
        if _isascii(char):
            letter = char.upper()
            letter = chr((ord(letter) - 65 + key) % 26 + 65)
            if char.islower():
                letter = letter.lower()
        else:
            letter = char
        result += letter
    return result

@catch({'KeyError': '<b>ERROR</b> is not recognized in standard morse code'})
def morse(self, encrypt: bool, text: str):
    """
    Transpose in standard morse code.

    """

    morseCode = {
        "A": ".-",
        "B": "-...",
        "C": "-.-.",
        "D": "-..",
        "E": ".",
        "F": "..-.",
        "G": "--.",
        "H": "....",
        "I": "..",
        "J": ".---",
        "K": "-.-",
        "L": ".-..",
        "M": "--",
        "N": "-.",
        "O": "---",
        "P": ".--.",
        "Q": "--.-",
        "R": ".-.",
        "S": "...",
        "T": "-",
        "U": "..-",
        "V": "...-",
        "W": ".--",
        "X": "-..-",
        "Y": "-.--",
        "Z": "--..",
        "0": "-----",
        "1": ".----",
        "2": "..---",
        "3": "...--",
        "4": "....-",
        "5": ".....",
        "6": "-....",
        "7": "--...",
        "8": "---..",
        "9": "----.",
        ".": ".-.-.-",
        ",": "--..--",
        "?": "..--..",
        "'": ".----.",
        "!": "-.-.--", # May be ---. in North America: Ignored
        "/": "-..-.",
        "(": "-.--.",
        ")": "-.--.",
        "&": ".-...",
        ":": "---...",
        ";": "-.-.-.",
        "=": "-...-",
        "+": ".-.-.",
        "-": "-....-",
        "_": "..--.-",
        '"': ".-..-.",
        "$": "...-..-",
        "@": ".--.-.",
        " ": "/" # For program design
    }

    inverseMorseCode = dict((v,k) for (k,v) in morseCode.items())

    if encrypt:
        result = ''
        for char in text:
            if char == '\n':
                result = result[:-1] + char
            else:
                result += morseCode[char.upper()]
                result += ' '
        result = result[:-1]

    else:
        result = []
        textLines = text.split('\n')
        for line in textLines:
            line = line.strip(' /')
            resultLine = ''
            textList = line.split('/')
            for word in textList:
                word = word.strip(' ')
                for char in word.split(' '):
                    resultLine += inverseMorseCode[char]
                resultLine += ' '
            resultLine = resultLine[:-1] # remove superficial ending space
            result.append(resultLine)
        result = '\n'.join(result)

    return result

@catch({
    'ValueError': 'Use only standard alphabet letters ; <b>ERROR</b> is not valid.',
    'IndexError': 'A digit is out of the grid.'
})
def polybius(self, encrypt: bool, text: str, key: str):
    """
    Replace letters by their abscissa and ordinate in a grid.
    If a key is given, it starts filling the grid, and finishes with the rest of the alphabet.

    The second grid is an example with 'CRYPTIX' used as key.
    As there are only 25 squares, one letter is removed and replaced.

    """

    key = _create_alphabet(key, False)

    result = ''
    if encrypt:
        i = 0 # for error handling
        for char in text.upper():
            if char == UNUSED:
                char = REPLACED
            if _isascii(char):
                pos = key.index(char)
                char = str((pos+1)//5 + 1 - ((pos+1)%5==0))+ str((pos+1)%5)
            result += char
            i += 1
        result = re.sub('0', '5', result)
    else:
        text = re.sub('0', '5', text)

        # List of 5 lists of 5
        polybius = [[key[y] for y in range(5*i, 5*(i+1))] for i in range(5)]

        i = 0
        while i < len(text):
            char = text[i]
            if char.isdigit():
                char = polybius[int(text[i])-1][int(text[i+1])-1]
                i += 1
            result += char
            i += 1

    return result

@catch()
def adfgvx(self, encrypt: bool, text: str, key: str):
    """
    Same as Polybius, but grid is indexed with these 6 letters and also encrypt digits.
    
    """

    key = _create_alphabet(key, False)
    pass

@catch({'IndexError': 'You need to enter a valid key'})
def vigenere(self, encrypt: bool, text: str, key: str):
    """
    Uses the letters in the key to shift (as in Caesar cipher) the letters in the text (A:0, B:1, Z:25).
    If it's shorter than the text, the key is repeated.

    """
    if not encrypt:
        encrypt = -1
    result = ''
    key = cycle(key.upper())
    for letter in text.upper():
        if _isascii(letter):
            letter = chr((ord(letter) + (encrypt * ord(next(key))) - 130) % 26 + 65)
        result += letter

    return result

@catch()
def wolseley(self, encrypt: bool, text: str, key: str):
    """
    Replaces letters with a reversed alphabet, missing a letter.

    """

    key = _create_alphabet(key, False)
    keyReverse = key[::-1]

    if not encrypt:
        key, keyReverse = keyReverse, key

    result = ''
    for letter in text.upper():
        if _isascii(letter):
            letter = keyReverse[key.find(letter)]
        result += letter

    return result

@catch({'ValueError': 'You need to enter a valid positive integer as the key'})
def gronsfeld(self, encrypt: bool, text: str, key: str):
    """
    Uses the digits in the key to shift (as in Caesar cipher) the letters in the text.
    If it's shorter than the text, the key is repeated.

    """

    if not encrypt:
        encrypt = -1
    result = ''
    key = cycle((int(i) for i in key))
    for letter in text.upper():
        if _isascii(letter):
            letter = chr((ord(letter) +  (encrypt * next(key) - 65)) % 26 + 65)
        result += letter

    return result

@catch({'ValueError': 'You need to enter valid integers as keys'})
def affine(self, encrypt: bool, text: str, key: str, key2: str):
    """
    Given a and b constants, x letter of the plain text and y letter of the encrypted one, : y = ax + b (modulo 26).
    Note that if a = 0, it's equivalent to Caesar cipher, and if b = 0, 'A' is always ciphered 'A'.

    """

    key, key2 = int(key), int(key2)
    result = ''
    for letter in text.upper():
        if _isascii(letter):
            letter = ord(letter) - 65
            if encrypt:
                letter = letter * key + key2
            else:
                letter = (letter - key2) // key
            letter = chr(letter % 26 + 65)
        result += letter
    return result

@catch({'IndexError': 'You need to enter a valid key'})
def beaufort(self, encrypt: bool, text: str, key: str):
    """
    A bit like the opposite of Vigenere cipher.
    Instead of adding the key's letters to those of the plain text ;
    we substract the plain text's letters to those of the key.

    """

    result = ''
    key = cycle((ord(k) for k in key.upper()))
    for letter in text.upper():
        if _isascii(letter):
            letter = chr((next(key) - ord(letter) + 130) % 26 + 65)
        result += letter
    return result

@catch()
def collon(self, encrypt: bool, text: str, key: str, key2: str):
    """
    With the help of the grid on the left (which you can generate with the key),
    each letter is converted to a bigram (a group of two letters)
    representing the abscissa and ordinate (or the ordinate and abscissa) in the grid.
    For instance, R will become CS (or SC). The script will randomly alternate these two options to renforce the cipher.

    Then, each bigram is entered under the letter in the two lines,
    and following a given number, the first and second line are added to the ciphered text.
    Here the number being 7, it will be ICQCKKK then QZSQZSS then KKCICEE etc. until the end.

    Notice that the ciphered text will be twice longer than the plain one: ICQCKKKQZSQZSSKKCICEEZVQQVVQCS.

    """
    key2 = int(key2)
    key = _create_alphabet(key, False)

    # 5x5 grid
    # grid = [[key[y] for y in range(5*i, 5*(i+1))] for i in range(5)]

    for letter in text.upper():
        if _isascii(letter):
            pos = key.index(letter)
            location = [(pos)//5 - ((pos)%5==0), (pos)%5]
            print(location)
