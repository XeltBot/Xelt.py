# Contributing

## Before Starting

Make sure to read these guides listed below

- [Installing Requirements](./installing-requirements.md)

## Design Principles

One of the major factors that led to Xelt's downfall is the fundamental lack of design principles. In order to ensure Xelt success, there must be some design principles that should be put in place. There are as listed:

- **Efficiency**: The efficiency of the code matters. The question that should be thought of when designing a new feature is what is the most efficient way that this algorithm can be done? When it comes to Discord bots, performance is key. Sure, you can use a different programming language like Go or Rust, and have increased performance that way, but another way to increase performance is simply optimizing the code itself.

- **Think before you code**: Programming isn't about just writing some code. Fundamentally, each new feature needs to be first designed, and prototyped before any code can be touched. First, before you start programming, get a sheet of paper out. This could be just any piece of paper, or it could be something like MSPaint. Then, design and think of every single step through. Consider the efficiency and the costs of the design. Then, write out any pseudo code on paper. Prototype a small scale version, which would be a proof of concept. Make sure to test all of the parts first, and test the integration of said parts. Then, once you think you have it set and everything works, then finally program the version that will go on the bot. This thought process is used in many software engineering industries. If you have taken AP CSA, you already know what I mean by this.

- **The end user**: Ultimately you are shipping your own product to your end users. Think about what it would feel like being said user. Would the commands work? Are their any flaws, or any parts that can be improved on? 

- **Testing**: There are unit tests set up for a reason... Unit testing and integration testing are 2 of the major building blocks to the success of any project.

## Coding Style

### Variables

Most of the code written uses `camelCasing` for variables, `PascalCasing` for classes, and `snake_casing` for ags. To sum it up:

- `camelCasing` for variables
- `PascalCasing` for classes
- `snake_casing` for args
- `ALL_CAPS` for constants
- `kebab-casing` for files

### Formatting

Xelt.py uses pre-commit hooks to format all of the code. Make sure run `git add --all` before committing to add all of the files. More than likely you'll need to commit twice due to the formatting that pre-commit does afterwards.

### Docstrings

Just like how major programs are documented, the libraries that are custom made for Xelt.py also have to be documented. The current standard for this project is to use [Google's Docstring format](https://google.github.io/styleguide/pyguide.html#s3.8-comments-and-docstrings). A handy VS Code extension that should be used is the [autoDocstring](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring) extension. By default it will generate the docstring in the Google format. Docstrings should be used on all coroutines and methods (excluding cogs), and on classes as well. 

For Cogs, docstrings formats are not needed. All you need to do is to add a basic docstring and discord.py will pick it up. Additionally for descriptions of slash command parameters, you can also use docstrings and discord.py will pick it up (see https://discordpy.readthedocs.io/en/stable/interactions/api.html#discord.app_commands.describe)

Example Cog:

```py 
import discord
from discord import app_commands
from discord.ext import commands

class MyCog(commands.Cog):
    """An example cog for demo purposes"""
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help")
    async def myCommand(self, interaction: discord.Interaction):
        """This is an example of a description for a slash command"""
        await interaction.response.send_message(f"Hello {ctx.user.name}!")

async def setup(bot):
    await bot.add_cog(MyCog(bot))
```

## GitHub Contributing Guidelines

### Releasing Tags
In order to automate the release system, you have to make sure that in order to use it, the git commit message must be done correctly. Only use this if there is a new update that is ready to be released. Xelt.py uses [SemVer](https://semver.org/) as the standard for versioning. Here's a table that should help with explaining this:

| Type of Release, Update, or Patch | Example |
|              :--:                 | :--:    | 
| Major Release (For updates that are not backwards compatible) | `Release: v2.0.0` | 
| Minor Release (For updates that are backwards compatible) | `Update: v2.5.0`|
| Patch Release (For critical security patches and bug fixes) | `Fix: v2.5.1` |
