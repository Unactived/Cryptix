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
# **kwargs is for key, which may be useless, but still sent
#
# They should return a string

from PySide2.QtWidgets import QMessageBox

def simple(self, encrypt, text, key=''):
    pass

def caesar(self, encrypt, text, key='0'):
    """
    Replace each letter in the text by the letter

    """

    try:
        try:
            key = int(key)
        except ValueError:
            return QMessageBox.warning(self, "Caesar Warning", "You should enter a valid number as key.")

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

    except Exception as e:
        return QMessageBox.critical(self, "Caesar error", repr(e))

def morse(self, encrypt, text, **kwargs):
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

    result = ''
    try:
        if '\n' in text:
            return QMessageBox.warning(self, "Morse Warning",
             "You can only write on a line")

        if encrypt:
            for char in text:
                result += morseCode[char.upper()]
                result += ' '

        else:
            textList = text.split('/')
            for word in textList:
                word = word.strip(' ')
                for char in word.split(' '):
                    result += inverseMorseCode[char]
                result += ' '

        return result[:-1] # remove superficial ending space

    except KeyError as e:
        return QMessageBox.warning(self, "Morse error",
        f"<b>{e.args[0]}</b> is not recognized in standard morse code")

    except Exception as e:
        return QMessageBox.critical(self, "Morse error",
         repr(e))

def polybe(self, encrypt, text, **kwargs):
    pass

def adfgvx(self, encrypt, text, **kwargs):
    pass

def vigenere(self, encrypt, text, **kwargs):
    pass
