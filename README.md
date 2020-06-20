# discord-vote
A Vote/ Poll Bot for Discord

# Host yourself
create a `secrests.json` file and place your token. The File should look like this:
```json
{
    "token": "token_here"
}
```
Replace `token_here` with your Bot token.


# Adding the Bot
I provide a self hosted version of the master branch.
Please notice, that the Bot may not always be online.

[Click me](https://discordapp.com/oauth2/authorize?client_id=722823450384662558&scope=bot&permissions=273472) to add the stable Bot to your Server.


# Using the Bot:

1. You can create a poll with the command `!poll` or `!vote`.
2. The poll needs a Title, which you need to provide in curly brackets `{Title}` after the command.
3. You can add Options in square brackets `[Option]` after the Title.
4. To attach a special emoji to an option you need to provide it after the option (without spaces) in curly brackets `{🧪}`. Otherwise, a default emoji is being used.
5. Replace 🧪 with your desired emoji.

## Example
```shell
!vote {How does Chocolate taste} [Good]{👍} [Bad]{👎}
# or
!poll {How does Chocolate taste} [Good]{👍} [Bad]{👎}
```

Note, that you can only use alphanumeric characters and spaces.
This means, that only characters from `A` to `Z`, `a` to `z`, `0` to `9` and ` ` are allowed.
Please also notice, that this does not include special characters.
