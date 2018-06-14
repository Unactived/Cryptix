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
# key is for key, which may be useless, but still sent
#
# They should return a string

from PySide2.QtWidgets import QMessageBox

def _check_alphabet(text):
    """
    Checks that given text is

    """

def _create_alphabet(key):
    """
    generate a transposition alphabet

    """

    alphabet = ''
    for letter in key.upper():
        if not letter in alphabet:
            alphabet += letter
    for i in range(65, 91):
        if not chr(i) in alphabet:
            alphabet += chr(i)

    return alphabet

def simple(self, encrypt, text, key):
    pass

def caesar(self, encrypt, text, key):
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

def morse(self, encrypt, text, key):
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

def polybe(self, encrypt, text, key):
    try:
        for char in key[:26]:
            if not (ord(char.upper()) > 64 and ord(char.upper()) < 91):
                return QMessageBox.warning(self, "Polybe warning",
                "Key should only be composed of alphabetic letters.")
        key = _create_alphabet(key.upper()[:26])

        # Removing 'J' to get 25 letters
        # TODO: Choose this letter or offer to remove 'W' instead
        key = key[:key.index('J')] + key[key.index('J')+1:]

        result = ''
        if encrypt:
            for char in text.upper():
                if char == 'J':
                    char = 'I'
                if char.isalpha():
                    pos = key.index(char)
                    char = str((pos+1)//5 + 1 - ((pos+1)%5==0))+ str((pos+1)%5)
                result += char
        else:
            polybe = []

            # List of 5 lists of 5 characters
            for i in range(5):
                list = []
                for y in range(5*i, 5*(i+1)):
                    list.append(key[y])
                polybe.append(list)

            i = 0
            while i < len(text):
                char = text[i]
                # print(text[i:i+2])
                if char.isdigit():
                    char = polybe[int(text[i])-1][int(text[i+1])-1]
                    i += 1
                result += char
                i += 1

        return result

    except Exception as e:
        return QMessageBox.critical(self, "Polybe error",
        repr(e))

def adfgvx(self, encrypt, text, key):
    pass

def vigenere(self, encrypt, text, key):
    pass
