import requests
import json
import re
from .models import Emoji


class EmojiService:
    BASE_URL = "https://emojihub.yurace.pro/api"

    @staticmethod
    def fetch_all_emojis():
        """Fetch all emojis from the API"""
        try:
            response = requests.get(f"{EmojiService.BASE_URL}/all")
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"Error fetching emojis: {e}")
            return []

    @staticmethod
    def fetch_by_category(category):
        """Fetch emojis by category"""
        try:
            # URL encode the category and replace spaces with hyphens
            formatted_category = category.lower().replace(' ', '-')
            response = requests.get(f"{EmojiService.BASE_URL}/category/{formatted_category}")
            if response.status_code == 200:
                return response.json()
            # If the direct category fetch fails, filter from all emojis
            all_emojis = EmojiService.fetch_all_emojis()
            return [emoji for emoji in all_emojis if category.lower() in emoji.get('category', '').lower()]
        except Exception as e:
            print(f"Error fetching emojis by category: {e}")
            return []

    @staticmethod
    def fetch_by_group(group):
        """Fetch emojis by group"""
        try:
            response = requests.get(f"{EmojiService.BASE_URL}/group/{group}")
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"Error fetching emojis by group: {e}")
            return []

    @staticmethod
    def search_emojis(query, emojis):
        """Search emojis by name"""
        if not query:
            return emojis

        query = query.lower()
        return [emoji for emoji in emojis if query in emoji.get('name', '').lower()]

    @staticmethod
    def sort_emojis(emojis, sort_by='name'):
        """Sort emojis by the given field"""
        if sort_by == 'name':
            return sorted(emojis, key=lambda x: x.get('name', '').lower())
        elif sort_by == 'category':
            return sorted(emojis, key=lambda x: x.get('category', '').lower())
        return emojis

    @staticmethod
    def unicode_to_character(unicode_str):
        """Convert Unicode code point string to actual character"""
        if not unicode_str:
            return ""

        # Remove 'U+' prefix and split by space if there are multiple code points
        code_points = unicode_str.replace('U+', '')
        if ' ' in code_points:
            code_points = code_points.split(' ')
        else:
            code_points = [code_points]

        # Convert each code point to character and join
        try:
            return ''.join([chr(int(cp, 16)) for cp in code_points])
        except ValueError:
            return unicode_str  # Return original if conversion fails

    @staticmethod
    def process_emoji_data(emoji_data):
        """Process emoji data to a consistent format"""
        processed_data = []

        for emoji in emoji_data:
            name = emoji.get('name', '')
            category = emoji.get('category', '')
            group = emoji.get('group', '')
            html_code = emoji.get('htmlCode', [''])[0] if emoji.get('htmlCode') else ''

            # Get unicode and convert to actual character
            unicode_raw = emoji.get('unicode', [''])[0] if emoji.get('unicode') else ''
            unicode_char = EmojiService.unicode_to_character(unicode_raw)

            processed_data.append({
                'name': name,
                'category': category,
                'group': group,
                'html_code': html_code,
                'unicode': unicode_raw,  # Original unicode code point
                'unicode_char': unicode_char  # Actual unicode character
            })

        return processed_data

    @staticmethod
    def debug_api_response(endpoint):
        """Debug API response for a specific endpoint"""
        try:
            response = requests.get(f"{EmojiService.BASE_URL}/{endpoint}")
            print(f"Status code: {response.status_code}")
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error debugging API: {e}")
            return None
