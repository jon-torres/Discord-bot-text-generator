import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import spacy
from text_generator import generate_text, CORPUS_DIR
from extract_messages import (
    extract_user_messages,
    save_user_messages,
)

load_dotenv()

# You can change it to the desired language.
nlp = spacy.load("pt_core_news_sm")
TOKEN = os.getenv("DISCORD_API_TOKEN")
if TOKEN is None:
    raise ValueError("The Discord Api Token environment variable must be set.")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    app_info = await bot.application_info()
    bot.owner_id = app_info.owner.id
    print(f"I'm ready as User: {bot.user} (ID: {bot.user.id})")


def build_help_embed(is_owner: bool):
    embed = discord.Embed(
        title="Text Generator Bot Help Menu",
        description="Here are the available commands:",
        color=0x00FF00,
    )
    embed.add_field(
        name="!gen <user> or /gen",
        value="Generate a message for a user.",
        inline=False,
    )
    if is_owner:
        embed.add_field(
            name="!extract_messages <channel_id> <user_id>",
            value="Extract messages sent by a specific user in a channel.",
            inline=False,
        )
        embed.add_field(
            name="!corpus_list",
            value="List available files in the corpus directory.",
            inline=False,
        )
        embed.add_field(
            name="!sync_commands",
            value="Syncs commands to the server. Use only when new slash commands are added.",
            inline=False,
        )
    return embed


@bot.command()
async def textgenhelp(ctx):
    """Show the help message."""
    is_owner = ctx.author.id == bot.owner_id
    embed = build_help_embed(is_owner)
    await ctx.send(embed=embed)


@bot.command()
@commands.is_owner()
async def sync_commands(ctx):
    await bot.tree.sync()
    print("The commands are up to date now!")


@bot.hybrid_command()
async def gen(ctx, user: str):
    text = generate_text(user)
    await ctx.send(text)


@bot.command()
@commands.is_owner()
async def extract_messages(ctx, channel_id: int, user_id: int):
    await ctx.send(
        "Extracting messages, please wait..."
    )  # Notify user about the start of the process
    channel = bot.get_channel(channel_id)
    user = await bot.fetch_user(user_id)

    try:
        messages = await extract_user_messages(channel, user)

        sentences = []
        for message in messages:
            doc = nlp(message)
            for sentence in doc.sents:
                sentences.append(sentence.text)

        save_user_messages(sentences, user_id)  # Save using user ID
        await ctx.send(
            "Messages extracted and saved successfully!"
        )  # Notify user about successful extraction
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")  # Send error feedback


@bot.command()
@commands.is_owner()
async def corpus_list(ctx):
    """List available files in the corpus directory."""
    try:
        files = os.listdir(CORPUS_DIR)
    except FileNotFoundError:
        await ctx.send("Corpus directory not found.")
        return
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
        return

    file_list = "\n".join([os.path.splitext(file)[0] for file in files])
    await ctx.send(f"Available corpus for text generation:\n{file_list}")


if __name__ == "__main__":
    bot.run(TOKEN)
