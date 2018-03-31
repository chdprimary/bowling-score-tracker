## dependencies
1. Python 3.6 (project uses f-string syntax)
2. Django 1.11

To run the end-to-end tests, you'll need:
1. Firefox
2. [Geckodriver](https://github.com/mozilla/geckodriver/releases) (put it on system PATH)
3. Selenium 3

You can set up a virtualenv (```python -m venv virtualenv```) in the cloned repo directory, then ```cd virtualenv``` and install Django 1.11 and Selenium 3 with ```pip install "django<1.12" "selenium<4"```.

## running locally
After cloning the repo:
  1. run ```python manage.py migrate```
  2. run ```python manage.py runserver```
  3. navigate to ```localhost:8000```
  4. enter your rolls as app scores and tabulates game data
* NOTE: game is persisted at ```localhost:8000/game/:id```
  * can close game, reload URI later and continue in-place
  
## running tests
* End-to-end tests: ```python manage.py test e2e_tests/```
* Unit tests: ```python manage.py test bowling_app/```

## note about version control
While I normally would've used git from the start, I didn't for this project, in case the team was wanting their coding challenge to be kept private. After a public GH link was requested, I added the full app to this repo in one commit. Apologies if the expectation was to be able to step through a commit history. 

## what I would improve / limitations
I enjoyed and am proud of this project, but there are areas for improvement. Given more time, I would:
* Increase test coverage with more of both functional/end-to-end and unit tests
* Write succinct and comprehensive documentation covering input validation, algorithm, URI structure, etc
* Write cleaner, more readable code and remove unnecessary code commenting. I usually prefer self-documenting, readable code in place of non-necessary comments, because comments can, over time, become misleading or irrelevant (as developers often neglect to update appropriate comments when they update code). See [here](https://www.informit.com/articles/article.aspx?p=1326509) and [here](https://stackoverflow.com/questions/209015/what-is-self-documenting-code-and-can-it-replace-well-documented-code#209089).
* Would use template inheritance to DRY up duplication between home.html and game.html templates
* Consider changing ```POST /games/:id/add_roll``` to ```PUT /games/:id/add_roll```
* While this app takes a RESTful approach, on a second attempt I might try to become more familiar with a framework like [Django REST Framework](http://www.django-rest-framework.org/) or [Flask](http://flask.pocoo.org/), and create a strict REST API, utilizing HTTP verbs like PUT and DELETE for rolls as well.
* One limitation of my current implementation of the game is that concurrent games are not supported. That use case fails because I resolve strikes and spares by inspecting sequential rolls, which I retrieve by adding a magic number (1 or 2) to the strike/spare roll ID. 
  * I would approach a fix by retrieving all current game's frames, and retrieving the unresolved Roll as well as the next sequential Roll in the resulting QuerySet (which is guaranteed to be part of the same Game)
  
That's it for my write-up. Thanks!
