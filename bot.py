import discord
import aiohttp
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

bot = commands.Bot(command_prefix=os.getenv("PREFIX"), case_insensitive=True)


@bot.event
async def on_ready():
    print("Weather Bot is ready")


@bot.command(help="Gives you the weather information to any place in the world", aliases=["w"])
async def weather(ctx, *, query):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.openweathermap.org/data/2.5/weather?q={query}&appid={os.getenv("APIKEY")}&units=metric') as response:
                if int(response.status) == 429:
                    await ctx.send("The api has received too many requests and has been rate limited.")
                elif int(response.status) != 200:
                    await ctx.send("Something went wrong with the request. Please check for any errors in the command sent.")
                    return
                data = await response.json()
                embed = discord.Embed(title=f"Weather", description=f"Detailed weather for the place {data['name']}, {data['sys']['country']}", color=discord.Color.blue())
                embed.set_thumbnail(url=f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png")
                embed.add_field(name="Coordinates", value=f"Longitude: {data['coord']['lon']}\nLatitude: {data['coord']['lat']}", inline=False)
                embed.add_field(name="Temperature", value=f"Temperature: {data['main']['temp']}°C\nLowest temp: {data['main']['temp_min']}°C\nHighest temp: {data['main']['temp_max']}°C", inline=False)
                embed.add_field(name="Wind", value=f"Speed: {data['wind']['speed']}m/s\nDirection: {data['wind']['deg']}°", inline=False)
                embed.add_field(name="Other", value=f"Pressure: {data['main']['pressure']}hPa\nHumidity: {data['main']['humidity']}%\nCloudiness: {data['clouds']['all']}%\nVisibility: {data['visibility']}m", inline=False)
                await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send("Something went wrong with the request. Please check for any errors in the command sent.")

bot.run(os.getenv("TOKEN"))
