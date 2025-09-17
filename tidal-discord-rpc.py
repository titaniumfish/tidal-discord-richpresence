#!/usr/bin/env python3
"""
Tidal Hi-Fi Discord Rich Presence for Linux
Connects to Tidal Hi-Fi's local API and updates Discord with currently playing track info
"""

import requests
import time
import json
import logging
from pypresence import Presence
from typing import Optional, Dict, Any
import sys

# Discord Application ID (you'll need to create this at https://discord.com/developers/applications)
DISCORD_CLIENT_ID = "1417674368380829776"

# Tidal Hi-Fi API configuration
TIDAL_API_BASE = "http://localhost:47836"
TIDAL_CURRENT_ENDPOINT = f"{TIDAL_API_BASE}/current"

# Configuration
UPDATE_INTERVAL = 15  # seconds between updates
CONNECT_RETRY_INTERVAL = 30  # seconds between Discord connection attempts

class TidalDiscordRPC:
    def __init__(self):
        self.discord_rpc = None
        self.last_track_data = None
        self.connected_to_discord = False
        
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Enable debug logging to see more details
        # Uncomment the line below for more verbose output
        # logging.getLogger().setLevel(logging.DEBUG)

    def connect_discord(self) -> bool:
        """Connect to Discord Rich Presence"""
        try:
            if self.discord_rpc:
                self.discord_rpc.close()
            
            self.discord_rpc = Presence(DISCORD_CLIENT_ID)
            self.discord_rpc.connect()
            self.connected_to_discord = True
            self.logger.info("Connected to Discord Rich Presence")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to connect to Discord: {e}")
            self.connected_to_discord = False
            return False

    def get_current_track(self) -> Optional[Dict[str, Any]]:
        """Get current track info from Tidal Hi-Fi API"""
        try:
            response = requests.get(TIDAL_CURRENT_ENDPOINT, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            # Check if we have valid track data
            if data.get('title') and data.get('artists'):
                return data
            else:
                return None
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to get track info from Tidal Hi-Fi: {e}")
            return None
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON response from Tidal Hi-Fi: {e}")
            return None

    def format_time(self, seconds: int) -> str:
        """Convert seconds to MM:SS format"""
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes}:{seconds:02d}"

    def update_discord_presence(self, track_data: Dict[str, Any]) -> bool:
        """Update Discord Rich Presence with track info"""
        if not self.connected_to_discord:
            return False

        try:
            # Extract track information
            title = track_data.get('title', 'Unknown Track')
            artists = track_data.get('artists', 'Unknown Artist')
            album = track_data.get('album', '')
            status = track_data.get('status', 'unknown')
            current_seconds = track_data.get('currentInSeconds', 0)
            duration_seconds = track_data.get('durationInSeconds', 0)
            playing_from = track_data.get('playingFrom', '')
            
            # Prepare presence data - start with minimal required fields
            presence_data = {
                'details': title,
                'state': f"by {artists}",
            }
            
            # Only add image assets if they exist (to avoid errors)
            # These need to be uploaded to Discord Developer Portal first
            try:
                presence_data.update({
                    'large_image': 'tidal_logo',
                    'large_text': 'Tidal Hi-Fi',
                    'small_image': 'play' if status == 'playing' else 'pause',
                    'small_text': 'Playing' if status == 'playing' else 'Paused'
                })
            except Exception as img_error:
                self.logger.warning(f"Image assets not available: {img_error}")
                # Continue without images

            # Add album info if available
            if album:
                presence_data['state'] = f"by {artists} • {album}"

            # Add playing source if available
            if playing_from:
                presence_data['large_text'] = f"Tidal Hi-Fi • {playing_from}"

            # Add timestamps for progress bar (only when playing)
            if status == 'playing' and duration_seconds > 0:
                current_time = time.time()
                start_time = current_time - current_seconds
                end_time = start_time + duration_seconds
                
                presence_data['start'] = int(start_time)
                presence_data['end'] = int(end_time)

            # Update Discord
            self.discord_rpc.update(**presence_data)
            
            # Add debugging information
            self.logger.debug(f"Sent presence data: {presence_data}")
            
            # Log the update
            time_info = ""
            if current_seconds and duration_seconds:
                time_info = f" [{self.format_time(current_seconds)}/{self.format_time(duration_seconds)}]"
            
            self.logger.info(f"Updated Discord: {title} by {artists} ({status}){time_info}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to update Discord presence: {e}")
            self.logger.error(f"Presence data that failed: {presence_data if 'presence_data' in locals() else 'N/A'}")
            self.connected_to_discord = False
            return False

    def clear_discord_presence(self):
        """Clear Discord Rich Presence"""
        if self.connected_to_discord and self.discord_rpc:
            try:
                self.discord_rpc.clear()
                self.logger.info("Cleared Discord presence")
            except Exception as e:
                self.logger.error(f"Failed to clear Discord presence: {e}")

    def has_track_changed(self, current_data: Dict[str, Any]) -> bool:
        """Check if track has changed since last update"""
        if not self.last_track_data:
            return True
            
        # Check key fields for changes
        current_key = (
            current_data.get('title'),
            current_data.get('artists'),
            current_data.get('status'),
            current_data.get('playingFrom')
        )
        
        last_key = (
            self.last_track_data.get('title'),
            self.last_track_data.get('artists'),
            self.last_track_data.get('status'),
            self.last_track_data.get('playingFrom')
        )
        
        return current_key != last_key

    def run(self):
        """Main run loop"""
        self.logger.info("Starting Tidal Hi-Fi Discord Rich Presence...")
        self.logger.info(f"Make sure Discord Client ID is set: {DISCORD_CLIENT_ID}")
        
        if DISCORD_CLIENT_ID == "YOUR_DISCORD_APP_ID_HERE":
            self.logger.error("Please set your Discord Application ID in the script!")
            sys.exit(1)

        last_discord_attempt = 0
        
        while True:
            try:
                # Try to connect to Discord if not connected
                current_time = time.time()
                if not self.connected_to_discord and (current_time - last_discord_attempt) > CONNECT_RETRY_INTERVAL:
                    self.connect_discord()
                    last_discord_attempt = current_time

                # Get current track info
                track_data = self.get_current_track()
                
                if track_data:
                    # Only update if track changed or status changed
                    if self.has_track_changed(track_data):
                        if self.connected_to_discord:
                            success = self.update_discord_presence(track_data)
                            if not success:
                                # Discord connection might be lost, try reconnecting next cycle
                                self.connected_to_discord = False
                        
                        self.last_track_data = track_data
                else:
                    # No track playing, clear presence if we had one
                    if self.last_track_data and self.connected_to_discord:
                        self.clear_discord_presence()
                        self.last_track_data = None

                time.sleep(UPDATE_INTERVAL)

            except KeyboardInterrupt:
                self.logger.info("Shutting down...")
                if self.connected_to_discord:
                    self.clear_discord_presence()
                break
            except Exception as e:
                self.logger.error(f"Unexpected error: {e}")
                time.sleep(UPDATE_INTERVAL)

        # Cleanup
        if self.discord_rpc:
            self.discord_rpc.close()

if __name__ == "__main__":
    rpc = TidalDiscordRPC()
    rpc.run()