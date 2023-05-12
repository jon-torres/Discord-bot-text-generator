# Discord bot Text Generator

A Discord bot that can extract messages from users and generate new messages from any corpus.

It uses a Markov Chains algorithm and an n-gram model to generate the text.

## How to run

1. Clone this repository or download it. 
2. Create a "corpus" directory in the app's folder.
3. Open your terminal/console and navigate to the app's folder.
4. Run bot.py using the command below.

```bash
  python3 bot.py
```

Once the bot is running, the owner or the server members can use the command !textgenhelp – in the chat – to get information about the bot's commands.

## Features

- Extract all the messages sent from users in a given channel.
- Generates new messages based on the given corpus or any corpus.
  <br>It's important to keep in mind that the generated text is highly dependent on the corpus, so make any necessary tweaks to the preprocessing.<br>

## Tech

It's powered by the advanced Natural Language Processing library <a href="https://github.com/explosion/spaCy">spaCy</a>!
