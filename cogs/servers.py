from nextcord.ext import commands
import nextcord
import json
from decouple import config

class servers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    #TODO Make it display every server
    @commands.command(description="List all servers that are registered on the site")
    async def list_servers(self, ctx):
        from db import mysql

        conn = mysql.connect()

        cur = conn.cursor()
        # Delete voter database entry if the vote is older than 12 h
        cur.execute("SELECT servername,serverurl,votes FROM servers ORDER BY votes DESC")
        serverdata = cur.fetchall()
        cur.close()
        conn.commit()
        
        servername = [item['servername'] for item in serverdata]
        servervotes = [item['votes'] for item in serverdata]
        
        for servername in servername:
            print (servername)
        
        for votes in servervotes:
            print (votes)
            
        embed=nextcord.Embed(title="Osu! Server List", url="https://osulist.kitsu.cf", description="osu private servers, just one click away", color=0xffffff)

        embed.add_field(name="servename", value=servername, inline=True)
        embed.add_field(name="votes", value=votes, inline=True)

        await ctx.send(embed=embed)
        
def setup(bot):
    bot.add_cog(servers(bot))