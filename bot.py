from dotenv import load_dotenv
import discord
from discord.ext import commands
from text_generator import generate_text
import os
from extract_messages import save_sentences_to_file, extract_user_messages
import spacy

load_dotenv()

TOKEN = os.getenv('DISCORD_API_TOKEN')


def run_discord_bot():
    # intents = discord.Intents.all()
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f"I'm ready as User: {bot.user} (ID: {bot.user.id})")

    @bot.command()
    @commands.is_owner()
    async def sync_commands(ctx):
        await bot.tree.sync()
        print(f'The commands are up to date now!')

    @bot.hybrid_command()
    async def gen(ctx, user: str):

        text = generate_text(user)
        await ctx.send(text)

    @bot.command()
    @commands.is_owner()
    async def extract_messages(ctx, channel_id: int, user_id: int):
        print('Extracting messages!')
        # You can change it to the desired language.
        nlp = spacy.load("pt_core_news_sm")
        # Get the Discord channel and user objects
        channel = bot.get_channel(channel_id)
        user = await bot.fetch_user(user_id)

    # Extract the user's messages from the channel
        messages = await extract_user_messages(channel, user)

    # Parse the messages into sentences using Spacy's sentencizer
        sentences = []
        for message in messages:
            doc = nlp(message)
            for sentence in doc.sents:
                sentences.append(sentence.text)

    # Save the sentences to a text file
        save_sentences_to_file(sentences, "user_messages.txt")

        print("Messages extracted and saved to user_messages.txt")

    bot.run(TOKEN)


if __name__ == "__main__":
    run_discord_bot()
