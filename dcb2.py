import discord
import openpyxl
import datetime
import os


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# 엑셀 파일 생성 또는 불러오기
if not os.path.exists('건의사항.xlsx'):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = '건의사항'
    ws.append(['일시', '유저명', '건의사항'])
    wb.save('건의사항.xlsx')
else:
    wb = openpyxl.load_workbook('건의사항.xlsx')
    ws = wb.active

# 클라이언트 이벤트
@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == '/건의사항':
        await message.channel.send("말씀하십시오")

        def check(m):
            return m.author == message.author and m.channel == message.channel

        try:
            msg = await client.wait_for('message', check=check, timeout=30.0)
            today = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ws.append([today, message.author.name, msg.content])
            wb.save('건의사항.xlsx')
            await message.channel.send("접수되었습니다")
        except:
            await message.channel.send("시간이 초과되어 건의사항이 접수되지 않았습니다.")

    elif message.content == '서령고등학교 의견수렴부입니다!':
        await message.channel.send("안녕하세요, 의견수렴부입니다!")

# 가동
access_token = os.environ["BOT_TOKEN"]
client.run(access_token)
