# Discord bot Text Generator

A Discord bot that can extract messages from users and generate new messages from any corpus.

It uses a simple Markov Chains algorithm and an n-gram model to generate the text.

## How to run

Clone this repository or download it and run the bot.py in a terminal/console.

```bash
  python3 bot.py
```

Create a "corpus" directory in the app's folder.

Once the bot is online. You and the server members can use the command !textgenhelp to get information about the bot's commands.

## Features

- Extract messages from users in a given channel.
- Generates new messages based on the given corpus.
  <br>It's important to keep in mind that the generated text is highly dependent on the given corpus, so make any necessary tweaks to the preprocessing.<br>

## Tech

It's powered by the advanced Natural Language Processing library <a href="https://github.com/explosion/spaCy">spaCy</a>
!
