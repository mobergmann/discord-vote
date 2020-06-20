"""
ith the bot you can create a poll using emojis to vote by reacting with them

the command to create a new poll is:
!vote | !poll {a questionable topic to discuss with your friends} [Option A]{optional emoji to replace the current one} [Option B] ...
"""

import datetime
import discord
from emoji import UNICODE_EMOJI
import json
import re

pattern_command = re.compile("!(?:vote|poll) {([\w ]+)} ((?:\[[\w ]+\](?:{[^}]*})? ?){2,10})")
pattern_option = re.compile("(\[[\w ]+\])({[^}]*})?")
pattern_emoji = re.compile("")

"""default emojis"""
predefined_emojis = [
    "0️⃣",
    "1️⃣",
    "2️⃣",
    "3️⃣",
    "4️⃣",
    "5️⃣",
    "6️⃣",
    "7️⃣",
    "8️⃣",
    "9️⃣",
    "🔟"
]

predefined_status = [
    "rig ballot papers",
    "buying votes from china",
    "buying votes from india",
    "buying votes from russia",
    "retuning!!!",
    "calculating next outcome",
    "preparing retuning",
    "preparing next outcome",
    "adding votes to win my bet",
    "paying bribe",
    "manipulate election",
    "overthinking last bet"
]

def checkEmoji(emoji_to_check: str, position: int, server_emojis: list) -> str:
    """
    checks if the emoji is a valid emoji. if not returns a default emoji, based on the current position.
    TODO add doc
    """

    if emoji_to_check in UNICODE_EMOJI: # if the given emoji is not in the default emoji set
        return emoji_to_check
        
    if isServerEmoji(emoji_to_check, server_emojis): # if also not an custom server emoji
        return emoji_to_check

    return predefined_emojis[position] # set the default emoji
    
    

def isServerEmoji(emoji_to_check: str, server_emojis: list) -> bool: 
    for server_emoji in server_emojis:
        constructed_emoji = "<:" + server_emoji.name + ":" + str(server_emoji.id) + ">"
        constructed_emoji_animated = "<a:" + server_emoji.name + ":" + str(server_emoji.id) + ">"
        if emoji_to_check == constructed_emoji or emoji_to_check == constructed_emoji_animated:
            return True
    return False

def extractParams(input: str):
    # TODO doc

    tmp_list_1 = re.findall(pattern_command, input)
    match = tmp_list_1[0]

    title = match[0]
    tmp = match[1]
    pre_options = re.findall(pattern_option, tmp)

    option_titles = []
    option_emojis = []

    options = []
    for option in pre_options:
        name = option[0][1 : len(option[0])-1]
        emoji = option[1][1 : len(option[1])-1]
        options.append((name, emoji))

    return title, options

def generateEmbed(title: str, author: discord.User, options: list):
    # TODO doc

    embed = discord.Embed(
        title = title,
        # description = "desc",
        timestamp = datetime.datetime.now())
    embed.set_author(
        name=author.display_name, 
        icon_url=author.avatar_url)

    for option in options:
        embed.add_field(name="\u200b", value=option[1] + " - " + option[0], inline=False)

    return embed


"""" get token"""
with open("secrets.json") as json_data:
    token = json.load(json_data)["token"]

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if not re.match(pattern_command, message.content): # command_pattern.match(message.content):
        return

    await message.delete()

    param = extractParams(input=message.content)

    title = param[0]
    options = param[1]

    # checkEmoji
    i = -1
    for option in options:
        i += 1
        options[i] = (option[0], checkEmoji(emoji_to_check=option[1], position=i, server_emojis=message.guild.emojis))

    embed = generateEmbed(title=title, author=message.author, options=options)

    send_message = await message.channel.send(embed=embed)

    for option in options:
        await send_message.add_reaction(option[1])
        
    # TODO check message longer that 6000 characters

client.run(token)
