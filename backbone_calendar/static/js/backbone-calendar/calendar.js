$(document).ready(function() {
    var options = window.options;
    var calendarOptions = $.extend({
        viewDisplay: function (view) {
            var h = (view.name == "month") ? NaN : 2500;
            $('#calendar').fullCalendar(
                'option', 'contentHeight', h
            );
        }, 
    }, window.calendarOptions);
    if(calendarOptions === undefined)
        var calendarOptions = {};
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

    function compileUTC(string_date, plain) {
        if(typeof string_date !== 'string') {
            return string_date;
        }
        if(plain === undefined) {
            var plain = false;
        }
        var offset = (new Date()).getTimezoneOffset();
        var hours = Math.abs(offset / 60);
        var minutes = Math.abs(offset) - hours * 60;
        if(plain) {
            var str = offset < 0 ? '+' : '-';
        } else {
            var str = offset < 0 ? '-' : '+';
        }
        if(hours <= 9)
            str += '0';
        str += hours + ':';
        if(minutes <= 9)
            str += '0';
        str += minutes;
        return string_date.substr(0, string_date.length - 1) + str;
    }

    function addUTC(event) {
        event.set('start', compileUTC(event.get('start')));
        event.set('end', compileUTC(event.get('end')));
    }
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
                calendarOptions.datetimepicker
            );
            this.el_end.datetimepicker(
                calendarOptions.datetimepicker
            );

            this.el_save_event.on('click', this.save);
        },
        formatDateTime: function(date) {
            var date_string = $.datepicker.formatDate(
                calendarOptions.datetimepicker.dateFormat,
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
                    this.model.get('start')
                ));
                this.model.set('end', $.fullCalendar.parseISO8601(
                    this.model.get('end')
                ));
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
            var start = $.datepicker.parseDateTime(
                calendarOptions.datetimepicker.dateFormat,
                calendarOptions.datetimepicker.timeFormat,
                this.el_start.val()
            );
            var end = $.datepicker.parseDateTime(
                calendarOptions.datetimepicker.dateFormat,
                calendarOptions.datetimepicker.timeFormat,
                this.el_end.val()
            );
            this.model.set({
                'title': this.el_title.val(),
                'start': start, 
                'end': end, 
                'agenda': this.el_agenda.val(),
                'places': this.el_places.val(),
                'url': this.el_url.val(),
            });
            if(this.model.isNew()) {
                this.collection.create(this.model, {success: this.close, });
            } else {
                //addUTC(this.model);
                this.model.save({}, {success: this.close, });
            }
            $(this.el).fullCalendar('rerenderEvents');
        },
        close: function() {
            $(this.el).modal('hide');
        },
    });
    var Events = Backbone.Collection.extend({
        model: Event,
        url: calendar.url_root,
        initialize: function() {
            this.bind('add', this.refreshNav);
            this.bind('remove', this.refreshNav);

            var collection = this;
            $('.agenda-item').click(function() {
                var item = $(this);
                var pk = parseInt(item.attr('data-id'));
                if(item.hasClass('active')) {
                    calendar.agendas = _.without(calendar.agendas, pk);
                    item.removeClass('active');
                    collection.trigger('delete_agenda', pk);
                } else {
                    calendar.agendas.push(pk);
                    item.addClass('active');
                    collection.trigger('add_agenda', pk);
                }

            });
        },
        refreshNav: function() {
            var counts = _.countBy(this.models, function(model) {
                return model.get('agenda');
            });
            $('.agenda-item[data-id]').each(function(i, item) {
                var item = $(item);
                var pk = item.attr('data-id');
                if(counts[pk] !== undefined) {
                    item.addClass('active');
                    item.find('.badge').text(counts[pk]);
                } else {
                    item.removeClass('active');
                }

            });
        },
    });

    var EventsView = Backbone.View.extend({
        url: calendar.url_root,
        initialize: function(){
            _.bindAll(this);

            this.collection.bind('reset', this.addAll);
            this.collection.bind('add', this.addOne);
            this.collection.bind('change', this.change);
            this.collection.bind('delete_agenda', this.deleteAgenda);
            this.collection.bind('add_agenda', this.addAgenda);


            this.eventView = new EventView();
            this.eventView.collection = this.collection;
        },
        render: function() {
            options.fullCalendar = $.extend(calendarOptions,
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
        deleteAgenda: function(pk) {
            $(this.el).fullCalendar('removeEvents', function(event) {
                return event.agenda == pk;
            });
        },
        change: function(event) {
            var fcEvent = $(this.el).fullCalendar('clientEvents', event.get('id'))[0];
            if(fcEvent !== undefined) {
                event = event.toJSON();
                if(typeof event.start === 'object') {
                    fcEvent.start = compileUTC(
                        $.fullCalendar.formatDate(event.start, 'u'),
                        true
                    );
                }
                if(typeof event.end === 'object') {
                    fcEvent.end = compileUTC(
                        $.fullCalendar.formatDate(event.end, 'u'),
                        true
                    );
                }
                fcEvent.title = event.title;
                $(this.el).fullCalendar('updateEvent', fcEvent);
            }
        },
        addAgenda: function(pk) {
            _.each(this.collection.where({agenda: pk}), this.addOne);
        },
        addAll: function() {
            $(this.el).fullCalendar('addEventSource', this.collection.toJSON());
        },
        addOne: function(event) {
            if(typeof event.get('start') === 'string') {
                addUTC(event);
            }
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
            if(calendar.agendas !== undefined && calendar.agendas.length > 0) {
                data.agendas = calendar.agendas;
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
