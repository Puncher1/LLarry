from discord.ext import commands
import os

from utils import general
from utils import global_ as g
from cogs import error_handler


# end imports


class MySelf(commands.Cog):

    def __init__(self, client):
        self.client = client


    # Command: Cog reload
    @commands.command(aliases=["cr", "r"])
    @commands.is_owner()
    async def reload(self, ctx, *, path=None):
        """Reloads cogs, loads cogs that aren't loaded and unloads cogs whose file doesn't exist anymore."""

        # All cogs reload
        async def all_cogs_reloading():
            """Reloads every extension in './cogs'. Loads extensions that aren't loaded. Unloads extensions whose file doesn't exist anymore."""

            error = None

            # Unload deleted extension files
            unloaded_list, unloaded_count = [], 0

            for extension in list(self.client.extensions):
                extension_raw = extension
                extension = extension.split(".", 1)[1]
                extension = f"{extension}.py"

                if extension not in os.listdir("./cogs"):
                    try:
                        self.client.unload_extension(extension_raw)
                    except:
                        short_trace = error_handler.short_traceback()
                        error = f"```py\n{short_trace}\n```"
                        break
                    else:
                        unloaded_list.append(f"`{extension_raw}`")
                        unloaded_count += 1

            # Reload/Load extensions
            reloaded_list, reloaded_count = [], 0
            loaded_list, loaded_count = [], 0

            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    path = f'cogs.{filename[:-3]}'

                    if path in self.client.extensions:
                        # Reload

                        try:
                            self.client.reload_extension(f'cogs.{filename[:-3]}')
                        except:
                            short_trace = error_handler.short_traceback()
                            error = f"```py\n{short_trace}\n```"
                            break

                        else:
                            reloaded_list.append(f"`{path}`")
                            reloaded_count += 1

                    else:
                        # Load

                        try:
                            self.client.load_extension(f'cogs.{filename[:-3]}')
                        except:
                            short_trace = error_handler.short_traceback()
                            error = f"```py\n{short_trace}\n```"
                            break

                        else:
                            loaded_list.append(f"`{path}`")
                            loaded_count += 1

            if loaded_count > 0:
                loaded_list_join = "\n".join(loaded_list)
                loaded_str = f"\n\n{g.e_arrow_up_right} **Loaded - [{loaded_count}]**" \
                             f"\n{loaded_list_join}"
            else:
                loaded_str = ""

            if reloaded_count > 0:
                reloaded_list_join = "\n".join(reloaded_list)
                reloaded_str = f"{g.e_reload} **Reloaded - [{reloaded_count}]**" \
                               f"\n{reloaded_list_join}"
            else:
                reloaded_str = ""

            if unloaded_count > 0:
                unloaded_list_join = "\n".join(unloaded_list)
                unloaded_str = f"\n\n{g.e_arrow_down_right} **Unloaded - [{unloaded_count}]**" \
                               f"\n{unloaded_list_join}"
            else:
                unloaded_str = ""

            error = error if error else "No error while reloading."

            await general.embed_gen(
                channel=ctx.channel,
                color=None,
                title="Cogs",
                description=f"{reloaded_str}"
                            f"{loaded_str}"
                            f"{unloaded_str}"
                            f"\n\n\n**Error**"
                            f"\n{error}",
                footer_text=None,
                thumbnail_url=None,
                image_url=None,
                return_embed=False
            )

        # Cog reload by path
        async def path_cog_reload():

            if path in self.client.extensions:
                try:
                    self.client.reload_extension(f"{path}")
                except:
                    short_trace = error_handler.short_traceback()
                    error = f"```py\n{short_trace}\n```"

                    await general.embed_gen(
                        channel=ctx.channel,
                        title="Cogs",
                        description=f"**An error occurred.**"
                                    f"\n{error}",
                        footer_text=None,
                        color=None,
                        thumbnail_url=None,
                        image_url=None,
                        return_embed=False
                    )
                    return 

            else:
                try:
                    self.client.load_extension(f"{path}")
                except:
                    short_trace = error_handler.short_traceback()
                    error = f"```py\n{short_trace}\n```"

                    await general.embed_gen(
                        channel=ctx.channel,
                        title="Cogs",
                        description=f"**An error occurred.**"
                                    f"\n{error}",
                        footer_text=None,
                        color=None,
                        thumbnail_url=None,
                        image_url=None,
                        return_embed=False
                    )
                    return

            reloaded_str = f"{g.e_reload} **Reloaded**" \
                           f"\n`{path}`"

            await general.embed_gen(
                channel=ctx.channel,
                color=None,
                title="Cogs",
                description=f"{reloaded_str}",
                footer_text=None,
                thumbnail_url=None,
                image_url=None,
                return_embed=False
            )

        # Invoking coroutines
        if not path:
            await all_cogs_reloading()
        else:
            await path_cog_reload()


def setup(client: commands.Bot):
    client.add_cog(MySelf(client))