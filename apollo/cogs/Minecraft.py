import os
import requests
import discord
from discord.ext import commands
from mcstatus import JavaServer


def server_status_embed(server: str, online: bool, online_count: int | None = 0):
    embed = discord.Embed()
    embed.add_field(name="Server", value=server, inline=True)
    embed.add_field(name="Online", value=online, inline=True)
    if online:
        embed.add_field(name="Online Player", value=online_count, inline=False)

    return embed


class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.START_ENDPOINT = f"{os.environ['PROXMOX_VM']}/status/start"
        self.STOP_ENDPOINT = f"{os.environ['PROXMOX_VM']}/status/stop"

        self.HEADERS = {"Authorization": f'PVEAPIToken={os.environ["PROXMOX_TOKEN"]}'}

    @commands.command()
    async def mcstart(self, ctx):
        await ctx.send("Starting minecraft server...")

        try:
            resp = requests.post(
                self.START_ENDPOINT,
                headers=self.HEADERS,
                verify=False,
            )

            data = resp.json()["data"]
            if data != None:
                await ctx.send("Minecraft server started!")
        except Exception as e:
            print("Error starting minecraft server: ", e)
            await ctx.send("Error starting minecraft server.")

    @commands.command()
    async def mcstop(self, ctx):
        await ctx.send("Stopping minecraft server...")

        try:
            resp = requests.post(
                self.STOP_ENDPOINT,
                headers=self.HEADERS,
                verify=False,
            )

            data = resp.json()["data"]
            if data != None:
                await ctx.send("Minecraft server stopped!")
        except Exception as e:
            print("Error stopping minecraft server: ", e)
            await ctx.send("Error stopping minecraft server.")

    @commands.command()
    async def mcstatus(self, ctx):
        server = JavaServer.lookup(os.environ["MINECRAFT_SERVER"])

        try:
            status = server.status()
            embed = server_status_embed(
                os.environ["MINECRAFT_SERVER"], True, status.players.online
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = server_status_embed(os.environ["MINECRAFT_SERVER"], False)
            print("Error when checking server status:", e)
            await ctx.send(embed=embed)
            return

        if status.players.online > 0:
            player_embed = discord.Embed()
            query = server.query()
            players = query.players.names
            player_embed.add_field(
                name="Online Player(s)", value="\n".join(players), inline=False
            )
            await ctx.send(embed=player_embed)
