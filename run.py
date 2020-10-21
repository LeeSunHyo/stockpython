import discord
import asyncio
import re
import os, random, time
import locale

client = discord.Client()

#사용하는 변수들
idA, moneyA, timeA, give, ID, TIME,member =  [], [], [], 0, 0, 0,[]
ment = ["님의 확률을 계산중에 있어요, 잠시만 기다려주세요.", "님의 확률을 계산중에 있어요, 잠시만 기다려주세요.", "님의 확률을 계산중에 있어요, 잠시만 기다려주세요."]

try: #만약 파일이 없으면 새로 만듦
    f = open("UserData.txt", "r")
except:
    f = open("UserData.txt", "w")
    f.close()
    f = open("UserData.txt", "r")
while True: #유저들 데이터를 읽음 데이터 형식 : 유저ID,가지고 있는 돈,돈받은 시간
    line = f.readline()
    if not line: break
    line = line.split(",")
    idA.append(line[0])
    moneyA.append(int(line[1]))
    timeA.append(int(line[2]))
f.close()

@client.event
async def on_ready(): #봇이 켜지면
    print("봇 아이디: ", client.user.id)
    print("봇 준비 완료")
    game = discord.Game("현재 원금 회수 중")
    await client.change_presence(status=discord.Status.online, activity=game)

@client.event
async def on_message(message):
    if message.content == "!ㄷㅂㄱ":
        ID = str(message.author.id)
        TIME = int(time.time())
        if ID in idA: #만약 등록된 ID라면
            if TIME - timeA[idA.index(ID)] < 1: #1시간이 안 지났을 때
                embed = discord.Embed(title='욕심이 너무 과해요.', description='1분마다 지원금을 받을 수 있습니다.', color=0xFF0000)
                await message.channel.send(embed=embed)
                raise ValueError #탈출
            elif TIME - timeA[idA.index(ID)] >= 1: #1시간이 지났을 때
                timeA[idA.index(ID)] = int(time.time())
        give = random.randrange(1,2)*random.randrange(1000,5000) # 줄 돈
        if ID in idA:
            moneyA[idA.index(ID)] += give
            f = open("UserData.txt", "w") #저장
            for i in range(0,len(idA),1):
                f.write(str(idA[i])+","+str(moneyA[i])+","+str(timeA[i])+"\n")
            f.close()
        elif not ID in idA:
            idA.append(ID)
            moneyA.append(give)
            timeA.append(int(time.time()))
            f = open("UserData.txt", "w") #저장
            for i in range(0,len(idA),1):
                f.write(str(idA[i])+","+str(moneyA[i])+","+str(timeA[i])+"\n")
            f.close()
            money1 = moneyA[idA.index(ID)]
        msg = str(give)+"원의 지원금을 지급하였습니다. \n\n 잔고: "+str(moneyA[idA.index(ID)])+"원"
        embed = discord.Embed(title='지원금을 지급하였습니다!', description=msg, color=0x00FF00)
        await message.channel.send(embed=embed)

    if message.content.startswith("!ㄷㅂ"):
        ID = str(message.author.id)
        msg = message.content.split()
        if msg[1].isdecimal() == False: #만약 숫자가 아니라면
            embed = discord.Embed(title='경고!', description='숫자만 입력해 주세요!', color=0xFF0000)
            await message.channel.send(embed=embed)
            raise ValueError
        msg[1] = int(msg[1])
        if not ID in idA or moneyA[idA.index(ID)] - int(msg[1]) < 0: #등록된 ID가 아니거나 돈이 부족하면
            embed = discord.Embed(title='경고!', description='아쉽네요, 보유하신 잔고가 부족하거나 저희 회원이 아니에요.', color=0xFF0000)
            await message.channel.send(embed=embed)
            raise ValueError #탈출
        moneyA[idA.index(ID)] -= msg[1]
        give = random.randrange(1,11)


        await asyncio.sleep(0)
        if give % 2 == 0:
            moneyA[idA.index(ID)] * give
            await asyncio.sleep(0)
            rank2, rankB = "", []
            money11 = 0;
            money11 = moneyA[idA.index(ID)]
            msg22 = '**{}님 '.format(message.author.name)+ str(give) + f'배 배팅에 성공하셨습니다. \n\n 잔고: {money11:,}원**'
            #await message.channel.send('{}님'.format(message.author.name)+ f' 축하드려요, 배팅에 성공하셨습니다. \n\n 잔고: {money11:,}원')
            embed = discord.Embed(title='축하드립니다!', description=msg22, color=0x008B8B)
            await message.channel.send(embed=embed)

        elif give % 2 != 0:
            money11 = moneyA[idA.index(ID)]
            msg22 = '**{}님 '.format(message.author.name) + f'아쉽네요, 배팅에 실패 하셨습니다.\n\n 잔고: {money11:,}원**'
            # await message.channel.send('{}님'.format(message.author.name)+ f' 축하드려요, 배팅에 성공하셨습니다. \n\n 잔고: {money11:,}원')
            embed = discord.Embed(title='아쉬워요.', description=msg22, color=0xDAA520)
            await message.channel.send(embed=embed)

        f = open("UserData.txt", "w") #저장
        for i in range(0,len(idA),1):
            f.write(str(idA[i])+","+str(moneyA[i])+","+str(timeA[i])+"\n")
        f.close()

    if message.content == "!돈":
        ID = str(message.author.id)
        if ID in idA: #만약 등록된 ID라면
            money12 = 0;
            money12 = moneyA[idA.index(ID)]
            embed = discord.Embed(title='내 자산', description=f"{money12:,}원", color=0x118811)
            await message.channel.send(embed=embed)
        elif not ID in idA: #등록된 ID가 아니라면
            embed = discord.Embed(title='', description="도박 시스템을 한번도 이용해보지 않으셨네요. !ㄷㅂㄱ를 통해 지원금을 받고 이용해보세요.", color=0x118811)
            await message.channel.send(embed=embed)

    if message.content == "!도움말":
        embed = discord.Embed(title="도움말", description="**이 봇은 장티푸스환자가 개발하였습니다. 아직 많이 불안정합니다. 꼬우면 쓰지 마십쇼.**", color=0xffffff)
        embed.add_field(name='**도움**', value='**이용이 처음이신 분들을 위한 도움말 페이지입니다.**', inline=False)
        embed.add_field(name='**Utility**', value='**`!돈 - 보유한 자산을 보여줍니다.`, `!ㄷㅂㄱ - 지원금을 받습니다.`, `!도박 <금액>`, `!올인`, `!랭킹`**', inline = False)
        await message.channel.send('', embed=embed)

    if message.content == "!올인":
        ID = str(message.author.id)
        if not ID in idA or moneyA[idA.index(ID)] <= 0: #만약 돈이 부족하면
            embed = discord.Embed(title='', description='돈이 부족합니다.', color=0xFF0000)
            await message.channel.send(embed=embed)
            raise ValueError
        give = random.randrange(2,10)
        count = await message.channel.send('**{}님'.format(message.author.name) + "의 확률을 계산중에 있어요, 잠시만 기다려주세요.")
        for i in range(0,2):
            await count.edit(content = ment[0])
            await asyncio.sleep(0)
            await count.edit(content = ment[1])
            await asyncio.sleep(0)
            await count.edit(content = ment[2])
            await asyncio.sleep(0)
        #await count.edit(content = '만약 성공하면 건 돈의 '+str(give)+"배 를 얻어요")
        await asyncio.sleep(0)
        if give % 2 == 0:
            moneyA[idA.index(ID)]*= give
            await asyncio.sleep(0)
            money13 = 0;
            money13 = moneyA[idA.index(ID)]

            msg33 = '**{}님 '.format(message.author.name) + str(give) + f'배 올인을 성공하셨습니다. \n\n 잔고: {money13:,}원**'
            # await message.channel.send('{}님'.format(message.author.name)+ f' 축하드려요, 배팅에 성공하셨습니다. \n\n 잔고: {money11:,}원')
            embed = discord.Embed(title='축하드립니다!', description=msg33, color=0x008B8B)
            await message.channel.send(embed=embed)

            #0xDAA520


        elif give % 2 != 0:
            moneyA[idA.index(ID)] = 0
            await asyncio.sleep(0)
            money15 = 0;
            money15 = moneyA[idA.index(ID)]

            msg33 = '**{}님 '.format(message.author.name) + f'에고.. 아쉽게 올인에 실패 하셨습니다.\n\n 잔고: {money15:,}원**'
            # await message.channel.send('{}님'.format(message.author.name)+ f' 축하드려요, 배팅에 성공하셨습니다. \n\n 잔고: {money11:,}원')
            embed = discord.Embed(title='아쉬워요.', description=msg33, color=0xDAA520)
            await message.channel.send(embed=embed)

        f = open("UserData.txt", "w") #저장
        for i in range(0,len(idA),1):
            f.write(str(idA[i])+","+str(moneyA[i])+","+str(timeA[i])+"\n")
        f.close()
    
    if message.content == "!랭킹":
        rank, rankA = "", []
        for i in range(0,len(idA)): rankA.append([idA[i], moneyA[i]])
        rankA = sorted(rankA, reverse = True, key = lambda x: x[1]) #많은 순으로 정렬
        for i in range(0,10): #10위 까지만 출력
            try:
                money3 = rankA[i][1]
                rank += str(i+1)+"위 <@"+rankA[i][0]+"> : "+f"{money3:,}원"+"\n"
            except:
                break
        embed = discord.Embed(title='서버 랭킹', description=rank, color=0xd8aa2d)
        await message.channel.send(embed=embed)

client.run(os.environ['token'])
