import discord
import asyncio
import re
import os, random, time
import locale
import threading

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
    game = discord.Game("4금융 | 투자증권")
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
                #raise ValueError #탈출
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
            #raise ValueError
        msg[1] = int(msg[1])
        if not ID in idA or moneyA[idA.index(ID)] - int(msg[1]) < 0: #등록된 ID가 아니거나 돈이 부족하면
            embed = discord.Embed(title='혹시 거지신가요?', description='아쉽네요, 보유하신 잔고가 부족하거나 저희 회원이 아니에요.', color=0xFF0000)
            await message.channel.send(embed=embed)
            #raise ValueError #탈출
        moneyA[idA.index(ID)] -= msg[1]
        give = random.randrange(1,5)

        await asyncio.sleep(0)
        if give % 2 == 0:

            #moneyA[idA.index(ID)] *= give
            moneyA[idA.index(ID)] += give * msg[1]
            money11 = moneyA[idA.index(ID)]
            msg22 = '**{}님 '.format(message.author.name) + f'배팅에 성공하셨습니다. \n\n 잔고: {money11:,}원**'
            #msg22 = '**{}님 '.format(message.author.name) + str(give) + f'배 배팅에 성공하셨습니다. \n\n 잔고: {money11:,}원**'
            #await message.channel.send('{}님'.format(message.author.name)+ f' 축하드려요, 배팅에 성공하셨습니다. \n\n 잔고: {money11:,}원')
            embed = discord.Embed(title='축하드립니다!', description=msg22, color=0x008B8B)
            await message.channel.send(embed=embed)
            #raise ValueError

        elif give % 2 != 0:
            money78 = moneyA[idA.index(ID)]
            msg22 = '**{}님 '.format(message.author.name) + f'아쉽네요, 배팅에 실패 하셨습니다.\n\n 잔고: {money78:,}원**'
            # await message.channel.send('{}님'.format(message.author.name)+ f' 축하드려요, 배팅에 성공하셨습니다. \n\n 잔고: {money11:,}원')
            embed = discord.Embed(title='아쉬워요.', description=msg22, color=0xDAA520)
            await message.channel.send(embed=embed)
            #raise ValueError

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
            embed = discord.Embed(title='거지신가요?', description='돈이 부족합니다.', color=0xFF0000)
            await message.channel.send(embed=embed)
            #raise ValueError
        give = random.randrange(2,10)
       
        #await count.edit(content = '만약 성공하면 건 돈의 '+str(give)+"배 를 얻어요")
        await asyncio.sleep(0.3)
        if give % 2 == 0:

            #moneyA[idA.index(ID)]*= give*msg[1]
            moneyA[idA.index(ID)] *= give
            money13 = moneyA[idA.index(ID)]
            msg33 = '**{}님 '.format(message.author.name) + str(give) + f'배 올인을 성공하셨습니다. \n\n 잔고: {money13:,}원**'
            # await message.channel.send('{}님'.format(message.author.name)+ f' 축하드려요, 배팅에 성공하셨습니다. \n\n 잔고: {money11:,}원')
            embed = discord.Embed(title='축하드립니다!', description=msg33, color=0x008B8B)
            await message.channel.send(embed=embed)
            #raise ValueError

        elif give % 2 != 0:
            moneyA[idA.index(ID)] = 0
            await asyncio.sleep(0)
            money15 = 0;
            money15 = moneyA[idA.index(ID)]

            msg33 = '**{}님 '.format(message.author.name) + f'에고.. 아쉽게 올인에 실패 하셨습니다.\n\n 잔고: {money15:,}원**'
            # await message.channel.send('{}님'.format(message.author.name)+ f' 축하드려요, 배팅에 성공하셨습니다. \n\n 잔고: {money11:,}원')
            embed = discord.Embed(title='아쉬워요.', description=msg33, color=0xDAA520)
            await message.channel.send(embed=embed)
            #raise ValueError

        f = open("UserData.txt", "w") #저장
        for i in range(0,len(idA),1):
            f.write(str(idA[i])+","+str(moneyA[i])+","+str(timeA[i])+"\n")
        f.close()

    if message.content == "!주식":
        stock1 = random.randrange(3000,7000)
        stock2 = random.randrange(70000,150000)
        stock3 = random.randrange(500, 2000)
        stock4 = random.randrange(100,300000)

        embed5 = discord.Embed(title="선효투자증권 주식 현황", description="선효투자증권의 주식 현황판을 보여드립니다. \n\n 5분마다 갱신됩니다.",
                               color=0x3bb9d8)
        embed5.add_field(name="선효대부", value=f'{stock1:,}원', inline=False)
        embed5.add_field(name="선효투자증권", value=f'{stock2:,}원', inline=False)
        embed5.add_field(name="급장흥신소", value=f'{stock3:,}원', inline=False)
        embed5.add_field(name="급장인신매매소", value=f'{stock4:,}원', inline=False)
        embed5.set_footer(text="* 연체시에는 상환시 까지 디스코드에서 대화, 보이스를 즐길 수 없도록 차단됩니다. 상환 시 즉시 해제됩니다.")
        await message.channel.send('', embed=embed5)


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

    if message.content == "!저축은행 대출":
        embed3 = discord.Embed(title="선효투자증권 대출 신청 안내", description="저희 선효투자증권은 저렴한 이자율과 만족스러운 승인율로 고객님꼐 다가갑니다.",
                              color=0xcf0707)
        embed3.add_field(name="이자율", value="45%", inline=True)
        embed3.add_field(name="최대 대출신청 가능 금액", value="5,000,000", inline=True)
        embed3.add_field(name="대출문의", value="@장티푸스환자/21", inline=True)
        embed3.add_field(name="대출신청", value="대출신청은 '!저축은행 대출신청 <금액>으로 가능합니다. ", inline=True)
        embed3.add_field(name="상환기간", value="최대 24시간으로 연장 불가능합니다.", inline=True)
        embed3.set_footer(text="* 연체시에는 상환시 까지 디스코드에서 대화, 보이스를 즐길 수 없도록 차단됩니다. 상환 시 즉시 해제됩니다.")
        await message.channel.send(embed=embed3)

    if message.content == "!저축은행 대출신청":
        embed = discord.Embed(title="선효투자증권 대출 신청 결과안내", description="저희 선효투자증권의 고객이 되어주셔서 대단히 감사드립니다.", color=0xcf0707)
        embed.add_field(name="적용 이자율", value="45%", inline=True)
        embed.add_field(name="대출신청금액", value="5,000,000", inline=True)
        embed.add_field(name="상환기간", value="24시간", inline=True)
        embed.add_field(name="상환금액", value="7,250,000원 * 이자포함", inline=True)
        embed.add_field(name="대출결과", value="지급이 완료되었습니다. 감사합니다.", inline=True)
        embed.set_footer(text="* 연체시에는 상환시 까지 디스코드에서 대화, 보이스를 즐길 수 없도록 차단됩니다. 상환 시 즉시 해제됩니다.")
        await message.channel.send(embed=embed)

        ID = str(message.author.id)
        TIME = int(time.time())
        if ID in idA:  # 만약 등록된 ID라면
            if TIME - timeA[idA.index(ID)] < 1:  # 1시간이 안 지났을 때
                embed2 = discord.Embed(title='어머, 상환이나 빨리 해주세요.', description='아직 진행중인 대출건이 존재합니다. \n\n 미 상환시 **채팅, 보이스 전부 금지 조치됩니다.**', color=0xFF0000)
                await message.channel.send(embed=embed2)
                #raise ValueError  # 탈출
            elif TIME - timeA[idA.index(ID)] >= 86400:  # 1시간이 지났을 때
                timeA[idA.index(ID)] = int(time.time())
        give = random.randrange(1, 2) * random.randrange(5000000, 5000001)  # 줄 돈
        if ID in idA:
            moneyA[idA.index(ID)] += give
            f = open("UserData.txt", "w")  # 저장
            for i in range(0, len(idA), 1):
                f.write(str(idA[i]) + "," + str(moneyA[i]) + "," + str(timeA[i]) + "\n")
            f.close()
        elif not ID in idA:
            idA.append(ID)
            moneyA.append(give)
            timeA.append(int(time.time()))
            f = open("UserData.txt", "w")  # 저장
            for i in range(0, len(idA), 1):
                f.write(str(idA[i]) + "," + str(moneyA[i]) + "," + str(timeA[i]) + "\n")
            f.close()

            #raise ValueError  # 탈출



client.run(os.environ['token'])
