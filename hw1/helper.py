import re

special = {
    "<",">","(",")","[","]","\\",".",",",";",":","@","\""
}

def validPath(string):
    if string[-1] != ">": return False
    sList = re.split('[<@>]', string)
    sList = list(filter(None,sList))
    if len(sList)!=2: return False
    local = sList[0]
    for s in special:
        if s in local: return False
    domain = sList[1]
    return string[1] != "<" or string[-1]!=">" or "@" in string