$(document).ready(function() {
    var options = window.options;
    if(options === undefined) {
        var options = {
            fullCalendar: {},
            datetimepicker: {},
        };
    }
    if(typeof calendar != 'undefined') {
        url = calendar.source_url;
    }

    var oldSync = Backbone.sync;
    Backbone.sync = function(method, model, options) {
        options.beforeSend = function(xhr){
            xhr.setRequestHeader('X-CSRFToken', calendar.csrf_token);
        };
        return oldSync(method, model, options);
    };

    var Event = Backbone.Model.extend({
        urlRoot: calendar.url_root,
    });

    var EventView = Backbone.View.extend({
        el: $('#calendar-event-dialog'),
        el_titles: $('#calendar-event-dialog-title'),
        el_start: $('#id_start'),
        el_end: $('#id_end'),
        el_title: $('#id_title'),
        el_agenda: $('#id_agenda'),
        el_allDay: $('#id_allDay'),
        el_places: $('#id_places'),
        el_url: $('#id_url'),
        el_save_event: $('#calendar-event-dialog-ok'),
        initialize: function() {
            _.bindAll(this);

            $(this.el).on('hidden.bs.modal', function (e) {
                $(this).find('form').each(function() {
                    this.reset(); 
                });
            });

            this.el_start.datetimepicker(
                options.datetimepicker
            );
            this.el_end.datetimepicker(
                options.datetimepicker
            );

            this.el_save_event.on('click', this.save);
        },
        formatDateTime: function(date) {
            var date_string = $.datepicker.formatDate(
                options.datetimepicker.dateFormat,
                date
            );

            var hours = ((date.getHours() < 10) ? '0' : '')
            + date.getHours()
            ;
            var minutes = ((date.getMinutes() < 10) ? '0' : '')
            + date.getMinutes()
            ;
            var time_string = hours + ':' + minutes;

            return date_string + ' ' + time_string;
        },
        render: function() {
            // Title
            this.el_titles.text(this.model.isNew()
            ? this.el_titles.attr('data-new')
            : this.el_titles.attr('data-edit')
            );

            // Convert model datetime
            if(typeof this.model.get('start') === 'string') {
                this.model.set('start', $.fullCalendar.parseISO8601(
                    this.model.get('start'))
                );
                this.model.set('end', $.fullCalendar.parseISO8601(
                    this.model.get('end'))
                );
            }

            if(!this.model.isNew()) {
                this.el_title.val(this.model.get('title'));
                this.el_allDay.val(this.model.get('allDay'));
                this.el_agenda.val(this.model.get('agenda'));
                this.el_places.val(this.model.get('places'));
                this.el_url.val(this.model.get('url'));
            }

            this.el_start.val(this.formatDateTime(this.model.get('start')));
            this.el_end.val(this.formatDateTime(this.model.get('end')));

            $(this.el).modal('show');

            return this;

        },
        save: function() {
            this.model.set({
                'title': this.el_title.val(),
                'start': this.model.get('start'),
                'end': this.model.get('end'),
                'agenda': this.el_agenda.val(),
                'places': this.el_places.val(),
                'url': this.el_url.val(),
            });
            if(this.model.isNew()) {
                this.collection.create(this.model, {success: this.close, });
            } else {
                this.model.save({}, {success: this.close, });
            }
        },
        close: function() {
            $(this.el).modal('hide');
        },
    });
    var Events = Backbone.Collection.extend({
        model: Event,
        url: calendar.url_root,
    });

    var EventsView = Backbone.View.extend({
        url: calendar.url_root,
        initialize: function(){
            _.bindAll(this);

            this.collection.bind('reset', this.addAll);
            this.collection.bind('add', this.addOne);


            this.eventView = new EventView();
            this.eventView.collection = this.collection;
        },
        render: function() {
            options.fullCalendar = $.extend({},
                options.fullCalendar, {
                    select: this.select,
                    events: this.fetchEvents,
                    eventClick: this.eventClick,
                    eventDrop: this.eventDropOrResize,
                    eventResize: this.eventDropOrResize,
                }
            );
            $(this.el).fullCalendar(options.fullCalendar);

        },
        addAll: function() {
            $(this.el).fullCalendar('addEventSource', this.collection.toJSON());
        },
        addOne: function(event) {
            $(this.el).fullCalendar('renderEvent', event.toJSON());
        },
        fetchEvents: function(start, end, callback) {

            var data = {
                start: $.fullCalendar.formatDate(start, 'u'),
                end: $.fullCalendar.formatDate(end, 'u'),
            };
            if(calendar.places !== undefined && calendar.places.length > 0) {
                data.places = calendar.places;
            }

            events.fetch({
                data: data,
            });
        },
        select: function(startDate, endDate) {
            this.eventView.model = new Event({
                start: startDate,
                end: endDate,
            });
            this.eventView.render();
        },
        eventClick: function(fcEvent) {
            this.eventView.model = this.collection.get(fcEvent.id);
            this.eventView.render();
        },
        eventDropOrResize: function(fcEvent) {
            console.log(fcEvent);
            this.collection.get(fcEvent.id).save({
                start: fcEvent.start,
                end: fcEvent.end,
            });
        },
        reset: function() {

        },
    });


    var events = new Events();
    var el_calendar = $('#calendar');
    var eventsView = new EventsView({el: $("#calendar"), collection: events});
    eventsView.render();
});
