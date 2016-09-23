[![Code Health](https://landscape.io/github/birkbeckOLH/annotran/master/landscape.svg?style=flat)](https://landscape.io/github/birkbeckOLH/annotran/master) [![Latest Version](https://img.shields.io/badge/python-2.7-blue.svg)]() [![License](http://img.shields.io/:license-mit-blue.svg)](https://github.com/birkbeckOLH/annotran/blob/master/LICENSE)

#annotran

## About

Annotran is an extension to the hypothesis annotation framework that allows users to translate web pages themselves and to view other users' translations. It is developed at the [Open Library of Humanities](https://about.openlibhums.org) and was funded by the Andrew W. Mellon Foundation. 

## Quirks

Annotran does not work well on extremely dynamic pages. If the web page that you are translating changes substantially, then it is likely that your translation will break.

## Development

This project is built as an extension to the hypothesis annotation framework: https://hypothes.is/. If you would like to join us in development efforts, or wish to run your own server, you can set up your development environment in the following way. Please note these instructions for Ubuntu 14.04.

Download the source code:
```
git clone https://github.com/birkbeckOLH/annotran.git
```
Download the hypothes.is version 0.8.14:
```
git clone https://github.com/hypothesis/h.git
cd h
git reset --hard v0.8.14
```
Install `h` by refering to its documentation on how to install it. Search for this document in project files: ../h/docs/hacking/install.rst. In addition to the Docker containers there, you will also need nsqd. The full set of container installs are:

```
docker run -d --name postgres -p 5432:5432 postgres
docker run -d --name elasticsearch -p 9200:9200 -p 9300:9300 nickstenning/elasticsearch-icu
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 --hostname rabbit rabbitmq:3-management
docker run -d --name redis -p 6379:6379 redis
docker run -d --name nsqd -p 4150:4150 -p 4151:4151 nsqio/nsq /nsqd
```

If you want to be able to easily monitor the emails that annotran/hypothes.is sends in your development environment, then you may wish to use the following command:

```
docker exec nsqd nsq_tail --topic email --nsqd-tcp-address localhost:4150
```

This can be important as account sign-up confirmation links are sent by email.

Create a Python virtual environment. Refer to the documentation on how to create virtual environments: http://docs.python-guide.org/en/latest/dev/virtualenvs/

Run the following commands to install hypothes.is into your virtual environment:
```
cd ..
cd annotran
sudo apt-get install -y --no-install-recommends  ruby-compass build-essential     git     libevent-dev     libffi-dev     libfontconfig     libpq-dev     python-dev     python-pip     python-virtualenv
pip install -r requirements.txt
```

###Steps performed to extend and overwrite hypothes.is

1. Boot system. Since the annotran package has been installed into the same Python environment as the hypothes.is application, it is possibile to start the hypothes.is application from annotran. To do so, place a version of h's pyramid configuration inside annotran. 

2. When extending Pyramid application (see documentation on how to do that: http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/extending.html), it is necessary to override views, routes and static assets (http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/assets.html#assets-chapter). To extend hypothes.is UI code, there are following steps performed:
	- There is assets.yaml file in annotran that is a copy of the same file from hypothes.is. Paths for assets that are overwritten in annotran are appropriately updated within this file. 
	- Assets are overwritten by invoking config.override_asset(..) method.
	- Javascript is overwritten using Angular dependency injection. h/static/scripts/app.coffee is required from the main module within the annotran.

3. In app.py we replace a set of hypothesis functions using Python monkey patching. The replacement functions are in replacements.py.

4. To override Angular directives, add the directive file in static/scripts/directive and then edit apps.js to add an app decorator that selects the override directive. 

###Understanding the different components and languages used by hypothes.is and overridden by annotran
Hypothesis uses multiple technologies:

* Pyramid for URL routing and setting handling
* The Python files (.py) in the project are part of the Pyramid framework's handling
* SQLAlchemy is used by the python files to read from and write to a PostgresSQL database and can be accessed by the python components
* An elasticsearch instance is used to store annotations themselves and can be accessed by the python components
* Annotator.js provides the core annotation functions
* A set of coffeescript and javascript files (.coffee and .js) extend Annotator.js and provide the hypothes.is sidebar and plugins to the document we are annotating
* Some javascript files make calls to the Pyramid framework's server-side python scripts (see above) and load database values in the client (see session.js for example)
* An event bubbling framework exists within the javascript files that can be fired and extended

##How to contribute

Tasks under development are available to investigate under the issues. You can also join in the discussion over there.

