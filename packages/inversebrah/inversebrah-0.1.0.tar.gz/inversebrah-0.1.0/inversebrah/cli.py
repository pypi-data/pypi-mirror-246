#Sauce, runs on all TI-84 Python calculators:
import random
import time

def expand_key(grammar, key):
    if key not in grammar:
        return key

    phrase = random.choice(grammar[key])
    return expand_phrase(grammar, phrase)

def find_keys(phrase):
    keys = []
    key = ''
    recording = False
    
    for char in phrase:
        if char == '#' and not recording:
            recording = True
        elif char == '#' and recording:
            keys.append(key)
            key = ''
            recording = False
        elif recording:
            key += char
            
    return keys

def expand_phrase(grammar, phrase):
    
    while "#" in phrase:
        keys = find_keys(phrase)
        
        for key in keys:
            phrase = phrase.replace("#" + key + "#", expand_key(grammar, key), 1)
            
    return phrase

# inversebrah summon
grammar = {
    "origin": ["#inversebrah# #getmein# #lilshid# #aw#","#aw# #inversebrah# #getmein# #lilshid#"],
    "inversebrah": ["@inversebrah", "", "inversebrah","inverted brother"],
    "getmein": ["get me in", "put me in","me too", "come here", "come on in", "do your thing", "do your job", "screenshot dis", "yo","come in"],
    "lilshid": ["smolting", "lil shid", "#snot# #salamander#",""],
    "snot" : ["snot","ugly","green", "weird","hybrid","mutated"],
    "salamander" : ["salamander","frok","platypus","cucumber","pickle"],
    "aw" : ["aw","lmwo","lmeow","iwo","jfw" ""]
}

def main():
    # Generate inversebrah notifs
    smoltingsummon = expand_phrase(grammar, "#origin#")
    print(smoltingsummon)  # writeout get me in lil shid
    
    
if __name__ == '__main__':
    main()
