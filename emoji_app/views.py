from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import logout, login
from django.contrib import messages
from .services import EmojiService
from .models import Emoji, Favorite
from .forms import SignUpForm


def home(request):
    """Home page view"""
    return render(request, 'emoji_app/home.html')


def emoji_catalog(request):
    """Emoji catalog view"""
    # Get query parameters
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort_by', 'name')
    category_filter = request.GET.get('category', '')
    display_style = request.GET.get('style', 'native')

    # Fetch emojis from service
    emoji_service = EmojiService()

    # Always fetch all emojis first
    emoji_data = emoji_service.fetch_all_emojis()

    # Then filter by category if specified
    if category_filter:
        emoji_data = [emoji for emoji in emoji_data if category_filter.lower() in emoji.get('category', '').lower()]

    # Search emojis
    if search_query:
        emoji_data = emoji_service.search_emojis(search_query, emoji_data)

    # Sort emojis
    emoji_data = emoji_service.sort_emojis(emoji_data, sort_by)

    # Process emoji data
    emojis = emoji_service.process_emoji_data(emoji_data)

    # Get unique categories for filter dropdown
    categories = set(emoji['category'] for emoji in emojis)

    # Get user's favorites if logged in
    favorites = []
    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(user=request.user).values_list('emoji__name', flat=True)

    context = {
        'emojis': emojis,
        'search_query': search_query,
        'sort_by': sort_by,
        'category_filter': category_filter,
        'categories': sorted(categories),
        'display_style': display_style,
        'favorites': favorites,
    }

    return render(request, 'emoji_app/emoji_catalog.html', context)


@login_required
def toggle_favorite(request):
    """Toggle emoji favorite status"""
    if request.method == 'POST':
        emoji_name = request.POST.get('emoji_name')
        emoji_category = request.POST.get('emoji_category')
        emoji_group = request.POST.get('emoji_group')
        emoji_html_code = request.POST.get('emoji_html_code')
        emoji_unicode = request.POST.get('emoji_unicode')

        # Get or create emoji
        emoji, created = Emoji.objects.get_or_create(
            name=emoji_name,
            defaults={
                'category': emoji_category,
                'group': emoji_group,
                'html_code': emoji_html_code,
                'unicode': emoji_unicode,
            }
        )

        # Check if already favorited
        favorite = Favorite.objects.filter(user=request.user, emoji=emoji).first()

        if favorite:
            # Remove from favorites
            favorite.delete()
            is_favorite = False
        else:
            # Add to favorites
            Favorite.objects.create(user=request.user, emoji=emoji)
            is_favorite = True

        return JsonResponse({'success': True, 'is_favorite': is_favorite})

    return JsonResponse({'success': False})


@login_required
def favorites(request):
    """User's favorite emojis view"""
    user_favorites = Favorite.objects.filter(user=request.user).select_related('emoji')
    display_style = request.GET.get('style', 'native')

    # Process emoji data to include unicode character
    emojis = []
    for fav in user_favorites:
        unicode_char = EmojiService.unicode_to_character(fav.emoji.unicode)
        emojis.append({
            'name': fav.emoji.name,
            'category': fav.emoji.category,
            'group': fav.emoji.group,
            'html_code': fav.emoji.html_code,
            'unicode': fav.emoji.unicode,
            'unicode_char': unicode_char,
        })

    context = {
        'emojis': emojis,
        'favorites': [fav.emoji.name for fav in user_favorites],
        'display_style': display_style,
    }

    return render(request, 'emoji_app/favorites.html', context)

def logout_view(request):
    """Custom logout view that accepts both GET and POST requests"""
    logout(request)
    return redirect('home')


def signup(request):
    """User registration view"""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to EmojiHub.')
            return redirect('emoji_catalog')
    else:
        form = SignUpForm()

    return render(request, 'emoji_app/signup.html', {'form': form})
