# remind_me

**System Setup :**

- `./install_os_dependencies.sh install`
- Install Anaconda - [https://www.continuum.io/downloads#_unix](https://www.continuum.io/downloads#_unix)
- Create a virtual env `conda create -n remind_me python=3.4.3` and activate it using `source activate remind_me`
- Install the requirements with `pip install -r requirements.txt`
- Install MySql and create a table `reminders`
- Add `export DJANGO_SETTINGS_MODULE=reminder.settings.local` to .bashrc
- Add `export DJANGO_SECRET_KEY='YOUR-SECRET-KEY-HERE'`
- Add `export DATABASE_URL=mysql://<USER>:<PASSWORD>@<HOST>:<PORT>/reminders`

**API Documentation :**

- https://monodeep12.github.io/remind_me/


**Test Coverage :**

- Run tests using: `coverage run manage.py test --settings=reminder.settings.test`
- View coverage - `coverage report`


**Current Coverage :**

Name                            Stmts   Miss  Cover
---------------------------------------------------
manage.py                           6      0   100%
reminder/__init__.py                0      0   100%
reminder/settings/__init__.py       2      0   100%
reminder/settings/celery.py         8      0   100%
reminder/settings/common.py        26      0   100%
reminder/settings/test.py           3      0   100%
tasks/__init__.py                   0      0   100%
tasks/models.py                    64      9    86%
tasks/tasks.py                     16      2    88%
tasks/tests.py                     35      3    91%
---------------------------------------------------
TOTAL                             160     14    91%
