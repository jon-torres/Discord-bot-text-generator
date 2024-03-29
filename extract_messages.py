from text_generator import CORPUS_DIR
import os
from typing import List
import discord


async def extract_user_messages(
    channel: discord.TextChannel, user: discord.User
) -> List[str]:
    """
    Extracts messages sent by a specific user in a channel.
    """
    messages = []
    async for message in channel.history(limit=None, oldest_first=True):
        if message.author == user:
            messages.append(message.content)
    return messages


def save_sentences_to_file(sentences: List[str], filename: str):
    """
    Saves the sentences to a file.
    """
    with open(
        os.path.join(CORPUS_DIR, filename), "w", encoding="utf-8"
    ) as file:
        file.write("\n".join(sentences))


def save_user_messages(sentences: List[str], user_id: int):
    """
    Saves user messages to a file named based on the user ID.
    """
    filename = f"user_messages_{user_id}.txt"
    save_sentences_to_file(sentences, filename)
