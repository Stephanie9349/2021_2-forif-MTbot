import discord
import time
import re
import registration
import randomPicker
from RandomGame import *
from ProductRecommendation import recommend_product
class MTBot(discord.Client):
    async def on_ready(self):
        print(f'Logged in as { self.user } (ID: { self.user.id })')

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return
        
        if '!술게임' in message.content:
            reply = randomGame()
            await message.reply(reply)

        if '!최저가' in message.content:
            product = str(message.content).strip('!최저가 ')
            name, price, fee, link, thumbnail = recommend_product(product)
            embed = discord.Embed(title=f'{product} 최저가로 사러가기🛍', description=f'상품명: {name}\n판매가: {price}\n배송비: {fee}', color=0x00ff00, url=link)
            embed.set_thumbnail(url=thumbnail)
            await message.channel.send(embed=embed)
            
        if re.match(r'^(!인원 \[)(\w+(, )*)*\w+\]$', message.content) != None:
            registration.registration(message)
            
        if message.content == '!돌림판':
            chosen = randomPicker.randomPicker(message)
            await message.reply("당첨자는 3초 후에 공개됩니다!")
            time.sleep(3)
            await message.reply(f'당첨된 사람은? {chosen}!', mention_author = True)


if __name__ == '__main__':
    token_file = open('token', 'r')
    token = token_file.read()
    token_file.close()
    client = MTBot()
    client.run(token)