from nextcord.ext import commands, ipc
from datetime import datetime


class IpcRoutes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @ipc.server.route()
    async def get_member_count(self, data):
        guild = self.bot.get_guild(data.guild_id)  # get the guild object using parsed guild_id
        return guild.member_count  # return the member count to the client


    @ipc.server.route()
    async def get_cmd(self, data):
        cmds = []
        for x in self.bot.commands:
            cmds.append(x.name)
        return cmds
   
   
    @ipc.server.route()
    async def get_cmd_desc(self, data):
        desc = []
        for x in self.bot.commands:
            desc.append(x.description)
        return desc


    @ipc.server.route()
    async def get_guild_count(self, data):
        return self.bot.server


    @ipc.server.route()
    async def get_uptime(self, ctx, data):
        delta_uptime = datetime.utcnow() - self.bot.uptime
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        uptime = f"{days}d, {hours}h, {minutes}m, {seconds}s"
        return uptime


def setup(bot):
    bot.add_cog(IpcRoutes(bot))