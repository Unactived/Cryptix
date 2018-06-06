# Encrypting functions
# Each should take at least two first arguments :
# a boolean : True => encrypt, False => decrypt
# the text to process

def caesar(encrypt, text, shift):
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
