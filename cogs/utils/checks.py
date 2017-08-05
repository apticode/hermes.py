import discord.utils
from discord.ext import commands

# Credits for this goes to tuxbot which can be found at:
# https://github.com/outout14/tuxbot-bot

def is_owner_check(message):
    owner = message.author.id in ['216666694582534145', '184361521558716418']
    return owner  # Owner of the bot


def is_owner(warn=True):
    def check(ctx, warn):
        owner = is_owner_check(ctx.message)
        if not owner and warn:
                print(ctx.message.author.name + "You are not the owner" + ctx.message.content)
        return owner

    owner = commands.check(lambda ctx: check(ctx, warn))
    return owner


def check_permissions(ctx, perms):
    msg = ctx.message
    if is_owner_check(msg):
        return True

    ch = msg.channel
    author = msg.author
    resolved = ch.permissions_for(author)
    return all(getattr(resolved, name, None) == value for name, value in perms.items())


def role_or_permissions(ctx, check, **perms):
    if check_permissions(ctx, perms):
        return True

    ch = ctx.message.channel
    author = ctx.message.author
    if ch.is_private:
        return False  # can't have roles in PMs

    role = discord.utils.find(check, author.roles)
    return role is not None


def admin_or_permissions(**perms):
    def predicate(ctx):
        return role_or_permissions(ctx, lambda r: r.name == 'Bot Admin', **perms)

    return commands.check(predicate)


def is_in_servers(*server_ids):
    def predicate(ctx):
        server = ctx.message.server
        if server is None:
            return False
        return server.id in server_ids

    return commands.check(predicate)