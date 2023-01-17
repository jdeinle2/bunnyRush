# Secret cheat code conversion from keydown E.g. K_0 == 48, K_9 = 57, so minus 48 to convert to an actual number

secret_word = ['h', 'o', 'p']
CHEAT = 0

letter = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def check_secret_word(key):
    global secret_word
    global letter
    global CHEAT
    character = key.value - 97
    if (character < 0 or character > 25):
        return 0
    if letter[character] == secret_word[CHEAT]:
        CHEAT = CHEAT + 1
    else:
        CHEAT = 0
    print ("CHEATCODE PROGRESS: ", CHEAT)
    if CHEAT >= len(secret_word):
        print ("CHEATCODE ACCEPTED!!")
        return 1
    else:
        return 0

def validate(key,  max_level):
    level = (key.value - 48)
    #print ("Checking key.value", key.value)
    if level > 0 and level <= max_level:
        print ("Super secret code was just entered! Going to level ", level, "max_level:", max_level)
        return level
    return 0
