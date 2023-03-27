import json
import requests
from django.core.management.base import BaseCommand
from anime.models import AnimeData, AnimeList

class Command(BaseCommand):
    help = 'Update anime data in the database from the anime-offline-database.'

    def update_database(self, anime_entry):
        sources = anime_entry['sources']
        title = anime_entry['title']
        
        # Extract the MyAnimeList ID and Anilist ID from the sources list
        anime_id = None
        for source in sources:
            if 'myanimelist.net' in source:
                anime_id = int(source.split('/')[-1])
                break

        if anime_id is not None:
            anime_data_obj, created = AnimeData.objects.update_or_create(
                anime_id=anime_id,
                defaults={
                    'title': title,
                    'type': anime_entry['type'],
                    'status': anime_entry['status'],
                    'picture': anime_entry['picture'],
                    'sources': anime_entry['sources'],
                    'episodes': anime_entry['episodes'],
                    'synonyms': anime_entry['synonyms'],
                    'tags': anime_entry['tags'],
                    'relations': anime_entry['relations'],
                    'thumbnail': anime_entry['thumbnail'],
                    'season_year': anime_entry['animeSeason']['year'],
                    'season': anime_entry['animeSeason']['season'],
                }
            )
            print(f"Database saved for {title}")
        else:
            print(f"Could not find suitable ID for {title}")

    def handle(self, *args, **options):
        # Download the anime-offline-database JSON file
        url = 'https://raw.githubusercontent.com/manami-project/anime-offline-database/master/anime-offline-database.json'
        response = requests.get(url)
        data = json.loads(response.text)

        # Iterate through the downloaded data and update the local database
        for anime_entry in data['data']:
            self.update_database(anime_entry)

        self.stdout.write(self.style.SUCCESS('Successfully updated anime data in the database.'))