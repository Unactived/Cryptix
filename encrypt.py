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
# They should also return a string

from PySide2 import QtWidgets, QtGui

def caesar(self, encrypt, text, shift):
    try:
        if not encrypt:
            shift = - shift
        result = ''
        for char in text:
            if char.isalpha():
                letter = char.upper()
                letter = chr((ord(letter) - 65 + shift) % 26 + 65)
                if char.islower():
                    letter = letter.lower()
            else:
                letter = char
            result += letter
        return result
    except Exception as e:
        return QtWidgets.QMessageBox.critical(self, "Algorithm error", repr(e))

def morse(self, encrypt, text):
    morseCode = {
        "A" : ".-",
        "B" : "-...",
        "C" : "-.-.",
        "D" : "-..",
        "E" : ".",
        "F" : "..-.",
        "G" : "--.",
        "H" : "....",
        "I" : "..",
        "J" : ".---",
        "K" : "-.-",
        "K" : "-.-",
        "L" : ".-..",
        "M" : "--",
        "N" : "-.",
        "O" : "---",
        "P" : ".--.",
        "Q" : "--.-",
        "R" : ".-.",
        "S" : "...",
        "T" : "-",
        "U" : "..-",
        "V" : "...-",
        "W" : ".--",
        "X" : "-..-",
        "Y" : "-.--",
        "Z" : "--..",
        "0" : "-----",
        "1" : ".----",
        "2" : "..---",
        "3" : "...--",
        "4" : "....-",
        "5" : ".....",
        "6" : "-....",
        "7" : "--...",
        "8" : "---..",
        "9" : "----.",
        "." : ".-.-.-",
        "," : "--..--",
        "?" : "..--..",
        "'" : ".----.",
        "!" : "-.-.--", # May be ---. in North America: Ignored
        "/" : "-..-.",
        "(" : "-.--.",
        ")" : "-.--.",
        "&" : ".-...",
        ":" : "---...",
        ";" : "-.-.-.",
        "=" : "-...-",
        "+" : ".-.-.",
        "-" : "-....-",
        "_" : "..--.-",
        '"' : ".-..-.",
        "$" : "...-..-",
        "@" : ".--.-.",
        " " : "/" # For program design
    }

    inverseMorseCode = dict((v,k) for (k,v) in morseCode.items())

    result = ''
    try:
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

    except Exception as e:
        return QtWidgets.QMessageBox.critical(self, "Morse error", repr(e))
