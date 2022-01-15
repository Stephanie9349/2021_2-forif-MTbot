import discord
import re
import registration
import randomPicker

class MTbot(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
    async def on_message(self, message):
        if re.match(r'^(!인원 \[)(\w+(, )*)*\w+\]$', message.content) != None:
            registration.registration(message)
            
        if message.content == '!돌림판':
            chosen = randomPicker.randomPicker(message)
            await message.reply(f'당첨된 사람은? {chosen}!', mention_author = True)
if __name__ == "__main__":
    token_file = open('token', 'r')
    token = token_file.read()
    token_file.close()
    client = MTbot()
    client.run(token)