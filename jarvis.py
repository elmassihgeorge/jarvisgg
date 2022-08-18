# bot.py
import os

import discord
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!jarvis "):
        tag = message.content.split("!jarvis ")[1]
        url = "https://smashdata.gg/smash/ultimate/player/" + tag
        driver.get(url)
        try:
            elem = driver.find_element(By.CSS_SELECTOR, '#players-tab > table > tbody > tr:nth-child(2) > td:nth-child(1) > a')
            elem.click()
        finally:
            driver.save_screenshot('./image.png')
            await message.channel.send('Jarvis, pull up the smashdata')
            #await message.channel.send(file=discord.File('tony-stark-jarvis.gif'))
            await message.channel.send(file=discord.File('./image.png'))

        
client.run(TOKEN)