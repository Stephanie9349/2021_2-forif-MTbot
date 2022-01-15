import discord
from RandomGame import *

class LMSBot(discord.Client):
    async def on_ready(self):
        print(f'Logged in as { self.user } (ID: { self.user.id })')

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return
        
        if '!술게임' in message.content:
            reply = randomGame()
            await message.reply(reply)



if __name__ == '__main__':
    token_file = open('token', 'r')
    token      = token_file.read()
    token_file.close()
    client     = LMSBot()
    client.run(token)