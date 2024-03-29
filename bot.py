import logging
import os
import signal
import sys

import discord
from discord.ext import commands

from db import db
from settings import TOKEN

logger = logging.getLogger("discord")


class MyBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            intents=discord.Intents.all(),
            command_prefix=(),
            activity=discord.Activity(
                type=discord.ActivityType.playing,
                name="/play"
            )
        )

    async def load_extension(self, name: str, *, package: str | None = None) -> None:
        try:
            await super().load_extension(name, package=package)
        except commands.ExtensionError as error:
            logger.error("Failed to load extension %s: %s", name, error)

    async def setup_hook(self) -> None:
        for file in os.listdir("./extensions"):
            if file.endswith(".py"):
                await self.load_extension(f"extensions.{file[:-3]}")
        logger.info("Extensions loaded.")

    async def on_ready(self) -> None:
        assert self.user is not None
        logger.info("Logged in as %s", self.user.name)

    async def close(self) -> None:
        await super().close()
        logger.info("Bot closed.")


def main() -> None:
    db.setup()
    bot = MyBot()
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
    bot.run(TOKEN)


if __name__ == "__main__":
    main()
