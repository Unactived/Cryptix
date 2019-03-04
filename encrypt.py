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
from itertools import cycle
from string import ascii_letters
# from math import ceil
from PySide2.QtWidgets import QMessageBox

with open('settings.json', 'r') as file:
    settingsDict = json.load(file)

UNUSED = settingsDict["removed letter"]
REPLACED = settingsDict["replace letter"]

def _isascii(string: str):
    return all((char in ascii_letters for char in string))

def _create_alphabet(key: str, polybius=False) -> list:
    """
    generate a transposition alphabet, with numbers

    """
    key = re.sub(r'[^a-zA-Z]', '', key) # remove non alphanumeric

    alphabet = ''
    for char in key.upper():
        # Avoid repetitions of characters
        if char.isalnum() and not char in alphabet:
            alphabet += char
    for i in range(65, 91):
        if not chr(i) in alphabet:
            alphabet += chr(i)

    if not polybius:
        return alphabet

    return alphabet.replace(UNUSED, '')

def simple(self, encrypt: bool, text: str, key: str):
    pass

def caesar(self, encrypt: bool, text: str, key: str):
    """
    Replace each letter in the text by the letter

    """

    try:
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

    except ValueError:
        return QMessageBox.warning(self, "Warning",
        "You should enter a valid integer as the key.")

    except Exception as e:
        return QMessageBox.critical(self, "Error", repr(e))

def morse(self, encrypt: bool, text: str):
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

    try:
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

    except KeyError as e:
        return QMessageBox.warning(self, "Error",
        f"<b>{e.args[0]}</b> is not recognized in standard morse code")

    except Exception as e:
        return QMessageBox.critical(self, "Error", repr(e))

def polybius(self, encrypt: bool, text: str, key: str):
    try:
        key = _create_alphabet(key, True)

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

    except ValueError:
        # Not in grid (encrypt)
        return QMessageBox.warning(self, "Error",
        f"Use only standard alphabet letters ; <b>{text[i]}</b> is not valid.")

    except IndexError:
        # Invalid number (decrypt)
        return QMessageBox.warning(self, "Error",
        f"<b>{text[i:i+2]}</b> is out of grid.")

    except Exception as e:
        return QMessageBox.critical(self, "Error", repr(e))

def adfgvx(self, encrypt: bool, text: str, key: str):
    pass

def vigenere(self, encrypt: bool, text: str, key: str):
    """
    Vigenere = Caesar with key's letters acting as the shift for the letters
    in the text


    """
    try:
        if not encrypt:
            encrypt = -1
        result = ''
        key = cycle(key.upper())
        for letter in text.upper():
            if _isascii(letter):
                letter = chr((ord(letter) + (encrypt * ord(next(key))) - 130) % 26 + 65)
            result += letter

        return result

    except IndexError:
        # Error with the key
        return QMessageBox.warning(self, "Warning",
        "You need to enter a valid key")

    except Exception as e:
        return QMessageBox.critical(self, "Error", repr(e))

def wolseley(self, encrypt: bool, text: str, key: str):
    try:
        key = _create_alphabet(key, True)
        keyReverse = key[::-1]

        if not encrypt:
            key, keyReverse = keyReverse, key

        result = ''
        for letter in text.upper():
            if _isascii(letter):
                letter = keyReverse[key.find(letter)]
            result += letter

        return result

    except Exception as e:
        return QMessageBox.critical(self, "Error", repr(e))

def gronsfeld(self, encrypt: bool, text: str, key: str):
    try:
        if not encrypt:
            encrypt = -1
        result = ''
        key = cycle((int(i) for i in key))
        for letter in text.upper():
            if _isascii(letter):
                letter = chr((ord(letter) +  (encrypt * next(key) - 65)) % 26 + 65)
            result += letter

        return result

    except ValueError:
        # Error with the key
        return QMessageBox.warning(self, "Warning",
        "You need to enter a valid positive integer as the key")

    except Exception as e:
        return QMessageBox.critical(self, "Error", repr(e))

def affine(self, encrypt: bool, text: str, key: str, key2: str):
    try:
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
    except Exception as e:
        return QMessageBox.critical(self, "Error", repr(e))

def beaufort(self, encrypt: bool, text: str, key: str):
    try:
        result = ''
        key = cycle((ord(k) for k in key.upper()))
        for letter in text.upper():
            if _isascii(letter):
                letter = chr((next(key) - ord(letter) + 130) % 26 + 65)
            result += letter
        return result

    except IndexError:
        # Error with the key
        return QMessageBox.warning(self, "Warning",
        "You need to enter a valid key")

    except Exception as e:
        return QMessageBox.critical(self, "Error", repr(e))

def collon(self, encrypt: bool, text: str, key: str, key2: str):
    try:
        key2 = int(key2)
        key = _create_alphabet(key, True)

        # 5x5 grid
        # grid = [[key[y] for y in range(5*i, 5*(i+1))] for i in range(5)]

        for letter in text.upper():
            if _isascii(letter):
                pos = key.index(letter)
                location = [(pos)//5 - ((pos)%5==0), (pos)%5]
                print(location)

    except Exception as e:
        return QMessageBox.critical(self, "Error", repr(e))
