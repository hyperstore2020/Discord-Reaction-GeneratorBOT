import discord 
from discord.ext import commands 
import json 
import os
import random
import datetime

github_link = "https://github.com/4-04/Discord-Reaction-GeneratorBOT/"

#opening the config.json file and loading the data.
if os.path.isfile("config.json"):
    with open("config.json") as f:
        data = json.load(f)
        try:
            #access the data
            token = data["token"]
            prefix = data["prefix"]
            name = data["name"]
            color = data['hex_color']
            color = color.replace("#", "")
            if color.startswith("0x"):
                color = int(color, 16)
            else:
                color = int("0x"+str(color), 16)
        except KeyError:
            raise KeyError(f"The config.json file is broken, please re-download it from my github page - ({github_link})")
else:
    raise IOError(f"Could not find the config.json file! please re-download it from my github page - ({github_link})")
    

#variables
file_dictionary = {}

file_cooldown_dictionary = {} 

active_dictionary = {}

where_dictionary = {}


error_color = 0xfc1703
    
#creating the  bot object

client = commands.Bot(command_prefix=prefix)
client.remove_command("help")
@client.event
async def on_ready():
    print("Bot is now running.\n")
    print(f"[{prefix}help for a list of commands]")
    
@client.command()
async def help(ctx):
    embed = discord.Embed(title=f"{name} - help command")
    embed.add_field(name="Start", value=f"{prefix}start (gen type) - Will load the gen, requires administrator.")
    embed.add_field(name="Stock", value=f"{prefix}stock (type) (file, optional) - Will show the available stock from that type, alternatively from that specific file (optional)")
    embed.add_field(name="restock", value=f"{prefix}restock (folder name) (lines, seperated by a comma) - Will append all the lines to that file in that folder, requires administraotr.")
    
    await ctx.channel.send(embed=embed)
    
#load the bot
@client.command()
@commands.has_permissions(administrator=True)
async def start(ctx, gen_type : str):
    global file_dictionary, file_cooldown_dictionary, active_dictionary, where_dictionary
    if gen_type:
        folder_name = "gen_"+str(gen_type)
        files = os.listdir(f"{folder_name}/")
        reactions_to_add = []
        
        if files:
            embed = discord.Embed(title=f"{name} - {gen_type}")
            json_dir = os.listdir("data/")
            for f in files:
                if f.endswith(".txt"):
                    file_name = f.replace(".txt", "")
                    lines = open(f"{folder_name}\\{f}", encoding="utf8").read().splitlines()
                    
                    emoji_id = str(lines[0])
                    cooldown = int(lines[1])
                    where_dictionary[file_name] = folder_name
                    
                    
                    reactions_to_add.append(emoji_id)
                    
                    file_dictionary[emoji_id] = file_name 
                    file_cooldown_dictionary[file_name] = cooldown
                    
                    embed.add_field(name=file_name, value=f"React with {emoji_id} to get sent a **{file_name}!** *[Cooldown: {cooldown} seconds]*", inline=False)
                    if file_name+".json" not in json_dir:
                        with open(f"data\\{file_name}.json", "w+") as f:
                            f.write(r"{}")
        
            msg = await ctx.channel.send(embed=embed)
            for emoji in reactions_to_add:
                await msg.add_reaction(emoji)
                
            active_dictionary[msg.id] = True
        
            
@client.command()
@commands.has_permissions(administrator=True)
async def restock(ctx, fo, types, *, lines=None):
    types = types.lower()
    msg = str(ctx.message.content).replace(f'{prefix}restock', '').replace(types, '').replace(fo, '').strip()
    accs = msg.split(',')
    try:
        fo = "gen_"+fo+"/"
        with open(fo+types+".txt", "a") as f:
            for line in accs:
                f.write(line+"\n")
        embed = discord.Embed(title="Success", description=f"Successfully added a total of +{len(accs)} lines to {types}.txt!", color=color)
        await ctx.send(embed=embed)
        return
    except FileNotFoundError:
        embed = discord.Embed(title="Error", description=f"Invalid type '{types}'! You may try again with a different type.", color=error_color)
        await ctx.send(embed=embed)
        return 
    except Exception as e:
        print(f"({e})")
        embed = discord.Embed(title="Error", description="An eror has accured. You may try agian.", color=error_color)
        await ctx.send(embed=embed)
        return
            

@client.command()
async def stock(ctx, folder_name, file_name=None):
    embed = discord.Embed(
        title=f"{name} - Stock Command - Stock of {folder_name}." ,
        color = color
    )
    folder_name = "gen_"+folder_name
    if file_name == None:
        for f in os.listdir(folder_name):
            embed.add_field(name=f"{f.replace('.txt', '')}", value=str(int(sum(1 for line in open(f"{folder_name}/{f}")))-2)+"x"+" lines.", inline=False)
    else:
        if not file_name.endswith(".txt"):
            file_name = file_name+".txt"
        for f in os.listdir(folder_name):
            if f.lower() == file_name.lower():
                embed.add_field(name=f"{f.replace('.txt', '')}", value=str(int(sum(1 for line in open(f"{folder_name}/{f}")))-2)+"x", inline=False)
                break
    
    await ctx.send(embed=embed)
    
    
@client.event
async def on_reaction_add(reaction, user):
    if user.id == client.user.id:
        return
    if not reaction.message.id in active_dictionary:
        return
    else:
        if active_dictionary[reaction.message.id] == False:
            return

    await reaction.remove(user)
    reaction_name = file_dictionary[str(reaction)]
    cooldown = file_cooldown_dictionary[reaction_name]
    where = where_dictionary[reaction_name]
    
    with open(f"data\\{reaction_name}.json") as f:
        last_uses = json.load(f)

    if str(user.id) not in last_uses:
        fil = open(f"{where}/{reaction_name}.txt").read().splitlines()
        fil.pop(0)
        fil.pop(1)
        line = random.choice(fil)
            
        embed = discord.Embed(
            title=reaction_name,
            description=line,
            timestamp = datetime.datetime.utcnow(),
            color = color
        )
        embed.set_footer(text="This bot was developed by (https://github.com/4-04/) - This message was generated: ")
        await user.send(embed=embed)
        now = datetime.datetime.now()
        now.strftime("%d/%m/%Y %H:%M:%S")
        print(f"{user} generated a {reaction_name} at {now}. Content sent: {line}")
        
        past_date = datetime.datetime(year=2020, month=1, day=1)
        time = (datetime.datetime.now() - past_date).total_seconds()
        last_uses[str(user.id)] = int(time)
        with open(f"data\\{reaction_name}.json", "w") as f:
            json.dump(last_uses, f, indent = 4)
        return
    else:
        last_used = last_uses[str(user.id)]
        past_date = datetime.datetime(year=2020, month=1, day=1)
        time_now = (datetime.datetime.now() - past_date).total_seconds()
        diff = time_now - last_used
        if int(diff) >= cooldown:
            fil = open(f"{where}/{reaction_name}.txt").read().splitlines()
            fil.pop(0)
            fil.pop(1)
            line = random.choice(fil)
            embed = discord.Embed(
                title=reaction_name,
                description=line,
                timestamp = datetime.datetime.utcnow(),
                color = color
            )
            embed.set_footer(text="This bot was developed by (https://github.com/4-04/) - This message was generated: ")
            await user.send(embed=embed)
            now = datetime.datetime.now()
            now.strftime("%d/%m/%Y %H:%M:%S")
            print(f"{user} generated a {reaction_name} at {now}. Content sent: {line}")
            
            past_date = datetime.datetime(year=2020, month=1, day=1)
            time = (datetime.datetime.now() - past_date).total_seconds()
            last_uses[str(user.id)] = int(time)
            with open(f"data\\{reaction_name}.json", "w") as f:
                json.dump(last_uses, f, indent = 4)
            return
        else:
            embed = discord.Embed(
                title="Error", 
                color = error_color,
                description=f"The cooldown for generating a '{reaction_name}' is {cooldown} seconds!"
            )
            
            await user.send(embed=embed)
            return


#attempting to run the bot
try:
    client.run(token)
except:
    print("The token (in the config.json file) is invalid! You may try again with a different token.")
