import sys
import traceback
from discord.ext import commands

from utils import general
from cogs.global_ import Global
# end imports

IGNORED_COMMANDS = ["reload"]
# end global constants


def short_traceback():
    """A function that returns a short version of the traceback."""

    error = sys.exc_info()[1]
    etype = type(error).__name__

    return f"{etype}: {error}"


def full_traceback():
    """A function that returns the full traceback."""

    error = sys.exc_info()[1]
    etype = type(error)
    trace = error.__traceback__
    lines = traceback.format_exception(etype, error, trace)
    full_traceback_text = ''.join(lines)

    return full_traceback_text


class ErrorListeners(commands.Cog):
    """A cog that represents ``on_command_error`` and ``on_error``."""

    def __init__(self, client):
        self.client = client

    # OnError
    @commands.Cog.listener()
    async def on_error(self, event):
        error = sys.exc_info()[1]
        etype = type(error)
        trace = error.__traceback__
        lines = traceback.format_exception(etype, error, trace)
        full_traceback_text = ''.join(lines)

        error_channel = self.client.get_channel(Global.error_channel)
        await general.embed_gen(
            error_channel,
            f"An error occurred. Event: {event}",
            f"```py\n{full_traceback_text}\n```",
            None,
            None,
            None,
            Global.error_red,
            False
        )

    # OnCommandError
    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):

        async def log_traceback():
            etype = type(error)
            trace = error.__traceback__
            lines = traceback.format_exception(etype, error, trace)
            full_traceback_text = ''.join(lines)

            error_channel = self.client.get_channel(Global.error_channel)
            await general.embed_gen(
                error_channel,
                f"An error occurred. Command: {ctx.command}",
                f"```py\n{full_traceback_text}\n```",
                None,
                None,
                None,
                Global.error_red,
                False
            )

        if isinstance(error, commands.CommandNotFound):
            return

        if isinstance(error, commands.NotOwner):
            if ctx.command.name.lower() in IGNORED_COMMANDS:
                return
            else:
                await log_traceback()

        else:
            await log_traceback()


def setup(client):
    client.add_cog(ErrorListeners(client))

