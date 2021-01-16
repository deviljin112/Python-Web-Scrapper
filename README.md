# Flask Scrapper

This is a flask based web scrapper for the ITJobsWatch website.

</br>

Note: This project was developed and deployed on Ubuntu 20

## Features

- One click app trigger
- Clearly formatted table results
- Login and Registration System
- Light weight Database with SQLite3
- SHA256 password encryption
- Easily deployed
- Easily modifiable with templates
- Outputs a JSON file
- Ease of implementation to other languages
- Functional API
- Functional user panel with GUI access to the API

## Pre-requisites

Essential Packages:

- Python 3.x
- Working Terminal
- [Python Virtual Environment](https://docs.python.org/3/library/venv.html)
- SQLite3

Optional Modules:

- Nginx (For reverse proxy)
- Gunicorn (For production deployment)
- Supervisor (For automating deployment)

## TLDR

Automated shell file available [HERE](/automation/dev_env.sh).

- Open terminal
- Install SQLite3
  - `sudo apt install sqlite3`
- Activate a fresh Python virtual environment
  - `python3 -m venv <venv_name>`
  - `source <venv_name>/bin/activate`
- Navigate to the folder where you have cloned this repository
- `cd deploy_code`
- `export PYTHONPATH=$PWD/project/`
- `python3 -m pip install -r requirements.txt`
- `python3 setup.py build`
- `python3 setup.py install`
- `python3 create_db.py`
- `export FLASK_APP=project`
- `flask run`
- Open browser
- Navigate to [http://localhost:5000](http://localhost:5000)

## Building the project

Before installing any dependencies we need to ensure we add our project into our python path. To do that run `export PYTHONPATH=$PWD/project/` in your shell. This will ensure that all the files are discoverable and available to our python interpreter.

</br>

Building the project requires 3 simple steps, installing the `requirements.txt` and building and installing the `setup.py` file. All the requirements and dependencies will be installed with `python3 -m pip install -r requirements.txt` followed by `python3 setup.py build` and `python3 setup.py install`. We also need to ensure we have SQLite3 installed, to do that run `sudo apt install sqlite3` which will install the package. And to initialise the database run `python3 create_db.py`.

## Running the project

After installing all the packages, we need to ensure we set the `FLASK_APP` variable to `project` as an environment variable. To do that we simply run `export FLASK_APP=project`. After setting our environment, all we need to do is run `flask run` and open our browser. Once our browser is open navigate to [http://localhost:5000](http://localhost:5000) and that is everything.

## Production Deployment

For production deployment you can use `gunicorn` or any other recommended package from Flask's website. To install simply activate your virtual environment in python and run `python3 -m pip install gunicorn` and to run your app just use `gunicorn project:app`.

</br>

For a more automated system, you can use `supervisor` to turn our application into a service which whill be enabled when our system is started. To install it run `sudo apt install supervisor`. Afterwards we need to copy a config file provided in the `config_files` folder in this repo called `flask_app.conf` into `/etc/supervisor/conf.d/`. After we have copied our config file we need to run the following commands:

- `sudo supervisorctl reread`
- `sudo supervisorctl update`
- `sudo supervisorctl avail`
- `sudo supervisorctl restart FlaskApp`

Our application should now be deployed as a service. Log files should be saved in the `../deploy_code/project/var/log/` folder.

</br>

We can also deploy our application with NGinx, for that we need to install it with `sudo apt install nginx`. Edit the configuration file at `server_name` with our public IP address, and copy that config file to `/etc/nginx/` folder. Afterwards use `sudo systemctl restart nginx` and we should have a running reverse proxy which redirects all trafic to our web-application.

## Ansible Automation

This repo also contains Ansible-Ready files to fully deploy the Flask application. [scrapper_playbook.yaml](automation/scrapper_playbook.yaml) will deploy the Flask application on the specified machine into production, therefore running `ansible-playbook scrapper_playbook.yaml` will take care of the entire provisioning of your machine. Please ensure that you add `scrapper` group to your hosts file, located in `/etc/ansible/hosts`.

</br>

Example:

```conf
[scrapper]
192.168.0.1 ansible_connection=ssh ansible_ssh_private_key_file=/path/to/file/key.pem
```
