import os
import requests
from discord.ext import commands


class Stardew(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.START_ENDPOINT = f"{os.environ['STARDEW_PROXMOX_VM']}/status/start"
        self.STOP_ENDPOINT = f"{os.environ['STARDEW_PROXMOX_VM']}/status/shutdown"

        self.HEADERS = {"Authorization": f'PVEAPIToken={os.environ["PROXMOX_TOKEN"]}'}

    @commands.command()
    async def sdvstart(self, ctx):
        await ctx.send("Starting Stardew Valley host...")

        try:
            resp = requests.post(
                self.START_ENDPOINT,
                headers=self.HEADERS,
                verify=False,
            )

            data = resp.json()["data"]
            if data != None:
                await ctx.send(
                    "Stardew Valley host has been started. Please wait 3-5 minutes for the server to start."
                )
        except Exception as e:
            print("Error starting Stardew Valley host: ", e)
            await ctx.send("Error starting Stardew Valley.")

    @commands.command()
    async def sdvstop(self, ctx):
        await ctx.send("Stopping Stardew Valley host...")

        try:
            resp = requests.post(
                self.STOP_ENDPOINT,
                headers=self.HEADERS,
                verify=False,
            )

            data = resp.json()["data"]
            if data != None:
                await ctx.send("Stardew Valley has been stopped.")
        except Exception as e:
            print("Error stopping Stardew Valley: ", e)
            await ctx.send("Error stopping Stardew Valley.")
