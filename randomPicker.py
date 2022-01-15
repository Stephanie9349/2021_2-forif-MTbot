import random

def randomPicker(message):
    peopleFile = open("people.txt", 'r')
    people = peopleFile.read().split(',')
    peopleFile.close()
    return random.choice(people)

    