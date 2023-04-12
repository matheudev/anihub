AniHub
======
AniHub is a full-stack web application created for the Final Project of CS50's Web Programming with Python and JavaScript course. The application serves as an anime tracking and discovery platform, allowing users to manage their personalized anime lists, search for anime, and explore top-rated and seasonal anime.

Distinctiveness and Complexity
-------------------------------
AniHub is a unique and complex project that stands out from the projects featured in the course. AniHub provides a personalized experience for anime fans, allowing them to easily manage their anime lists and discover new anime based on their interests.

AniHub goes beyond the complexity of the course projects by incorporating several advanced features such as importing anime lists from other websites, utilizing multiple APIs, and implementing a theme toggle system. Moreover, AniHub's frontend is mobile-responsive, ensuring a seamless user experience on various devices.

Features
--------
- **User Authentication:** Users can register, login, and add a profile picture.
- **Theme Toggle:** Users can switch between light and dark themes.
- **Anime Search:** Users can search for anime using filters such as query, genres, type, and airing status.
- **Top-Rated Anime:** Users can view a list of top-rated anime.
- **Seasonal Anime:** Users can explore seasonal anime with year and season filters.
- **Anime Lists:** Users can add anime to categories such as Watching, Completed, Dropped, and Plan to Watch.
- **Import Lists:** Users can import their anime lists from other websites like MyAnimeList using an XML file.

Technologies
------------
- **Backend:** Django
- **Frontend:** HTML, CSS, and JavaScript
- **Database:** PostgreSQL

APIs and Data Sources
---------------------
- **JikanAPI** for fetching anime data
- **Manami Project** for the anime database used in creating anime lists, due to request limitations in Jikan API

Deployment
----------
The application was deployed using Digital Ocean with Gunicorn and Nginx as the web server and reverse proxy. It is live and available 24/7 at [AniHub.net](https://www.anihub.net/).

File Structure
--------------
- `anime/`: Django app for anime search, lists, and data management.
- `animelist/`: Main Django project folder with settings.py.
- `media/`: Folder for storing user-uploaded images.
- `static/`: Folder containing all static files, such as CSS, JavaScript, and images.
- `templates/`: Folder containing all the HTML templates.
- `users/`: Django app for authentication and profile management.
- `manage.py`: Main management script for Django.
- `README.md`: Documentation of the project.
- `requirements.txt`: List of Python packages needed to run the application.

How to Run
----------
1. Install PostgreSQL on your local machine if you haven't already. You can follow the instructions for your operating system here: [PostgreSQL installation](https://www.postgresql.org/download/)
2. Create a PostgreSQL user and database for your project. You can do this using the `psql` command-line interface or a GUI tool like [pgAdmin](https://www.pgadmin.org/).
3. Update the `settings.py` file in the main Django project folder (animelist/) with the new credentials for the PostgreSQL connection and email settings. Replace the values with os.getenv calls. For email, follow this guide on [how to set up an App Password for Gmail](https://support.google.com/accounts/answer/185833).
4. Install the required packages using `pip install -r requirements.txt`.
5. Run `python manage.py makemigrations` and `python manage.py migrate` to set up the database.
6. Run `python manage.py runserver` to start the development server.
7. Access the application via your web browser at `http://127.0.0.1:8000/`.


Acknowledgements
----------------
This project took a considerable amount of time and effort, but I am extremely proud of the final result. I would like to thank CS50's Web Programming with Python and JavaScript course for providing the knowledge and guidance necessary to create this project.

Additional Information
----------------------
- To import anime lists from other websites, users must first export their lists as an XML file from the respective website. Then, they can use the "Import List" feature in AniHub to upload the XML file and update their AniHub anime lists accordingly.
- AniHub utilizes the JikanAPI for fetching anime data and the Manami Project as an anime database for creating anime lists. Due to request limitations in the Jikan API, the Manami Project database is used to minimize the number of API requests made. This setup ensures that the application remains responsive and efficient even with a large number of users.

