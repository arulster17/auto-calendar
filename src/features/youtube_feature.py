"""
YouTube Download Feature

Allows users to download YouTube videos as MP3 (audio) or MP4 (video).
Supports multiple URLs in a single request.
"""

import os
import re
import tempfile
import json
from pathlib import Path
import discord
import yt_dlp
from google import genai

# Lazy-load client to ensure env vars are loaded first
_client = None

def _get_client():
    """Get or create the Gemini client"""
    global _client
    if _client is None:
        api_key = os.getenv('GOOGLE_GEMINI_API_KEY')
        if not api_key:
            raise ValueError(
                "GOOGLE_GEMINI_API_KEY not found in environment variables. "
                "Please set it in your .env file."
            )
        _client = genai.Client(api_key=api_key)
    return _client


class YouTubeFeature:
    """
    Downloads YouTube videos as MP3 or MP4.
    """

    def __init__(self):
        self.name = "YouTube Downloader"
        self.description = "Download YouTube videos as audio (MP3) or video (MP4)"

        # Create temp directory for downloads
        self.temp_dir = Path(tempfile.gettempdir()) / "alfred_youtube"
        self.temp_dir.mkdir(exist_ok=True)

    def get_capabilities(self):
        """
        Describe what this feature can do for AI routing.
        """
        return """
        Download YouTube videos in different formats:
        - Convert YouTube videos to MP3 (audio only)
        - Download YouTube videos as MP4 (video with audio)
        - Handle multiple YouTube URLs at once
        - Supports various YouTube URL formats (youtube.com, youtu.be, etc.)

        Example requests:
        - "download this as mp3: https://youtube.com/watch?v=..."
        - "convert to mp3: [youtube link]"
        - "download as mp4: [youtube link]"
        - "get me the audio from [link]"
        - "download these videos as mp3: [link1] [link2]"
        - "convert these to mp4: [multiple links]"
        """

    async def handle(self, message, message_text, context=None):
        """
        Handle YouTube download requests.

        Args:
            message: Discord message object
            message_text: The user's message text
            context: Optional conversation context

        Returns:
            str: Response message
        """
        try:
            # Use AI to parse the request
            parsed = await self._parse_request(message_text, context)

            if not parsed.get('urls'):
                return "I couldn't find any YouTube URLs in your message. Please include at least one YouTube link."

            urls = parsed['urls']
            format_type = parsed.get('format', 'mp3').lower()  # Default to mp3

            if format_type not in ['mp3', 'mp4']:
                return f"Sorry, I can only convert to MP3 or MP4 format. You requested: {format_type}"

            # Validate URL count
            if len(urls) > 5:
                return "I can download up to 5 videos at once. Please try again with fewer URLs."

            # Send initial response
            if len(urls) == 1:
                await message.channel.send(f"⏳ Downloading as {format_type.upper()}... This may take a moment.")
            else:
                await message.channel.send(f"⏳ Downloading {len(urls)} videos as {format_type.upper()}... This may take a moment.")

            # Download each URL
            downloaded_files = []
            errors = []

            for url in urls:
                try:
                    file_path = await self._download_video(url, format_type)
                    downloaded_files.append(file_path)
                except Exception as e:
                    errors.append(f"Failed to download {url}: {str(e)}")

            # Send files to user via Discord
            if downloaded_files:
                for file_path in downloaded_files:
                    try:
                        # Check file size (Discord limit: 25MB for free users)
                        file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB

                        if file_size > 25:
                            await message.channel.send(
                                f"⚠️ File too large ({file_size:.1f}MB): {Path(file_path).name}\n"
                                f"Discord's limit is 25MB for free users."
                            )
                        else:
                            # Send file
                            with open(file_path, 'rb') as f:
                                await message.channel.send(
                                    file=discord.File(f, filename=Path(file_path).name)
                                )
                    except Exception as e:
                        errors.append(f"Failed to send file: {str(e)}")
                    finally:
                        # Clean up temp file
                        try:
                            os.remove(file_path)
                        except:
                            pass

            # Build response message
            if downloaded_files and not errors:
                return f"✅ Successfully downloaded {len(downloaded_files)} file(s)!"
            elif downloaded_files and errors:
                return f"⚠️ Downloaded {len(downloaded_files)} file(s), but encountered {len(errors)} error(s):\n" + "\n".join(errors)
            else:
                return f"❌ Failed to download any files:\n" + "\n".join(errors)

        except Exception as e:
            return f"❌ Error processing your request: {str(e)}"

    async def _parse_request(self, message_text, context=None):
        """
        Use AI to parse the download request and extract URLs and format preference.

        Args:
            message_text: User's message
            context: Conversation context

        Returns:
            dict: {'urls': [list of URLs], 'format': 'mp3' or 'mp4'}
        """
        # Format context if available
        context_str = ""
        if context:
            context_str = "\nRecent conversation:\n"
            for timestamp, role, msg in context:
                role_label = "User" if role == "user" else "Alfred"
                context_str += f"{role_label}: {msg}\n"
            context_str += "\n"

        prompt = f"""
{context_str}
User message: "{message_text}"

Extract the following information:
1. All YouTube URLs (youtube.com, youtu.be, etc.)
2. Desired format: MP3 (audio) or MP4 (video)

If the user doesn't specify a format:
- Default to MP3 if they mention "audio", "song", "music", "mp3"
- Default to MP4 if they mention "video", "mp4"
- Otherwise default to MP3

Return ONLY valid JSON:
{{
  "urls": ["url1", "url2", ...],
  "format": "mp3" or "mp4"
}}

Examples:
User: "download as mp3: https://youtube.com/watch?v=abc"
Response: {{"urls": ["https://youtube.com/watch?v=abc"], "format": "mp3"}}

User: "convert to mp4: https://youtu.be/xyz"
Response: {{"urls": ["https://youtu.be/xyz"], "format": "mp4"}}

User: "get the audio from these: [link1] [link2]"
Response: {{"urls": ["link1", "link2"], "format": "mp3"}}
"""

        try:
            client = _get_client()
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            response_text = response.text.strip()

            # Clean up response (remove markdown if present)
            if response_text.startswith('```json'):
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif response_text.startswith('```'):
                response_text = response_text.split('```')[1].split('```')[0].strip()

            # Parse JSON
            result = json.loads(response_text)

            return result

        except Exception as e:
            print(f"Error parsing download request with AI: {e}")
            # If AI parsing fails completely, we can't reliably extract intent
            # Return empty to trigger error message to user
            return {'urls': [], 'format': 'mp3'}

    async def _download_video(self, url, format_type):
        """
        Download video using yt-dlp.

        Args:
            url: YouTube URL
            format_type: 'mp3' or 'mp4'

        Returns:
            str: Path to downloaded file
        """
        output_template = str(self.temp_dir / '%(title)s.%(ext)s')

        if format_type == 'mp3':
            # Audio only
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': output_template,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'quiet': True,
                'no_warnings': True,
            }
        else:
            # Video with audio
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': output_template,
                'quiet': True,
                'no_warnings': True,
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Download and get info
            info = ydl.extract_info(url, download=True)

            # Get the actual filename
            if format_type == 'mp3':
                filename = ydl.prepare_filename(info).rsplit('.', 1)[0] + '.mp3'
            else:
                filename = ydl.prepare_filename(info)

            return filename
