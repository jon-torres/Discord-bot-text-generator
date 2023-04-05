import spacy
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from text_generator import generate_text, CORPUS_DIR
from extract_messages import save_sentences_to_file, extract_user_messages


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
        app_info = await bot.application_info()
        bot.owner_id = app_info.owner.id
        print(f"I'm ready as User: {bot.user} (ID: {bot.user.id})")

    @bot.command()
    async def textgenhelp(ctx):
        """Show the help message."""
        if ctx.author.id == bot.owner_id:
            embed = discord.Embed(title="Text Generator Bot Help Menu",
                                  description="Here are the available commands:", color=0x00ff00)
            embed.add_field(
                name="!gen <user> or /gen", value="Generate a message for a user.", inline=False)
            embed.add_field(name="!extract_messages <channel_id> <user_id> or /extract_messages",
                            value="Extract messages sent by a specific user in a channel.", inline=False)
            embed.add_field(name="!corpus_list",
                            value="List available files in the corpus directory.", inline=False)
            embed.add_field(name="!sync_commands",
                            value="Syncs commands to the server. It should be used only when new slash commands are added.", inline=False)
        else:
            embed = discord.Embed(title="Text Generator Bot Help Menu",
                                  description="Here are the available commands:", color=0x00ff00)
            embed.add_field(
                name="!gen <user> or /gen", value="Generate a message for a user.", inline=False)

        await ctx.send(embed=embed)

    @bot.command()
    @commands.is_owner()
    async def sync_commands(ctx):
        await bot.tree.sync()
        print(f'The commands are up to date now!')

    @bot.hybrid_command()
    async def gen(ctx, user: str):

        text = generate_text(user)
        await ctx.send(text)

    @bot.hybrid_command()
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

    @bot.command()
    @commands.is_owner()
    async def corpus_list(ctx):
        """List available files in the corpus directory."""
        files = os.listdir(CORPUS_DIR)
        file_list = '\n'.join([os.path.splitext(file)[0] for file in files])
        await ctx.send(f"Available corpus for text generation:\n{file_list}")

    bot.run(TOKEN)


if __name__ == "__main__":
    run_discord_bot()
