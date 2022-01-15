def registration(message):
    f = open("people.txt", 'w')
    f.write(message.content[5:-1])
    f.close()