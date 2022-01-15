from AlcoholGames import *
import random

def randomGame():
    #people.txt 읽어오기
    f = open("people.txt",'r')
    data = f.read()
    people = data.split(', ')
    f.close()

    #게임 제목들 가져오기
    title = []
    for key in games:
        title.append(key)

    #게임 제목과 설명
    game = random.choice(title)
    text = '<'+game+'>\n'+games[game] + '\n'

    #술래 지목해서 시작
    text += random.choice(people)+'부터 시작!'
    return text