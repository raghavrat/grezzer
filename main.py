from nextcord import Client, Interaction, SlashOption, ChannelType
import nextcord
from nextcord.abc import GuildChannel
from nextcord.ext import commands
import datetime
import humanfriendly

import os
testingServers = [920436093734772736, 895791228921192459, 926508489487044628]
intents = nextcord.Intents.default()
intents.members = True

print(nextcord.Intents().all())
# While slash commands work with Bot from ext.commands, this is a basic slash example and thus, we use Client.
client = commands.Bot(command_prefix='&', intents=intents)
client.remove_command("help")



@client.command()
async def help(ctx):
    await ctx.send('Please use slash comands.')


@client.event
async def on_ready():
    print("Slash template is up and running!")



@client.slash_command(name='ban',guild_ids=testingServers, description='bon 🔨')
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


@client.slash_command(name='unban',guild_ids=testingServers, description='Unbans a user using their id.')
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

@client.slash_command(name='ping', guild_ids=testingServers, description='Pong!🏓')
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
@client.slash_command(name='mute', guild_ids=testingServers, description='Mutes a user for a given amount of time')
async def mute(interaction: Interaction, user: nextcord.Member, time, reason):
    if interaction.user.guild_permissions.moderate_members:
        timeSeconds = humanfriendly.parse_timespan(time)
        await interaction.response.send_message(f'{user} has been muted successfully.')
        await user.edit(timeout=nextcord.utils.utcnow()+datetime.timedelta(seconds=timeSeconds))
        await user.send(f'You have been muted in {interaction.guild.name} by {interaction.user} for {time} for {reason}')
    else:
        await interaction.response.send_message('You do not have the necessay permissions for this command.', ephemeral = True)

@client.slash_command(name='unmute', guild_ids=testingServers, description='Unmutes a user')
async def unmute(interaction: Interaction, user: nextcord.Member, reason):
    if interaction.user.guild_permissions.moderate_members:
        await interaction.response.send_message(f'{user} has been unmuted successfully.')
        await user.edit(timeout=None)
        await user.send(f'You have been unmuted in {interaction.guild.name} by {interaction.user} for {reason}')
    else:
        await interaction.response.send_message('You do not have the necessay permissions for this command.', ephemeral = True)

@client.slash_command(name='github', description='Gives you the github link.', guild_ids=testingServers)
async def github(interaction: Interaction):
    await interaction.response.send_message('https://github.com/doggysir/grezzer', ephemeral = True)


token = open('token.txt')



client.run(str(token.read()))