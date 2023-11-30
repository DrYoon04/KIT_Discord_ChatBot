
import random
import discord
from discord import app_commands
from discord.ext import commands
from module import food
from module import chatgpt as gpt
import base64

file_path = "discord_api_key_base64.txt"

with open(file_path, 'r') as file:
    # 파일 내용 읽기
    encoded_content = file.read()

    # base64 디코딩
    decoded_content = base64.b64decode(encoded_content)
    decoded_string = decoded_content.decode('utf-8')

#paramètres
intents = discord.Intents.all()
client = discord.Client(intents = intents)
activity = discord.Activity(type = discord.ActivityType.streaming, name="name", url = "twitch_url")
tree = app_commands.CommandTree(client)
bot = commands.Bot(intents=intents, command_prefix="!")
blue = discord.Color.from_rgb(0, 0, 200)
red = discord.Color.from_rgb(200, 0, 0)
green = discord.Color.from_rgb(0, 200, 0)
discord_blue = discord.Color.from_rgb(84, 102, 244)

guild=discord.Object(id=951082793037873212)

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=951082793037873212))
    print('Ready!')

@tree.command(name='핑',description='핑!',guild=guild)
async def first_command(interaction):
    await interaction.response.send_message('퐁')

@tree.command(name='기숙사',description='기숙사 메뉴을 알 수 있습니다(푸름, 오름1, 오름3, 분식당, 교직원식당, 학생식당)',guild=guild)
async def menu(interaction: discord.Integration,이름 : str):
    embed  = discord.Embed(title = '😝오늘의 식단😝', description = food.get_menu_data(이름), colour=0x3498DB)
    await interaction.response.send_message(embed = embed)


@tree.command(name='주사위',description='주사위가 조금... 이상한거 같습니다..!',guild=guild)
async def rsp(interaction: discord.Integration,넣을숫자 :int):
    pick = random.randint(1,넣을숫자)
    embed = discord.Embed(title='결과!',description=pick,colour=0x3498DB)
    await interaction.response.send_message(embed = embed)

@tree.command(name='메롱',description='😝',guild=guild)
async def wow(interaction : discord.Integration):
    embed = discord.Embed(title='😝',description='😝',colour=0x3498DB)
    await interaction.response.send_message(embed = embed)


@tree.command(name='chat', description='만능 명령어를 경험해보세요',guild=guild)
async def chat(interaction: discord.Integration,질문사항 : str):
    embed1 = discord.Embed(title = "GPT", description = "답변생성중...",colour=0x3498DB)
    await interaction.response.send_message(embed = embed1)
    embed = discord.Embed(title = "GPT", description =gpt.chat(질문사항) ,colour=0x3498DB)
    await interaction.response.send_message(embed = embed)
    
client.run(decoded_string)