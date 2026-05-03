
import os

import discord
from dotenv import load_dotenv

import asyncio
import re

import tools
import sw
import inf
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
        ct = api_cnt.roll_dice(sys, cmd)
        if ct:
            await message.channel.send(ct)
    
    if message.content.startswith('.'):
        pattern_inf = r"\.(\d+)wd(\d+)?"
        match_inf = re.search(pattern_inf, message.content, re.IGNORECASE)
        if match_inf:
            ct = inf.roll_inf(message.content)
            if ct:
                await message.channel.send(ct)


token = os.environ.get('TOKEN')
client.run(token)
    



        


        
        

