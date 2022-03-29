import requests
import random
import os

def secretWord(alpha, n, bool = False):
    g = random.randint(0, n-1)
    secret = alpha[g].lower()
    if bool == False: return secret
    return secret, g+1

def copyfix(aw, bool = False):
    av = ""
    for z in range(len(aw)):
        av += aw[z]
    aw = list(av)
    if bool == True: return av
    return av, aw

def getList(url):
    r = requests.get(url)
    urlf = open("temp.txt", "wb")
    urlf.write(r.content)
    urlf.close()
    urlf = open("temp.txt", "r")
    listi = urlf.readlines()
    for i in range(len(listi)):
        listi[i] = listi[i].replace("\n", "")
    urlf.close()
    os.remove("temp.txt")
    return listi

def ArrToStrSpaces(arr, stro = " "):
    stri = ""
    for i in range(len(arr)):
        stri += str(arr[i])
        if i != len(arr) - 1:
            stri += stro
    return stri

def nCopies(n, copy):
    res = []
    for _ in range(n):
        res.append(copy)
    return res
