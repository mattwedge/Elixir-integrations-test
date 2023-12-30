### Issues encountered
1. When initially running the `make migrations` command, I was getting the error `RuntimeWarning: Got an error checking a consistent migration history performed for database connection 'default': unable to open database file`.
This appears to be an issue to do with the permissions within the docker container. Changing the SQLite database location from `/app/integrations/db.sqlite3` to `/tmp/db.sqlite3` did the trick.
2. Even after this the migrations script was running succesfully but making no changed to the actual database schema.
I don't know what exactly was going on here but `exec`ing into the docker container and running `poetry run python manage.py migrate` worked.