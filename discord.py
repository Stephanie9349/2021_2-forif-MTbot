import discord
from ProductRecommendation import recommend_product
class LMSBot(discord.Client):
    async def on_ready(self):
        print(f'Logged in as { self.user } (ID: { self.user.id })')

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return
        
        if '!최저가' in message.content:
            recommend_product(str(message.content).strip('!최저가 '))
            result = open("recommended_product.txt", 'r')
            reply = ''
            for line in result.readlines():
                reply += line
            await message.reply(reply, mention_author = False)

if __name__ == '__main__':
    token_file = open('token', 'r')
    token      = token_file.read()
    token_file.close()
    client     = LMSBot()
    client.run(token)
