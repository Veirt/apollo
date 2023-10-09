import os
import requests
import discord
from discord.ext import commands


def server_status_embed(
    ip: str, port: int, online_count: int | None, cachehit: bool, online: bool
):
    embed = discord.Embed()
    embed.add_field(name="Server", value=f"{ip}:{port}", inline=True)
    embed.add_field(name="Online", value=online, inline=True)
    if online_count != None:
        embed.add_field(name="Online Player", value=online_count, inline=False)

    return embed


class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.START_ENDPOINT = f"{os.environ['PROXMOX_VM']}/status/start"
        self.STOP_ENDPOINT = f"{os.environ['PROXMOX_VM']}/status/start"

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
        server_status_endpoint = (
            f"https://api.mcsrvstat.us/3/{os.environ['MINECRAFT_SERVER']}"
        )

        try:
            resp = requests.get(server_status_endpoint)

            data = resp.json()

            if data:
                players = data["players"]["online"] if "players" in data else None

                embed = server_status_embed(
                    data["ip"],
                    data["port"],
                    players,
                    data["debug"]["cachehit"],
                    data["online"],
                )

                await ctx.send(embed=embed)
            else:
                raise ValueError("Data is empty.")

        except Exception as e:
            print("Error when checking minecraft server status: ", e)
            await ctx.send("Error when checking minecraft server status.")
