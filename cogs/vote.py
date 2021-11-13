from nextcord.ext import commands

class vote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(description="Vote for the server you send the message in")
    async def vote_server(self, ctx):
        dc_serverid = ctx.message.guild.id
        user = ctx.message.author.id
        
        #Import db
        from db import mysql

        conn = mysql.connect()
        
        cur = conn.cursor()
        # Delete voter database entry if the vote is older than 12 h
        cur.execute("DELETE FROM `user_votes` WHERE `voted_time` < ADDDATE(NOW(), INTERVAL -12 HOUR)")
        cur.close()
        conn.commit()
        
        cur = conn.cursor()
        # look if the user is in the vote database
        cur.execute("SELECT voted FROM user_votes WHERE dcuserid = (%s)", (user))
        voted = cur.fetchall()
        cur.close()

        if voted:
            await ctx.send('You already voted in the past 12 hours')
        
        else:
            cur = conn.cursor()
            cur.execute('SELECT * FROM servers WHERE discordserverid = (%s)', (dc_serverid))
            serversql = cur.fetchall()
            cur.close()

            if not serversql:
                await ctx.send ('LOL This server is not registered')

            else:
                cur = conn.cursor()
                cur.execute('UPDATE servers SET votes = votes + 1 WHERE discordserverid = %s',(dc_serverid))
                cur.close()

                cur = conn.cursor()
                cur.execute("INSERT INTO user_votes(dcuserid, voted, voted_time) VALUES (%s,%s, CURRENT_TIMESTAMP)", (user, dc_serverid))
                cur.close()
                conn.commit()
                conn.close()
                
                await ctx.send('You successfully voted for your favorite server ❤️')
                serversql.pop(0)

def setup(bot):
    bot.add_cog(vote(bot))