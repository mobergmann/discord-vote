# represents a new version of the poll discord bot
# it can create a poll using emojis to vote
# 
# the command to create a new poll is:
# !vote | !poll {a questionable topic to discuss with your friends} [Option A] [optional emoji to replace the current one] [Option B] ...

import datetime
import discord
import json
import re

command_pattern = re.compile("^!((vote)|(poll)) {[\w ]+}(( \[[\w ]+\])({.*})?){2,10}$") # http://regexr.com/56use
command_beginning_pattern = re.compile("^!(vote)|(poll) {[\w ]+} ")

option_pattern = re.compile("\[w+\]({.*})?")
option_title_pattern = re.compile("(\[[\w]+\])")
option_emoji_pattern = re.compile("({.*})?")

# default emojis
predefined_emojis = [
    "0️⃣","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"
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

# TODO comment
def extractBetween(input, start, start_delimiter, end_delimiter):
    inWord = False
    ret = ""

    i = -1
    for char in input:
        i+=1

        if i < start:
            continue
        elif char == start_delimiter:
            inWord = True
            continue
        elif char == end_delimiter:
            break
        elif not inWord: # skip all literals to the start position
            continue

        ret += char

    return {"ret":ret, "jump":i}

# TODO comment, output end of file
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
    # tmp_list = re.findall(option_pattern, input)
    
    text_list = []
    emoji_list = []

    i = -1
    counter = 0
    while True:
        i+=1
        if i > len(input)-1:
            break

        char = input[i]

        if char == "[":
# TODO tests
            obj = extractBetween(input, i, "[", "]")
            
            i = obj["jump"]
            i+=1 # count up, to catch the next character
            char = input[i] # update char when modifying i

            text_list.append(obj["ret"])
            counter += 1
            
            # do not out of bounce
            if (i + 1) > len(input):
                emoji_list.append(predefined_emojis[counter]) # no emoji is following, append the default emoji
            else:
                # emoji is following, extract it
                if char == "{":
                    obj = extractBetween(input, i, "{", "}")
                    i = obj["jump"]
                    char = input[i] # update char when modifying i
                    emoji_list.append(obj["ret"])
                    # TODO test if valid emoji
                else:
                    emoji_list.append(predefined_emojis[counter]) # no emoji is following, append the default emoji
        



# region old
    # i = -1
    # for elem in tmp_list:
    #     elem = elem[0]
    #     i+=1

    #     # region extract text
        
    #     text_match = re.search(option_title_pattern, elem) # search the option for text (used for retriving the start and stop indices)
    #     text_list.append(elem[text_match.start()+1 : text_match.end()-1]) # [text] cut the [ and the ] off, so only the text is left
        
    #     # endregion
        
    #     # region extract emoji
        
    #     # TODO remove two lines
    #     emoji_list.append(predefined_emojis[i])
    #     continue

    #     emoji_match = re.search(option_emoji_pattern, elem)
    #     if not emoji_match: # if not a match set the default emoji and skip to the next iteration
    #         emoji_list.append(predefined_emojis[i])
    #         continue
    
    #     emoji = elem[emoji_match.start()+1 : emoji_match.end()-1]

    #     # TODO check for is_usable()
    #     # TODO emoji does not exist
    #     # if not an emoji emoji already used, or emoji is a predefined emoji, override it with the matching emoji at position i
    #     if emoji in emoji_list or emoji in predefined_emojis: # TODO may change emoji_match to not None
    #         emoji_list.append(predefined_emojis[i])
    #         continue
        
    #     emoji_list.append(emoji)

    #     # endregion
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

    match_obj = re.search(command_beginning_pattern, message.content) # identify bound os title, to extract an string contining only the options # TODO rename
    raw_option = message.content[match_obj.end()+1 : len(message.content)] # string only containing the options
    
    title = getTitle(message.content) # TOOD may add extra string based on match_obj
    option_list = getOptions(raw_option)

    embed = discord.Embed(
        title = title,
        # description = "desc",
        timestamp = datetime.datetime.now())
    embed.set_author(
        name=message.author.display_name, 
        icon_url=message.author.avatar_url)

    for option in option_list:
        embed.add_field(name=option["text"], value=option["emoji"], inline=False)

    react_message = await message.channel.send(embed=embed)

    for option in option_list:
        await react_message.add_reaction(option["emoji"])

# TODO check message longer that 6000 characters

    # await message.delete() # TODO uncomment

client.run(token)
