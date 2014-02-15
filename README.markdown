# Django Backbone Calendar

Django Backbone Calendar is an app for Django which aims to manipulate easily a calendar.

## Status

Currently in development

## Javascript
To add in an efficient way events and to modify them this project uses the following
javascript librairies :

* [FullCalendar][1]
* [Backbone.js][2]
* [jQuery][3] & [jQuery UI][4]
* [jQuery Timepicker Addon][5]
* [Bootstrap][6]

The Javascript part is widely inspired by the following [article of Ben Teese][7].

## Django Apps
It uses the followings Django apps :

* [django-backbone][8] (forked version)
* [django-bootstrap-form][9]

## ToDo

* Recurrent events
* Export : iCalendar
* Better support of timezones and locales

[1]: http://arshaw.com/fullcalendar/  
[2]: http://backbonejs.org/
[3]: http://jquery.com/
[4]: http://jqueryui.com/
[5]: http://trentrichardson.com/examples/timepicker/
[6]: http://getbootstrap.com/
[7]: http://blog.shinetech.com/2011/08/05/building-a-shared-calendar-with-backbone-js-and-fullcalendar-a-step-by-step-tutorial/
[8]: https://github.com/gpichot/django-backbone
[9]: https://github.com/tzangms/django-bootstrap-form
