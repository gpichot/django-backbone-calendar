from setuptools import setup, find_packages

import os

backbone_calendar = __import__('backbone_calendar')


setup(
    name='django-backbone-calendar',
    packages=find_packages(),
    author='Gabriel Pichot',
    author_email='gabriel.pichot@gmail.com',
    url='https://github.com/gpichot/django-backbone-calendar',
    description=(
        'Django Backbone Calendar is an app for '
        'Django which aims to manipulate easily a'
        'calendar.'
    ),
    include_package_data=True,
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python',
    ],
    keywords=['calendar', 'backbone', 'event', 'agenda'],
    install_requires=[
       'Django >= 1.5',
       'django-backbone >= 0.3.1',
       'django-bootstrap3 >= 4.2.0',
       'django-ical >= 1.2',
    ],
)
