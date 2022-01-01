from nextcord import Client, Interaction, SlashOption, ChannelType
import nextcord
from nextcord.abc import GuildChannel
from nextcord.ext import commands


import os
TESTING_GUILD_ID = 920436093734772736
intents = nextcord.Intents.default()
intents.members = True

print(nextcord.Intents().all())
# While slash commands work with Bot from ext.commands, this is a basic slash example and thus, we use Client.
client = commands.Bot(command_prefix='&', intents=intents)

@client.event
async def on_ready():
    print("Slash template is up and running!")



@client.slash_command(name='ban',guild_ids=[TESTING_GUILD_ID], description='bon 🔨')
async def ban(interaction: Interaction, user: nextcord.Member, reason):
  if interaction.user.guild_permissions.ban_members == True:
    print(user.name)
    await user.send('You got banned in ' + interaction.guild.name)
    await user.ban(reason=reason)

    await interaction.response.send_message(
        "Banned " + user.name + '.'
    )
  else:
    await interaction.response.send_message(
      'You do not have the necessary permissions for this action'
    )


@client.slash_command(name='unban',guild_ids=[TESTING_GUILD_ID], description='Unbans a user using their id.')
async def unban(interaction: Interaction, id, reason):
  if interaction.user.guild_permissions.ban_members:
    username = await client.fetch_user(id)
    await interaction.guild.unban(username)


    await interaction.response.send_message(
        "Unbanned " + username.name + '.'
    )
  else:
    await interaction.response.send_message(
      'You do not have the necessary permissions for this action'
    )

@client.slash_command(name='ping', guild_ids=[TESTING_GUILD_ID], description='Pong!🏓')
async def ping(interaction : Interaction):
  em = nextcord.Embed(title="Pong!🏓", colour=nextcord.Colour.random())
  em.add_field(
      name="My API Latency is:", value=f"{round(client.latency*1000)} ms!"
  )
  em.set_footer(
      text=f"Ping requested by {interaction.user}", icon_url=interaction.user.display_avatar
  )
  await interaction.response.send_message(
    embed=em
  )
token = open('token.txt')



client.run(str(token.read()))