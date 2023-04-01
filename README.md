# AniHub

AniHub is a full-stack web application created for the Final Project of CS50's Web Programming with Python and JavaScript course. The application serves as an anime tracking and discovery platform, allowing users to manage their personalized anime lists, search for anime, and explore top-rated and seasonal anime.

## Features

- **User Authentication**: Users can register, login, and add a profile picture.
- **Theme Toggle**: Users can switch between light and dark themes.
- **Anime Search**: Users can search for anime using filters such as query, genres, type, and airing status.
- **Top-Rated Anime**: Users can view a list of top-rated anime.
- **Seasonal Anime**: Users can explore seasonal anime with year and season filters.
- **Customizable Anime Lists**: Users can add anime to categories such as Watching, Completed, Dropped, and Plan to Watch.
- **Anime List Import**: Users can import their anime lists from other websites like MyAnimeList using an XML file.

## Technologies

- **Backend**: Django
- **Frontend**: HTML, CSS, and JavaScript
- **Database**: PostgreSQL

## APIs and Data Sources

- [JikanAPI](https://jikan.moe/) for fetching anime data
- [Manami Project](https://github.com/manami-project/anime-offline-database) for the anime database used in creating anime lists, due to request limitations in Jikan API

## Deployment

The application was deployed using Digital Ocean with Gunicorn and Nginx as the web server and reverse proxy. It is live and available 24/7 at [AniHub.net](https://www.anihub.net/).

## Acknowledgements

This project took a considerable amount of time and effort, but I am extremely proud of the final result. I would like to thank CS50's Web Programming with Python and JavaScript course for providing the knowledge and guidance necessary to create this project.
