#annotran

## About

The purpose of this project is to develop annotation technologies for translation purposes for the Open Library of Humanities (OLH).

## Development

This project is built as an extension to hypothesis annotation framework: https://hypothes.is/. We are in an early stage of the development, and if you would like to join us you can set up your development environment in a following way:

1. Download the source code:
```
git clone https://github.com/birkbeckOLH/annotran.git
```

2. Download the hypothes.is version 0.8.14:
```
git clone https://github.com/hypothesis/h.git
cd h
git reset --hard v0.8.14
```

3. Create a Python virtual environment. Refer to the documentation on how to create virtual environments: http://docs.python-guide.org/en/latest/dev/virtualenvs/

4. Run the following commands to install hypothes.is into your virtual environment:
```
cd ..
cd annotran
pip install -r requirements.txt
```

##How to contribute

Tasks under development are available to investigate under the issues. You can also join in the discussion over there. More guidelines to come..
