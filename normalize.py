import re

def normalize(name: str) -> str:
    CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщьыъэюяґєії'
    TRANSLATION = ['a','b','v','g','d','e','e','zh','z',
                   'i','j','k','l','m','n','o','p','r',
                   's','t','u','f','kh','ts','ch','sh',
                   'shch','','y','','e','u','ja','g','e','i','y']  
     
    TRANS= {}
    for c, l in zip(list(CYRILLIC_SYMBOLS), TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()
    trans_name = name.translate(TRANS)
    trans_name = re.sub(r'\W', '_', trans_name)
    return trans_name
