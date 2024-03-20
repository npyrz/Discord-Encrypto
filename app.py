import discord
from discord.ext import commands
import os
from message import messageEncrypter, messageDecrypter, listAllDecrypts
from image import imageEncrypter, imageDecrypter, listAllKeys
from dotenv import load_dotenv 
load_dotenv()

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
@bot.event 
async def on_ready():
     print(f'We have logged in as {bot.user}')

@bot.command()
async def sync(ctx):
    await bot.tree.sync()
    await ctx.send("Synced!")

@bot.tree.command(name="encrypte-message", description="Enter a message to be encrypted")
async def load(ctx, message:str):
    username = ctx.user.name
    encryptedMessage = messageEncrypter(message, username)
    embed = discord.Embed(
        title="Encrypted Message",
        color=discord.Color.blue()
    )
    embed.add_field(name="Original Message:", value=message, inline=True)
    embed.add_field(name="Dencryption Key:", value="```"+encryptedMessage+"```", inline=False)
    embed.set_author(name=ctx.user.display_name, icon_url=ctx.user.display_avatar.url)
    embed.timestamp = ctx.created_at
    await ctx.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="encrypte-image", description="Enter an image URL to be encrypted (Must be a .png)")
async def load(ctx, url:str):
    username = ctx.user.name
    encryptedImage = imageEncrypter(url, username)
    fileImage = encryptedImage + ".png"
    embed = discord.Embed(
        title="Encrypted Image",
        color=discord.Color.blue()
    )
    image_path = os.path.join("imgs", fileImage)
    with open(image_path, "rb") as image_file:
        file = discord.File(image_file, filename="image.png")
    embed.add_field(name="Decryption Key:", value="```"+encryptedImage+"```", inline=True)
    embed.add_field(name="Decrypted Image:",value="", inline=False)
    embed.set_image(url="attachment://image.png")
    embed.set_thumbnail(url= url)
    embed.set_author(name=ctx.user.display_name, icon_url=ctx.user.display_avatar.url)
    embed.timestamp = ctx.created_at
    await ctx.response.send_message(embed=embed, file=file, ephemeral=True)

@bot.tree.command(name="decrypt-image", description="Enter the decryption key to get your orginal image")
async def load(ctx, encrypted_key:str):
    username = ctx.user.name
    dencryptedImage = imageDecrypter(encrypted_key, username)
    embed = discord.Embed(
        title="Decrypted Image",
        color=discord.Color.blue()
    )
    embed.add_field(name="Original Image:", value="", inline=True)
    embed.set_image(url=dencryptedImage)
    embed.set_author(name=ctx.user.display_name, icon_url=ctx.user.display_avatar.url)
    embed.timestamp = ctx.created_at
    embed2 = discord.Embed(
        title="Decrypted Image Error",
        color=discord.Color.blue(),
        description="The provided key is either invalid or not a key registered to your account."
    )
    embed2.set_author(name=ctx.user.display_name, icon_url=ctx.user.display_avatar.url)
    embed2.timestamp = ctx.created_at

    if (dencryptedImage == 'ERROR'):
        await ctx.response.send_message(embed=embed2, ephemeral=True)
    else:
        await ctx.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="decrypt-message", description="Enter the decrypted message to get the orginal message")
async def load(ctx, encrypted_message:str):
    username = ctx.user.name
    dencryptedMessage = messageDecrypter(encrypted_message, username)
    embed = discord.Embed(
        title="Decrypted Message",
        color=discord.Color.blue()
        )
    embed.add_field(name="Original Message:", value=f"`{dencryptedMessage}`", inline=True)
    embed.set_author(name=ctx.user.display_name, icon_url=ctx.user.display_avatar.url)
    embed.timestamp = ctx.created_at
    await ctx.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="image-keys", description="List of all your current image decryption keys.")
async def load(ctx):
    username = ctx.user.name
    listKeys = listAllKeys(username)
    embed = discord.Embed(
        title="Image Decryption Key List",
        color=discord.Color.blue()
        )
    embed.add_field(name="Keys:", value=f"```{listKeys}```", inline=True)
    embed.set_author(name=ctx.user.display_name, icon_url=ctx.user.display_avatar.url)
    embed.timestamp = ctx.created_at
    await ctx.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="message-keys", description="List of all your current message decryption keys.")
async def load(ctx):
    username = ctx.user.name
    listKeys = listAllDecrypts(username)
    embed = discord.Embed(
        title="Message Decryption Key List",
        color=discord.Color.blue()
        )
    embed.add_field(name="Keys:", value=f"```{listKeys}```", inline=True)
    embed.set_author(name=ctx.user.display_name, icon_url=ctx.user.display_avatar.url)
    embed.timestamp = ctx.created_at
    await ctx.response.send_message(embed=embed, ephemeral=True)

bot.run(os.getenv("TOKEN"))