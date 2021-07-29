import typing

import discord
from discord.ext import commands
# end imports


# Embed generator
async def embed_gen(
        channel: discord.abc.Messageable,
        title: typing.Union[
            str,
            None],
        description: typing.Union[
            str,
            None
        ],
        footer_text: typing.Union[
            str,
            None
        ],
        thumbnail_url: typing.Union[
            str,
            None
        ],
        image_url: typing.Union[
            str,
            None
        ],
        color: typing.Union[
            int,
            discord.Colour,
            None
        ],
        return_embed: bool
):
    """A coroutine that returns a ``discord.Embed`` or a ``discord.Message``"""

    Empty = discord.Embed.Empty

    embed = discord.Embed()

    embed.title = title if title else Empty
    embed.description = description if description else Empty
    embed.set_footer(text=footer_text if footer_text else Empty)
    embed.set_thumbnail(url=thumbnail_url if thumbnail_url else Empty)
    embed.set_image(url=image_url if image_url else Empty)
    embed.colour = color if color else Empty

    if not return_embed:
        message = await channel.send(embed=embed)
        return message

    else:
        return embed