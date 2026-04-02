
import os

import discord
from dotenv import load_dotenv

import asyncio
import re

import tools
import sw
import api_cnt

load_dotenv()
token = os.environ.get('TOKEN')
client = discord.Client(intents=discord.Intents.all())


@client.event
# 當機器人完成啟動時在終端機顯示提示訊息
async def on_ready():
    print(f'目前登入身份：{client.user}')

@client.event
async def on_message(message: discord.message.Message):
    currentWorkLoop = asyncio.get_event_loop()
    if message.author == client.user:
        return
    #if message.content.startswith('!d'):
        #ctx = message.content.split(' ')[1]
        #send = tools.xndmplus(ctx)
        #if send:
            #await message.channel.send(send)
    if message.content.startswith('d66'):
        #await message.channel.send(tools.d66())
        pass #until fully sub
    
    if message.content.startswith('!'):
        ctx = message.content.split(' ',1)
        sys,cmd = ctx[0].lstrip('!'), ctx[1]
        
        #await message.channel.send(sw.comment_parse(cmd))
        await message.channel.send(api_cnt.roll_dice(sys, cmd))


        
    






token = os.environ.get('TOKEN')
client.run(token)
    



        


        
        

