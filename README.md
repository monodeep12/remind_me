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
