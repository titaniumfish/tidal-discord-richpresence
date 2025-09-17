# Tidal Hi-Fi Discord Rich Presence

A Python script that displays your currently playing Tidal Hi-Fi music in Discord as a Rich Presence status. Shows the song title, artist, album, and real-time playback progress.

![Discord Rich Presence Example](https://img.shields.io/badge/Discord-Rich%20Presence-7289DA?style=for-the-badge&logo=discord&logoColor=white)

## Features

- 🎵 **Real-time music display** - Shows currently playing track in Discord
- ⏱️ **Live progress tracking** - Displays current playback position and total duration
- 🎮 **Rich Presence integration** - Native Discord status with song details
- 🔄 **Auto-updates** - Refreshes every 15 seconds with current track info
- ⏸️ **Play/pause detection** - Shows when music is paused or playing

## Prerequisites

1. **Tidal Hi-Fi** - Must be running and accessible at `http://localhost:47836` (or change this if you run the local API on a different port)
2. **Discord Desktop** - Rich Presence only works on Discord desktop client
3. **Python 3.6+** - Required for running the script

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/titaniumfish/tidal-discord-richpresence.git
   cd tidal-discord-richpresence
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Enable Discord Rich Presence**
   - Open Discord → Settings → Activity Privacy
   - Enable "Display currently running game as a status message"

## Usage

### Quick Start

```bash
python3 tidal-discord-rpc.py
```

## Example Output

```
❯ python3 tidal-discord-rpc.py
2025-09-17 11:19:23,499 - INFO - Starting Tidal Hi-Fi Discord Rich Presence...
2025-09-17 11:19:23,517 - INFO - Connected to Discord Rich Presence
2025-09-17 11:19:23,567 - INFO - Updated Discord: Song 2 by Blur (playing) [1:06/2:01]
2025-09-17 11:20:23,631 - INFO - Updated Discord: Pretty Fly (For A White Guy) by The Offspring (playing) [0:04/3:08]
2025-09-17 11:22:39,026 - INFO - Updated Discord: Pretty Fly (For A White Guy) by The Offspring (paused) [2:16/3:08]
2025-09-17 11:22:54,045 - INFO - Updated Discord: Pretty Fly (For A White Guy) by The Offspring (playing) [2:23/3:08]
2025-09-17 11:23:39,171 - INFO - Updated Discord: First Date by blink-182 (playing) [0:05/2:51]
```

## What You'll See in Discord

Your Discord status will show:
- **Status**: "Playing Tidal Hi-Fi"
- **Details**: Song title
- **State**: "by Artist • Album"
- **Progress bar**: Live playback position (when playing)
- **Icons**: Tidal logo and play/pause status indicator

## Configuration

### Custom Discord Application

If you want to use your own Discord application:

1. Create a new application at [Discord Developer Portal](https://discord.com/developers/applications)
2. Copy the Application ID
3. Replace `DISCORD_CLIENT_ID` in the script with your ID
4. Upload these images (512x512 or 1024x1024 recommended):
   - `tidal_logo` - Main Tidal/music icon
   - `play` - Play button icon
   - `pause` - Pause button icon

### Script Configuration

You can modify these settings in the script:

```python
# Update frequency (seconds)
UPDATE_INTERVAL = 15

# Tidal Hi-Fi API endpoint
TIDAL_API_BASE = "http://localhost:47836"

# Discord Application ID
DISCORD_CLIENT_ID = "1417674368380829776"
```

## Contributing

I knocked this together quickly as i couldnt find something that did exactly what i wanted, but if you want, feel free to submit issues or pull requests.

## License

This project is open source. Feel free to use, modify, and distribute.

## Acknowledgments

- [Tidal Hi-Fi](https://github.com/Mastermindzh/tidal-hifi) - For providing the local API
- [pypresence](https://github.com/qwertyquerty/pypresence) - Discord Rich Presence library
- Discord Developer Platform - For Rich Presence support

---

**Note**: This script is not affiliated with Tidal or Discord. It's a community project for enhancing your music listening experience.