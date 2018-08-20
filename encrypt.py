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

import re
# from math import ceil
from PySide2.QtWidgets import QMessageBox

with open('settings.json', 'r') as file:
    settingsDict = json.load(file)

UNUSED = settingsDict["removed letter"]
def _create_alphabet(key: str) -> list:
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

    return alphabet

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
            if char.isalpha():
                letter = char.upper()
                letter = chr((ord(letter) - 65 + key) % 26 + 65)
                if char.islower():
                    letter = letter.lower()
            else:
                letter = char
            result += letter
        return result

    except ValueError:
        return QMessageBox.warning(self, "Caesar Warning",
        "You should enter a valid number as key.")

    except Exception as e:
        return QMessageBox.critical(self, "Caesar error", repr(e))

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
        return QMessageBox.warning(self, "Morse error",
        f"<b>{e.args[0]}</b> is not recognized in standard morse code")

    except Exception as e:
        return QMessageBox.critical(self, "Morse error", repr(e))

def polybe(self, encrypt: bool, text: str, key: str):
    try:
        key = _create_alphabet(key)

        # Removing one letter to make 25
        key = key[:key.index(UNUSED)] + key[key.index(UNUSED)+1:]

        result = ''
        if encrypt:
            i = 0 # for error handling
            for char in text.upper():
                if char == UNUSED:
                    char = REPLACED
                if char.isalpha():
                    pos = key.index(char)
                    char = str((pos+1)//5 + 1 - ((pos+1)%5==0))+ str((pos+1)%5)
                result += char
                i += 1
            result = re.sub('0', '5', result)
        else:
            text = re.sub('0', '5', text)

            # List of 5 lists of 5
            polybe = [[key[y] for y in range(5*i, 5*(i+1))] for i in range(5)]

            i = 0
            while i < len(text):
                char = text[i]
                if char.isdigit():
                    char = polybe[int(text[i])-1][int(text[i+1])-1]
                    i += 1
                result += char
                i += 1

        return result

    except ValueError:
        # Not in grid (encrypt)
        return QMessageBox.warning(self, "Polybe error",
        f"<b>{text[i]}</b> is not valid.")

    except IndexError:
        # Invalid number (decrypt)
        return QMessageBox.warning(self, "Polybe error",
        f"<b>{text[i:i+2]}</b> is out of grid.")

    except Exception as e:
        return QMessageBox.critical(self, "Polybe error", repr(e))

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
        i = 0
        for letter in text.upper():
            if letter.isalpha():
                letter = chr((ord(letter)\
                + (encrypt * ord(key.upper()[i])) - 130) % 26 + 65)
                i += 1
                i %= len(key)
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
        key = _create_alphabet(key)
        # Removing one letter to make 25
        key = key[:key.index(UNUSED)] + key[key.index(UNUSED)+1:]
        keyReverse = key[::-1]

        if not encrypt:
            key, keyReverse = keyReverse, key

        result = ''
        for letter in text.upper():
            if letter.isalpha():
                letter = keyReverse[key.find(letter)]
            result += letter

        return result

    except Exception as e:
        return QMessageBox.critical(self, "Wolseley error", repr(e))

def gronsfeld(self, encrypt: bool, text: str, key: str):
    try:
        if not encrypt:
            encrypt = -1
        result = ''
        i = 0
        for letter in text.upper():
            if letter.isalpha():
                letter = chr((ord(letter) +  (encrypt * int(key[i]) - 65)) % 26 + 65)
            result += letter
            i += 1
            i %= len(key)

        return result

    except IndexError:
        # Error with the key
        return QMessageBox.warning(self, "Gronsfeld warning",
        "You need to enter a valid number as key")

    except Exception as e:
        return QMessageBox.critical(self, "Gronsfeld error", repr(e))

def affine(self, encrypt: bool, text: str, key: str, key2: str):
    pass

def beaufort(self, encrypt: bool, text: str, key: str):
    try:
        result = ''
        i = 0
        for letter in text.upper():
            if letter.isalpha():
                letter = chr((ord(key.upper()[i]) - ord(letter) + 130) % 26 + 65)
                i += 1
                i %= len(key)
            result += letter
        return result

    except IndexError:
        # Error with the key
        return QMessageBox.warning(self, "Beaufort Warning",
        "You need to enter a valid key")

    except Exception as e:
        return QMessageBox.critical(self, "Beaufort Error", repr(e))

def collon(self, encrypt: bool, text: str, key: str):
    pass
