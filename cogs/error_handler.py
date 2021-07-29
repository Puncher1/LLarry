import sys
import traceback
import discord
from discord.ext import commands
import aiohttp

from utils import embeds
from cogs.global_ import Global
# end imports

IGNORED_COMMANDS = ["reload", "shutdown"]
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
    """Represents ``on_command_error`` and ``on_error``."""

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
        await embeds.embed_gen(
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
        error_png = discord.File("./images/error.png", filename="error.png")
        # end local constants

        async def log_traceback():
            etype = type(error)
            trace = error.__traceback__
            lines = traceback.format_exception(etype, error, trace)
            full_traceback_text = ''.join(lines)

            error_channel = self.client.get_channel(Global.error_channel)
            await embeds.embed_gen(
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

        elif isinstance(error, commands.NotOwner):
            if ctx.command.name.lower() in IGNORED_COMMANDS:
                return
            else:
                not_owner_embed = await embeds.embed_gen(
                    ctx.channel,
                    None,
                    f"**You don't have sufficient permissions to use that!**",
                    None,
                    None,
                    None,
                    Global.error_red,
                    True
                )
                not_owner_embed.set_author(name="Error", icon_url="attachment://error.png")
                await ctx.channel(embed=not_owner_embed, file=error_png)

        elif isinstance(error, commands.MissingRequiredArgument):
            signature = f"{ctx.prefix}{ctx.command.qualified_name} {ctx.command.signature}"

            missing_embed = await embeds.embed_gen(
                ctx.channel,
                None,
                f"**A required argument is missing!** "
                f"\nPlease try again."
                f"\n\n**Usage:**"
                f"\n`{signature}`",
                None,
                None,
                None,
                Global.error_red,
                True
            )
            missing_embed.set_author(name="Error", icon_url="attachment://error.png")
            await ctx.send(embed=missing_embed, file=error_png)

        elif isinstance(error, commands.CommandInvokeError):
            error_msg = error.args[0].split("NotFound:")[-1].strip()
            if error_msg == "notFound (status code: 404)":
                error_png = discord.File("./images/error.png", filename="error.png")
                signature = f"{ctx.prefix}{ctx.command.qualified_name} {ctx.command.signature}"

                not_found_embed = await embeds.embed_gen(
                    ctx.channel,
                    None,
                    f"**Resource not found!** "
                    f"\nMake sure you provide a valid tag and then try again."
                    f"\n\n**Usage:**"
                    f"\n`{signature}`",
                    None,
                    None,
                    None,
                    Global.error_red,
                    True
                )
                not_found_embed.set_author(name="Error", icon_url="attachment://error.png")
                await ctx.send(embed=not_found_embed, file=error_png)
            else:
                await log_traceback()

        else:
            await log_traceback()


def setup(client):
    client.add_cog(ErrorListeners(client))

