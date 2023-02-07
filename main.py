# Imports
import requests
import os
import discord
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents = intents)

# Functions
def getAWord():
    api_url = 'https://api.api-ninjas.com/v1/randomword'
    response = requests.get(api_url, headers={'X-Api-Key': os.environ['wordApiToken']})
    if response.status_code == requests.codes.ok:
        return(response.json()['word'])
    else:
        print("Error:", response.status_code, response.text)
        return "HANGMAN"
    
async def printHangman (lettersFound, mistakeCount, channel):
  message = hangmanPhases[mistakeCount]
  message += "\n" + " ".join(lettersFound)
  await channel.send(message)

# Variables
hangmanPhases = [
    "",
    "       +----------+\n       |\n       |\n       |\n       |\n       |\n       |\n       |\n       |\n       |\n+------+------------------+",
    "       +----------+\n       |          |\n       |          |\n       |         (.)\n       |\n       |\n       |\n       |\n       |\n       |\n+------+------------------+",
    "       +----------+\n       |          |\n       |          |\n       |         (.)\n       |          | \n       |          | \n       |\n       |\n       |\n       |\n+------+------------------+",
    "       +----------+\n       |          |\n       |          |\n       |         (.)\n       |         /|\ \n       |        | | |\n       |\n       |\n       |\n       |\n+------+------------------+",
    "       +----------+\n       |          |\n       |          |\n       |         (.)\n       |         /|\ \n       |        | | |\n       |         / \ \n       |        /   \ \n       |        '   '\n       |\n+------+------------------+"
]

# main()

#Event listener
@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if(message.author == client.user):
    return

  if message.content.startswith('!hello'):
    await message.channel.send('Waiting for something to happen ?')

  if message.content.startswith('!hangman'):
    wordToFind = [x for x in getAWord().upper()]
    lettersChecked = []
    lettersFound = ["-" if x == "-" else "\_" for x in wordToFind]
    mistakeCount = 0
    isGameNotOver = True
    channel = message.channel
    error = ""

    await printHangman(lettersFound, mistakeCount, channel)

    while(isGameNotOver):
      if(error == ""):
        def check(m):
          return m.author == message.author and m.channel == channel and m.content.isalpha() and len(m.content) == 1
  
        msg = await client.wait_for('message', check=check)
  
        letter = msg.content.upper()
        
        if (letter in lettersChecked):
          error = "checkDuplicate"
        else:
          lettersChecked.append(msg.content.upper())
          if(letter in wordToFind):
            for i in range(len(wordToFind)):
              if (wordToFind[i] == letter):
                  lettersFound[i] = letter
          else:
            mistakeCount += 1
  
        await printHangman(lettersFound, mistakeCount, channel)
        
        if(mistakeCount == 5):
          isGameNotOver = False
          await channel.send("You lose ! The word was : " + ''.join(wordToFind))
        if("\_" not in lettersFound):
          isGameNotOver = False
          await channel.send("You won !")
    
      elif (error == "checkDuplicate"):
        await channel.send("You already checked this letter. Enter another one")
        error = ""

keep_alive()
client.run(os.environ['discordApiToken'])