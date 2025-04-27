import requests
import json
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
    def process_emoji_data(emoji_data):
        """Process emoji data to a consistent format"""
        processed_data = []

        for emoji in emoji_data:
            name = emoji.get('name', '')
            category = emoji.get('category', '')
            group = emoji.get('group', '')
            html_code = emoji.get('htmlCode', [''])[0] if emoji.get('htmlCode') else ''
            unicode = emoji.get('unicode', [''])[0] if emoji.get('unicode') else ''

            processed_data.append({
                'name': name,
                'category': category,
                'group': group,
                'html_code': html_code,
                'unicode': unicode,
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
