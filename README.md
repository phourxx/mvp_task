# mvp_task

##How to run
- Install Python:3.9 on your computer
- Install pipenv on your python installation
- Clone this repo.
- Move into the project direction from your command line with `cd mvp_task`
- Duplicate the file `.env_example` and name the duplicate `.env`
- Run `pipenv install` to install the project dependencies
- Run `pipenv shell` to switch to the virtual env that'd be created for this
 project automatically
- Run `python manage.py migrate` to apply migrations
- Run `python manage runserver` to start the application on `port 8000`