import requests

import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from urllib.parse import urlencode
from datetime import datetime

from .models import AnimeList, AnimeData, Comment
from .utils import parse_anime_ids_from_xml

# Create your views here.
def index(request):
    # Top 6 popular anime
    top_anime = cache.get('top_anime_data_index')
    if top_anime is None:
        params = {'limit': 10, 'order_by': 'members', 'sort': 'desc'}
        url = f'https://api.jikan.moe/v4/anime?' + urlencode(params, doseq=True)
        response = requests.get(url)
        top_results = response.json()
        top_anime = top_results['data']
        cache_timeout = 12 * 60 * 60
        cache.set('top_anime_data_index', (top_anime), cache_timeout)

    # Current season anime
    current_year = datetime.now().year
    current_month = datetime.now().month
    if current_month in [1, 2, 3]:
        season = 'winter'
    elif current_month in [4, 5, 6]:
        season = 'spring'
    elif current_month in [7, 8, 9]:
        season = 'summer'
    else:
        season = 'fall'
    
    season_anime = cache.get(f'season_anime_data_index')
    if season_anime is None:
        url = f'https://api.jikan.moe/v4/seasons/{current_year}/{season}?page=1&limit=10'
        response = requests.get(url)
        season_results = response.json()
        season_anime = season_results['data']
        cache_timeout = 12 * 60 * 60
        cache.set('season_anime_data_index', (season_anime), cache_timeout)

    return render(request, '../templates/index.html', {
        'top_anime': top_anime,
        'season_anime': season_anime,
    })

def update_total_pages():
    url = 'https://api.jikan.moe/v4/top/anime'
    response = requests.get(url)
    results = response.json()
    total_pages = results['pagination']['last_visible_page']

    # Store the total pages in the cache for 24 hours
    cache_timeout = 24 * 60 * 60
    cache.set('total_pages', total_pages, cache_timeout)
    return total_pages

def update_total_search_pages(query):
    url = f'https://api.jikan.moe/v4/anime?order_by=members&sort=desc&q={query}&page=1&sfw'
    response = requests.get(url)
    results = response.json()
    total_pages = results['pagination']['last_visible_page']

    # Store the total pages in the cache for 24 hours
    cache_timeout = 24 * 60 * 60
    cache.set('total_pages', total_pages, cache_timeout)
    return total_pages

def top(request, page=1):
    cache_key = f'top_anime_page_{page}'
    top_anime_data = cache.get(cache_key)

    if top_anime_data is None:
        url = f'https://api.jikan.moe/v4/top/anime?page={page}'
        response = requests.get(url)
        top_results = response.json()
        animeData = top_results['data']

        total_pages = cache.get('total_pages')
        if total_pages is None:
            total_pages = update_total_pages()
        has_next_page = page < total_pages
        has_next_next_page = page + 1 < total_pages

        cache_timeout = 12 * 60 * 60
        cache.set(cache_key, (animeData, has_next_page, has_next_next_page), cache_timeout)
    else:
        animeData, has_next_page, has_next_next_page = top_anime_data

    return render(request, '../templates/top.html', {
        'data': animeData,
        'current_page': int(page),
        'has_next_page': has_next_page,
        'has_next_next_page': has_next_next_page,
    })

def seasonal(request, page=1):
    if request.method == 'POST':
        year = request.POST.get('year')
        season = request.POST.get('season')
        query_params = urlencode({'year': year, 'season': season})
        return HttpResponseRedirect(reverse('season_page', kwargs={'page': 1}) + f"?{query_params}")

    year = request.GET.get('year')
    season = request.GET.get('season')
    seasons = ['Winter', 'Spring', 'Summer', 'Fall']

    if year is None or season is None:
        year = 2023
        season = 'winter'

    cache_key = f'top_anime_{year}_{season}_page_{page}'
    season_anime_data = cache.get(cache_key)
    current_year = datetime.now().year

    if season_anime_data is None:
        url = f'https://api.jikan.moe/v4/seasons/{year}/{season}?page={page}'
        response = requests.get(url)
        season_results = response.json()
        animeData = season_results['data']
        pagination = season_results['pagination']
        has_next_page = pagination['has_next_page']

        cache_timeout = 12 * 60 * 60
        cache.set(cache_key, (animeData, has_next_page), cache_timeout)
    else:
        animeData, has_next_page = season_anime_data

    return render(request, '../templates/seasonal.html', {
        'data': animeData,
        'year': year,
        'season': season,
        'current_page': int(page),
        'has_next_page': has_next_page,
        'current_year': current_year,
        'seasons': seasons,
    })

def get_anime_genres():
    genres_url = 'https://api.jikan.moe/v4/genres/anime'
    genres_response = requests.get(genres_url)
    genres_data = json.loads(genres_response.text)
    return genres_data['data']

def search_anime(page, genres, type, status, search_query):
    params = {'page': page, 'order_by': 'members', 'sort': 'desc'}

    if search_query:
        params['q'] = search_query

    if genres:
        params['genres'] = ','.join(genres)

    if type:
        params['type'] = type

    if status:
        params['status'] = status

    url = f'https://api.jikan.moe/v4/anime?' + urlencode(params, doseq=True)
    response = requests.get(url)
    search_results = response.json()
    anime_data = search_results['data']
    pagination = search_results['pagination']
    has_next_page = pagination['has_next_page']

    return anime_data, has_next_page

def anime_search(request):
    TYPES = ['TV', 'Movie', 'OVA', 'ONA', 'Special', 'Music']
    AIRING_STATUS = ['Airing', 'Complete', 'Upcoming']

    page = request.GET.get('page', 1)
    selected_genre_names = request.GET.getlist('genres')
    selected_type = request.GET.get('type', '')
    selected_airing_status = request.GET.get('status', '')
    search_query = request.GET.get('search_query', '')

    # Convert genre names to genre IDs
    all_genres = get_anime_genres()
    genre_name_to_id = {genre['name']: genre['mal_id'] for genre in all_genres}
    selected_genre_ids = [str(genre_name_to_id[name]) for name in selected_genre_names if name in genre_name_to_id]

    cache_key = f'anime_search_{hash(frozenset(request.GET.items()))}_page_{page}'
    anime_search_data = cache.get(cache_key)

    if anime_search_data is None:
        animeSearchData, has_next_page = search_anime(page, selected_genre_ids, selected_type, selected_airing_status, search_query)

        cache_timeout = 12 * 60 * 60
        cache.set(cache_key, (animeSearchData, has_next_page), cache_timeout)
    else:
        animeSearchData, has_next_page = anime_search_data

    # Properly handle the 'genres' parameter for the template
    genres_param = '&'.join([f'genres={genre}' for genre in selected_genre_names])

    type_param = f'type={selected_type}' if selected_type else ''
    status_param = f'status={selected_airing_status}' if selected_airing_status else ''

    return render(request, '../templates/anime_search.html', {
        'data': animeSearchData,
        'current_page': int(page),
        'has_next_page': has_next_page,
        'params': {'genres': genres_param, 'type': type_param, 'status': status_param},
        'genres': get_anime_genres(),
        'selected_genres': selected_genre_ids,
        'types': TYPES,
        'airing_status': AIRING_STATUS,
        'selected_type': selected_type,
        'selected_airing_status': selected_airing_status,
        'search_query': search_query,
    })



def search(request, page=1):
    query = request.GET.get('query', '')

    if query:
        cache_key = f'search_anime_page_{query}_{page}'
        search_anime_data = cache.get(cache_key)

        if search_anime_data is None:
            url = f'https://api.jikan.moe/v4/anime?order_by=members&sort=desc&q={query}&page={page}&sfw'
            response = requests.get(url)
            search_results = response.json()
            animeData = search_results['data']

            total_pages = cache.get(f'total_search_pages_{query}')
            if total_pages is None:
                total_pages = update_total_search_pages(query)
            has_next_page = page < total_pages
            has_next_next_page = page + 1 < total_pages

            cache_timeout = 12 * 60 * 60
            cache.set(cache_key, (animeData, has_next_page, has_next_next_page), cache_timeout)
        else:
            animeData, has_next_page, has_next_next_page = search_anime_data
    else:
        animeData = []
        has_next_page = False
        has_next_next_page = False

    return render(request, '../templates/search.html', {
        'data': animeData,
        'query': query,
        'current_page': int(page),
        'has_next_page': has_next_page,
        'has_next_next_page': has_next_next_page,
    })




def detail(request, anime_id):
    cache_key = f'anime_detail_{anime_id}'
    detail_anime_data = cache.get(cache_key)

    if detail_anime_data is None:
        url = f'https://api.jikan.moe/v4/anime/{anime_id}'
        response = requests.get(url)
        animedetail = response.json()
        animeData = animedetail['data']

        # Store the fetched data in the cache for 12 hours
        cache_timeout = 12 * 60 * 60
        cache.set(cache_key, animeData, cache_timeout)
    else:
        animeData = detail_anime_data

    comments = Comment.objects.filter(anime_id=anime_id).order_by('-timestamp')
    if request.user.is_authenticated:
        user_anime = AnimeList.objects.filter(user=request.user, anime_id=anime_id).first()
    else:
        user_anime = None
    return render(request, '../templates/detail.html', {
        'anime': animeData,
        'user_anime': user_anime,
        'status_choices': AnimeList.STATUS_CHOICES,
        'comments': comments,
    })

@login_required
@csrf_exempt
def update_anime_status(request, anime_id):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = json.loads(request.body)
        new_status = data.get('status')

        anime, created = AnimeList.objects.get_or_create(user=request.user, anime_id=anime_id)
        anime.status = new_status
        anime.save()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False})

def animelist(request):
    user_anime_list = AnimeList.objects.filter(user=request.user)
    watching = user_anime_list.filter(status='watching').count()
    completed = user_anime_list.filter(status='completed').count()
    dropped = user_anime_list.filter(status='dropped').count()
    plan_to_watch = user_anime_list.filter(status='plan to watch').count()
    status_counts = {
        'Watching': watching,
        'Completed': completed,
        'Dropped': dropped,
        'Plan to Watch': plan_to_watch,
    }
    animelist = []
    anime_list_with_data = [(AnimeData.objects.get(anime_id=int(anime.anime_id)), anime) for anime in user_anime_list]
    sorted_anime_list_with_data = sorted(anime_list_with_data, key=lambda x: x[0].title.lower())

    for anime_data, anime in sorted_anime_list_with_data:
        animelist.append((anime_data, anime.status))
    return render(request, 'anime_list.html', {
        'status_choices': AnimeList.STATUS_CHOICES,
        'animelist': animelist,
        'status_counts': status_counts,
    })

from django.http import JsonResponse

@login_required
def remove_anime_from_list(request, anime_id):
    if request.method == "POST":
        try:
            anime = AnimeList.objects.get(user=request.user, anime_id=anime_id)
            anime.delete()
            return JsonResponse({"success": True})
        except AnimeList.DoesNotExist:
            return JsonResponse({"success": False, "message": "Anime not found in the list."})
    else:
        return JsonResponse({"success": False, "message": "Invalid request method."})

@login_required
def submit_comment(request, anime_id):
    if request.method == 'POST':
        comment_text = request.POST['comment']
        user = request.user
        anime_id = anime_id

        new_comment = Comment(user=user, anime_id=anime_id, text=comment_text)
        new_comment.save()

        return redirect('detail', anime_id=anime_id)

@login_required
def edit_comment(request, comment_id):
    if request.method == 'POST':
        comment = Comment.objects.get(id=comment_id)

        if request.user == comment.user:
            new_text = json.loads(request.body).get('comment')
            comment.text = new_text
            comment.save()
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "error": "Permission denied."})
    else:
        return JsonResponse({"success": False, "error": "Invalid request method."})

@login_required
def delete_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    response_data = {'success': False}

    if request.user == comment.user:
        if request.method == 'POST':
            comment.delete()
            response_data['success'] = True

    return JsonResponse(response_data)

@login_required
def import_anime_list(request):
    if request.method == 'POST':
        xml_file = request.FILES.get('anime_list_file', None)
        overwrite_existing = request.POST.get('overwrite_existing', None)

        if xml_file:
            anime_data = parse_anime_ids_from_xml(xml_file)

            if overwrite_existing:
                AnimeList.objects.filter(user=request.user).delete()

            for anime_entry in anime_data:
                anime_id = anime_entry['anime_id']
                status = anime_entry['status'].lower()

                if status != 'on_hold':
                    existing_anime = AnimeList.objects.filter(anime_id=anime_id, user=request.user).first()

                    if not existing_anime:
                        AnimeList.objects.create(anime_id=anime_id, user=request.user, status=status)

            messages.success(request, 'Anime list imported successfully!')
        else:
            messages.error(request, 'Please upload a valid XML file.')

        return redirect('importlist')  # Replace 'profile' with the name of your profile URL
    else:
        # If the request is not a POST request, redirect to the profile page
        return render(request, 'importlist.html')