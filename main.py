"""
with the bot you can create a poll using emojis to vote by reacting with them

the command to create a new poll is:
!vote | !poll {a questionable topic to discuss with your friends} [Option A]{optional emoji to replace the current one} [Option B] ...
"""

import datetime
import discord
from discord.ext import commands
from emoji import UNICODE_EMOJI
import json
import re

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

pattern_vote_args = re.compile(
    "^{([^}]+)} ((?:\[[^\]]+\](?:{[^}]*})? ?){2,10})$")
pattern_vote_option = re.compile("(\[[^\]]+\])({[^}]*})?")

client = commands.Bot(command_prefix="!")

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


# region helper functions

def checkEmoji(emoji_to_check: str, position: int, server_emojis: list) -> str:
    """Checks if the emoji is a valid emoji.
    If not returns a default emoji, based on the current position.

    Args:
        emoji_to_check (str): The Emoji which should be validated.
        position (int): The position of the current option. Used for replacement when the emoji is invalid.
        server_emojis (list): A list of Emojis available on the guild from which the message has been send.

    Returns:
        str: The original emoji, if the Emoji is supported, or a default emoji based on the position of the option.
    """

    if emoji_to_check in UNICODE_EMOJI:  # if the given emoji is not in default emoji set
        return emoji_to_check

    # if the emoji is not available from the server
    if isServerEmoji(emoji_to_check=emoji_to_check, server_emojis=server_emojis):
        return emoji_to_check

    return predefined_emojis[position]  # set the default emoji


def isServerEmoji(emoji_to_check: str, server_emojis: list) -> tuple:
    """Checks, if the Guild has the given emoji and if its available.

    Args:
        emoji_to_check (str): The emoji, which should be checked.
        server_emojis (list): A list of all emojis available on the server.

    Returns:
        bool: True if the Guild has the emoji and its available. False otherwise. 
    """

    for server_emoji in server_emojis:
        constructed_emoji = "<:" + server_emoji.name + ":" + \
            str(server_emoji.id) + ">"  # generate the name of the emoji
        constructed_emoji_animated = "<a:" + server_emoji.name + ":" + \
            str(server_emoji.id) + \
            ">"  # generate the name of the emoji if it was an animated emoji
        # check if the emoji is on the guild
        if emoji_to_check == constructed_emoji or emoji_to_check == constructed_emoji_animated:
            if not server_emoji.available:  # check if the emoji is available
                return False
            return True
    return False


def extractParams(input: str):
    """Extracts the title and the options of the message content with the help of regex. 
    The title is of type string, and the options is of type list, containing tuples with name and emoji.

    Args:
        input (str): the content of the message

    Returns:
        tuple: Returns a tuple, containing the title and a list of the options.
    """

    tmp_list_1 = re.findall(pattern_vote_args, input)
    match = tmp_list_1[0]

    title = match[0]
    tmp = match[1]
    pre_options = re.findall(pattern_vote_option, tmp)

    option_titles = []
    option_emojis = []

    options = []
    for option in pre_options:
        name = option[0][1: len(option[0])-1]
        emoji = option[1][1: len(option[1])-1]
        emoji = emoji.replace(" ", "") # remove any spaces, for convenience purpose when typing the command
        options.append((name, emoji))

    return title, options


def generateEmbed(title: str, author: discord.User, options: list) -> discord.Embed:
    """Generate an embed for the vote and returns the embed.

    Args:
        title(str): the title of the Vote
        author(discord.User): the User, which created the Vote
        options(list): the list of options, which has to be embeded

    Returns:
        discord.Embed: Returns the generated embed
    """

    embed = discord.Embed(
        title=title,
        # description = "desc",
        timestamp=datetime.datetime.now())
    embed.set_author(
        name=author.display_name,
        icon_url=author.avatar_url)

    for option in options:
        embed.add_field(
            name="\u200b", value=option[1] + " - " + option[0], inline=False)

    return embed

# endregion

# region commands

@client.command()
async def vote(ctx, *, args):
    # TODO use args instead of ctx.message.content
    
    if ctx.author == client.user:
        return
    if ctx.author.bot:
        return
    if not re.match(pattern_vote_args, args):
        return

    await ctx.message.delete() # clean message history


    param = extractParams(input=args)

    title = param[0]
    options = param[1]

    # checkEmoji
    i = -1
    for option in options:
        i += 1
        options[i] = (option[0], checkEmoji(emoji_to_check=option[1],
                                            position=i, server_emojis=ctx.guild.emojis))

    embed = generateEmbed(title=title, author=ctx.author, options=options)
    
    send_message = await ctx.channel.send(embed=embed)
    
    for option in options:
        await send_message.add_reaction(option[1])
    
    return

@client.command()
async def evaluate(ctx: str) -> str:
    """returns a link to an image, which is postet into the changel with the message.

    Args:
        ctx (str): [description]

    Returns:
        str: [description]
    """
    pass

# endregion

# region starting the bot

""""parse token from secrets.json"""
with open("secrets.json") as json_data:
    token = json.load(json_data)["token"]
client.run(token)

# endregion