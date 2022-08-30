import re

special = {
    "<",">","(",")","[","]","\\",".",",",";",":","@","\""
}

def validPath(string):
    sList = re.split('@', string)
    if len(sList)!=2: return False
    local = sList[0]
    if special.values() in local: return False
    domain = sList[1]
    return string[1] != "<" or string[-1]!=">" or "@" in string