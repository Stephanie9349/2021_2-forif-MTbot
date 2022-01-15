from AlcoholGames import *
import random

def randomGame(people):
    title = []
    for key in games:
        title.append(key)
    game = random.choice(title)
    text = '<'+game+'>\n'+games[game] + '\n'
    text += random.choice(people)+'부터 시작!'
    return text

#people.txt 읽어오기
f = open("people.txt",'r', encoding='UTF8')
data = f.read()
people = data.split(', ')
a= randomGame(people)
print(a)
f.close()