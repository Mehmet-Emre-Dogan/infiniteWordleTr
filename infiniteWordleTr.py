import sys
from json import load
from random import randint
from colorama import init as beginColoring
from colorama import Fore, Style
import ctypes
from collections import defaultdict

wordArr = []

ctypes.windll.kernel32.SetConsoleTitleW("Sonsuz Wordle Türkçe")
with open("config.json", "r", encoding="utf-8") as fil:
    configDict = load(fil)
    DEBUG = configDict["DEBUG"]
    MAX_TRIALS = configDict["MAX_TRIALS"]

with open("words.json", "r", encoding="utf-8") as fil:
    wordArr = load(fil)["data"]
    WORD_COU = len(wordArr)

beginColoring()
print("Sonsuz Wordle Türkçe oyununa hoş geldiniz! Oyundan sıkılınca CTRL^C ye basın (keyboard interrupt)")
print(f"--> Konfigürasyon >> DEBUG: {DEBUG}; Maksimum tahmin limiti: {MAX_TRIALS}; Yüklü kelime sayısı: {WORD_COU}")

def checkWord(userWord, selectedWord):
    colorPatternArr = []
    # Get th number of occurence each letter
    letters = defaultdict(int)
    for letter in selectedWord:
        letters[letter] += 1
    
    for i, (letterUser, letterSelected) in enumerate(zip(userWord, selectedWord)):
        if DEBUG:
            print(f"{i} {letterUser} {letterSelected}")

        if letterUser == letterSelected:
            colorPatternArr.append(Fore.GREEN)
            letters[letterUser] -= 1
        elif letters[letterUser]:
            colorPatternArr.append(Fore.YELLOW)
            letters[letterUser] -= 1
        else:
            colorPatternArr.append(Fore.RED)
        
    for (letter, color) in zip(userWord, colorPatternArr):
        print(color, end='')
        print(letter + " ", end='')
    print(Style.RESET_ALL)

    if selectedWord == userWord:
        return True
    
def play(selectedWord):
    global wordArr
    for i in range(1, MAX_TRIALS + 1):
        guess = ""
        while True:
            guess = input(f"{i}. Tahmininiz:\n-> ")
            if guess in wordArr:
                break
            else:
                print("Bu kelime listede yok. Tekrar tahmin yapın.")
        if checkWord(guess, selectedWord):
            return True
    return False

while True:
    try:
        print("="*50)
        print("--> Yeni tur!")
        word = wordArr[randint(0, WORD_COU-1)]
        if play(word):
            print("Kazandınız")
            print(f"{word} kelimesini başarıyla buldunuz.")
        else:
            print("Kaybettiniz")
            print(f"Seçilen kelime: {word} idi.")
    except KeyboardInterrupt:
        sys.exit()