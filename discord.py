import discord
from ProductRecommendation import recommend_product
class LMSBot(discord.Client):
    async def on_ready(self):
        print(f'Logged in as { self.user } (ID: { self.user.id })')

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return
        
        if '!최저가' in message.content:
            product = str(message.content).strip('!최저가 ')
            name, price, fee, link, thumbnail = recommend_product(product)
            embed = discord.Embed(title=f'{product} 최저가로 사러가기🛍', description=f'상품명: {name}\n판매가: {price}\n배송비: {fee}', color=0x00ff00, url=link)
            embed.set_thumbnail(url=thumbnail)
            await message.channel.send(embed=embed)


if __name__ == '__main__':
    token_file = open('token', 'r')
    token      = token_file.read()
    token_file.close()
    client     = LMSBot()
    client.run(token)
