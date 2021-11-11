from nextcord.ext import commands

class servers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def list_servers(self, ctx):
        from db import mysql
        conn = mysql.connect()
        
        cur = conn.cursor()
        # Delete voter database entry if the vote is older than 12 h
        cur.execute("SELECT * FROM servers ORDER BY votes DESC")
        serverdata = cur.fetchall()
        cur.close()
        conn.commit()
        
        for servername in serverdata:
            await ctx.send(servername)
        
def setup(bot):
    bot.add_cog(servers(bot))