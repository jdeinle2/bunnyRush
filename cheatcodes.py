# Secret cheat code conversion from keydown E.g. K_0 == 48, K_9 = 57, so minus 48 to convert to an actual number

def validate(key,  max_level):
    level = (key.value - 48)
    if level > 0 and level <= max_level:
        print ("Super secret code was just entered! Going to level ", level, "max_level:", max_level)
        return level
    return 0
