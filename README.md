[![Build Status](https://travis-ci.org/birkbeckOLH/annotran.svg?branch=master)](https://travis-ci.org/birkbeckOLH/annotran)
[![Code Health](https://landscape.io/github/birkbeckOLH/annotran/master/landscape.svg?style=flat)](https://landscape.io/github/birkbeckOLH/annotran/master)

#annotran

## About

The purpose of this project is to develop annotation technologies for translation purposes for the Open Library of Humanities (OLH).

## Development

This project is built as an extension to hypothesis annotation framework: https://hypothes.is/. We are in an early stage of the development, and if you would like to join us you can set up your development environment in a following way. Please note these instructions for Ubuntu 14.04.

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
sudo apt-get install -y --no-install-recommends  build-essential     git     libevent-dev     libffi-dev     libfontconfig     libpq-dev     python-dev     python-pip     python-virtualenv
pip install -r requirements.txt
```

###Steps performed to extend and overwrite hypothes.is

1. Boot system. Since the annotran package has been installed into the same Python environment as the hypothes.is application, it is possibile to start hypothes.is application from the annotran. To do that, in annotran, a h's pyramid configuration should be included in the annotran's Pyramid configuration. 

2. When extending Pyramid application (see documentation on how to do that: http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/extending.html), it is necessary to override views, routes and static assets (http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/assets.html#assets-chapter). To extend hypothes.is UI code, there are following steps performed:
	a) There is assets.yaml file in annotran that is a copy of the same file from hypothes.is. Paths for assets that are overwritten in annotran are appropriately updated within this file. 
	b) Assets are overwitted by invoking config.override_asset(..) method.
	b) Javascript is overwritten using Angular dependency injection. h/static/scripts/app.coffee is required from the main module within the annotran.


##How to contribute

Tasks under development are available to investigate under the issues. You can also join in the discussion over there. More guidelines to come..
