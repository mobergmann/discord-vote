import datetime
import discord
import json
import re

# represents a new version of the poll discord bot
# it can create a poll using emojis to vote
# 
# the command to create a new poll is:
# !vote | !poll {a questionable topic to discuss with your friends} [Option A] [optional emoji to replace the current one] [Option B] ...

command_pattern = re.compile("^!((vote)|(poll)) {[\w ]+}(( \[[\w ]+\])({.*})?){2,10}$") # see http://regexr.com/56use

option_pattern = re.compile("(\[((\w)|( ))+\])({.*})?")
option_title_pattern = re.compile("(\[[\w ]+\])")
option_emoji_pattern = re.compile("({.*})?")

# default emojis
predefined_emojis = [
    ":regional_indicator_a:",
    ":regional_indicator_b:",
    ":regional_indicator_c:",
    ":regional_indicator_d:",
    ":regional_indicator_e:",
    ":regional_indicator_f:",
    ":regional_indicator_g:",
    ":regional_indicator_h:",
    ":regional_indicator_i:",
    ":regional_indicator_j:",
    ":regional_indicator_k:",
    ":regional_indicator_l:",
    ":regional_indicator_m:",
    ":regional_indicator_n:",
    ":regional_indicator_o:",
    ":regional_indicator_p:",
    ":regional_indicator_q:",
    ":regional_indicator_r:",
    ":regional_indicator_s:",
    ":regional_indicator_t:",
    ":regional_indicator_u:"
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

def extractBetween(input, start, start_delimiter, end_delimiter):
    inWord = False
    ret = ""

    i = 0
    for char in input:
        i+=1

        if i != start or not inWord: # skip all literals to the start position
            continue
        
        if char == end_delimiter or i > len(input):
            break

        if char == start_delimiter:
            inWord = True
            continue

        ret += char

    return ret



# DONE
def getTitle(input):
    ret = ""
    inTitle = False

    # finds the title
    i = -1
    while True:
        i+=1
        char = input[i]
        if char == "}" or i > len(input):
            break
        elif char == "{":
            inTitle = True
            continue
        elif not inTitle:
            continue

        ret += char

    return ret


# TODO
def getOptions(input):
    # creates a list of options with or without emojis
    tmp_list = re.findall(option_pattern, input)
    
    text_list = []
    emoji_list = []

    i = -1
    for elem in tmp_list:
        elem = elem[0]
        i+=1

        # region extract text
        
        text_match = re.search(option_title_pattern, elem) # search the option for text (used for retriving the start and stop indices)
        text_list.append(elem[text_match.start()+1 : text_match.end()-1]) # [text] cut the [ and the ] off, so only the text is left
        
        # endregion
        
        # region extract emoji
        
        emoji_match = re.search(option_emoji_pattern, elem)
        if not emoji_match: # if not a match set the default emoji and skip to the next iteration
            emoji_list.append(predefined_emojis[i])
            continue
    
        emoji = elem[emoji_match.start()+1 : emoji_match.end()-1]

        # TODO check for is_usable()
        # TODO emoji does not exist
        # if not an emoji emoji already used, or emoji is a predefined emoji, override it with the matching emoji at position i
        if emoji in emoji_list or emoji in predefined_emojis: # TODO may change emoji_match to not None
            emoji_list.append(predefined_emojis[i])
            continue
        
        emoji_list.append(emoji)

        # endregion
        
    # fuse emoji and text list together
    ret = []
    for i in range(0, len(text_list)):
        ret.append({"text":text_list[i], "emoji":emoji_list[i]})


    return ret


# get token
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
    
    if not command_pattern.match(message.content):
        return

    title = getTitle(message.content)
    options = getOptions(message.content)

    embed = discord.Embed(
        title = title,
        # title = ,
        # description = "desc",
        # url = ,
        timestamp = datetime.datetime.now(),
        # colour = ,
    )
    # embed_message.set_footer()
    # embed_message.set_image()
    embed.set_author(
        name=message.author.display_name, 
        icon_url=message.author.avatar_url)

    for option in options:
        embed.add_field(name=option["text"], value=option["emoji"], inline=False)

    react_message = await message.channel.send(embed=embed)

    for option in options:
        await react_message.add_reaction(option["emoji"])

# TODO check message shorter that 6000 characters

    # delete send command, to remove any 
    await message.delete()

client.run(token)
