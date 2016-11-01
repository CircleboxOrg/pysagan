
def signed(number, bitLength):
    basetop = 1 << bitLength
    base = (basetop / 2) - 1
    if (number > base):
        number -= basetop
    return number