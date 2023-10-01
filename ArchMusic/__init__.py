#
# Copyright (C) 2021-2023 by ArchBots@Github, < https://github.com/ArchBots >.
#
# This file is part of < https://github.com/ArchBots/ZenMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/ArchBots/ZenMusic/blob/master/LICENSE >
#
# All rights reserved.
#

from ZenMusic.core.bot import ZenMusic
from ZenMusic.core.dir import dirr
from ZenMusic.core.git import git
from ZenMusic.core.userbot import Userbot
from ZenMusic.misc import dbb, heroku, sudo

from .logging import LOGGER

# Directories
dirr()

# Check Git Updates
git()

# Initialize Memory DB
dbb()

# Heroku APP
heroku()

# Load Sudo Users from DB
sudo()

# Bot Client
app = ZenMusic()

# Assistant Client
userbot = Userbot()

from .platforms import *

YouTube = YouTubeAPI()
Carbon = CarbonAPI()
Spotify = SpotifyAPI()
Apple = AppleAPI()
Resso = RessoAPI()
SoundCloud = SoundAPI()
Telegram = TeleAPI()
