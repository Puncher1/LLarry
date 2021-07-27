from discord.ext import commands
# end imports


class Global(commands.Cog):

    def __init__(self, client):
        self.client = client


    # Channel
    error_channel = 764227729653628949

    # Emojis
    e_reload = "🔄"
    e_arrow_up_right = "↗️"
    e_arrow_down_right = "↘️"
    e_white_checkmark = "✅"

    # Hex colors
    error_red = 0xBB0000


def setup(client):
    client.add_cog(Global(client))