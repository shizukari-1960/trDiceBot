
import os

import discord
from dotenv import load_dotenv

import asyncio
import re
from random import choice, randint

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
    if message.author.bot:
        return
    if message.guild.id == 1499348320861028442:
        return
    if message.content.startswith('d66'):
        await message.channel.send(str(randint(1,6)) + str(randint(1,6)))
        return
    
    if message.channel.id == 1508886760686620742:
        await message.author.ban(delete_message_days= 1, reason='Hacked account.')
    
    if message.content.startswith('.'):
        pattern_inf = r"\.(\d+)wd(\d+)?"
        match_inf = re.match(pattern_inf, message.content, re.IGNORECASE)
        if match_inf:
            ct = await inf.roll_inf(message.content)
            await message.channel.send(ct)
            return
        ctx = message.content.split(' ',1)
        sys,cmd = ctx[0].lstrip('.'), ctx[1]
        
        #await message.channel.send(sw.comment_parse(cmd)) abandon
        ct = await api_cnt.roll_dice_async(sys, cmd)
        if ct:
            await message.channel.send(ct)
            return
        
        
    pattern_normal_d = r'(\d+)d(\d+)'
    pattern_multiply_d = r'x(\d+)'
    match_nd = re.match(pattern_normal_d, message.content, re.IGNORECASE)
    match_md = re.match(pattern_multiply_d, message.content, re.IGNORECASE)
    if match_nd or match_md:
        ct = await api_cnt.roll_dice_async('sw', message.content)
        if ct:
            await message.channel.send(ct)
        return
    
    if message.content.startswith('隨機'):
        ct = message.content.split(' ')
        ct.pop(0)
        await message.channel.send(choice(ct))
        return
    

        
            


token = os.environ.get('TOKEN')
client.run(token)
    



        


        
        

