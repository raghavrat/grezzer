# Grezzer Discord Bot

A Discord moderation bot built with Nextcord that provides essential moderation commands through slash commands.

## Commands

### Ban Command
**Usage:** `/ban [user] [reason]`

**Description:**
Permanently removes a user from the server. Sends them a DM notification about the ban and records the reason. Only users with ban permissions can use this command.

**Code Implementation:**
```python
@client.slash_command(name='ban', guild_ids=testingServers, description='bon 🔨')
async def ban(interaction: Interaction, user: nextcord.Member, reason):
    if interaction.user.guild_permissions.ban_members == True:
        await user.send('You got banned in ' + interaction.guild.name)
        await user.ban(reason=reason)
        await interaction.response.send_message("Banned " + user.name + '.')
    else:
        await interaction.response.send_message(
            'You do not have the necessary permissions for this action'
        )
```

### Unban Command
**Usage:** `/unban [user_id] [reason]`

**Description:**
Removes a ban from a previously banned user using their ID. Only users with ban permissions can use this command. The user can rejoin the server after being unbanned through a new invite.

**Code Implementation:**
```python
@client.slash_command(name='unban', guild_ids=testingServers, description='Unbans a user using their id.')
async def unban(interaction: Interaction, id, reason):
    if interaction.user.guild_permissions.ban_members:
        username = await client.fetch_user(id)
        await interaction.guild.unban(username)
        await interaction.response.send_message("Unbanned " + username.name + '.')
    else:
        await interaction.response.send_message(
            'You do not have the necessary permissions for this action'
        )
```

### Mute Command
**Usage:** `/mute [user] [time] [reason]`

**Description:**
Temporarily prevents a user from sending messages or joining voice channels. Accepts human-readable time formats (e.g., "1h", "30m", "1d"). Sends a DM to the user with mute duration and reason. Only users with moderation permissions can use this command.

**Code Implementation:**
```python
@client.slash_command(name='mute', guild_ids=testingServers, description='Mutes a user for a given amount of time')
async def mute(interaction: Interaction, user: nextcord.Member, time, reason):
    if interaction.user.guild_permissions.moderate_members:
        timeSeconds = humanfriendly.parse_timespan(time)
        await interaction.response.send_message(f'{user} has been muted successfully.')
        await user.edit(timeout=nextcord.utils.utcnow()+datetime.timedelta(seconds=timeSeconds))
        await user.send(f'You have been muted in {interaction.guild.name} by {interaction.user} for {time} for {reason}')
    else:
        await interaction.response.send_message('You do not have the necessay permissions for this command.', ephemeral = True)
```

### Unmute Command
**Usage:** `/unmute [user] [reason]`

**Description:**
Removes a timeout from a muted user, allowing them to send messages and join voice channels again. Sends a DM to the user informing them of the unmute. Only users with moderation permissions can use this command.

**Code Implementation:**
```python
@client.slash_command(name='unmute', guild_ids=testingServers, description='Unmutes a user')
async def unmute(interaction: Interaction, user: nextcord.Member, reason):
    if interaction.user.guild_permissions.moderate_members:
        await interaction.response.send_message(f'{user} has been unmuted successfully.')
        await user.edit(timeout=None)
        await user.send(f'You have been unmuted in {interaction.guild.name} by {interaction.user} for {reason}')
    else:
        await interaction.response.send_message('You do not have the necessay permissions for this command.', ephemeral = True)
```

### Ping Command
**Usage:** `/ping`

**Description:**
Checks the bot's response time by displaying the API latency in milliseconds. Creates an embed with the latency information and the user who requested it. This command can be used by any member.

**Code Implementation:**
```python
@client.slash_command(name='ping', guild_ids=testingServers, description='Pong!🏓')
async def ping(interaction: Interaction):
    em = nextcord.Embed(title="Pong!🏓", colour=nextcord.Colour.random())
    em.add_field(
        name="My API Latency is:", value=f"{round(client.latency*1000)} ms!"
    )
    em.set_footer(
        text=f"Ping requested by {interaction.user}", icon_url=interaction.user.display_avatar
    )
    await interaction.response.send_message(embed=em)
```

### Github Command
**Usage:** `/github`

**Description:**
Provides the link to the bot's GitHub repository. The response is only visible to the user who ran the command (ephemeral message).

**Code Implementation:**
```python
@client.slash_command(name='github', description='Gives you the github link.', guild_ids=testingServers)
async def github(interaction: Interaction):
    await interaction.response.send_message('https://github.com/doggysir/grezzer', ephemeral = True)
```

## Installation and Setup

### 1. Clone the Repository
```bash
git clone github.com:raghavrat/grezzer.git
cd grezzer
```

### 2. Install Required Libraries
```bash
pip install nextcord humanfriendly
```

### 3. Discord Bot Setup
1. Create a new application at [Discord Developer Portal](https://discord.com/developers/applications)
2. Go to the Bot section and create a bot
3. Enable these Privileged Gateway Intents:
   - PRESENCE INTENT
   - SERVER MEMBERS INTENT
   - MESSAGE CONTENT INTENT
4. Create a `token.txt` file in the project root
5. Copy your bot token and paste it in `token.txt`
6. Invite the bot to your server using the OAuth2 URL generator:
   - Select `bot` and `applications.commands` scopes
   - Select required permissions (Admin recommended for all features)

### 4. Run the Bot
```bash
python main.py
```

## Required Permissions

The bot requires these permissions for full functionality:
- `Ban Members` - For ban/unban commands
- `Moderate Members` - For mute/unmute commands
- `Send Messages` - For command responses
- `Use Slash Commands` - For all commands
- `View Channels` - For basic functionality

## Features

- Modern Slash Commands
- Permission-based command access
- DM notifications for moderation actions
- Human-readable time formats for mutes
- Embedded messages for better presentation
- API latency checking
- Error handling and permission checking
- Easy-to-use moderation commands

## Configuration

### Server IDs
Add your server IDs to the `testingServers` list:
```python
testingServers = [
    YOUR_SERVER_ID_1,
    YOUR_SERVER_ID_2,
    # Add more servers as needed
]
```

### Command Prefix
The bot uses `&` as its prefix for legacy commands:
```python
client = commands.Bot(command_prefix='&', intents=intents)
```

## Error Handling

The bot includes error handling for:
- Missing permissions
- Invalid user IDs
- Invalid time formats
- Failed DM deliveries
- API communication errors
