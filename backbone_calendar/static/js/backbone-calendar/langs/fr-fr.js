var calendarOptions = {
    header: {
        left: 'prev,next today',
        center: 'title',
        right: 'month,agendaWeek,agendaDay',
    },
    firstDay: 1,
    titleFormat: {
        month: 'MMMM yyyy',
        week:"'Semaine du' dd [yyyy] {'au' [MMM] dd MMM yyyy}",
        day: 'dddd dd MMM yyyy'
    },
    columnFormat: {
        month: 'ddd',
        week: 'ddd dd/M',
        day: 'dddd dd/M' 
    },
    timeFormat: {
        '': 'HH:mm',
        agenda: 'H:mm{ - H:mm}'
    },
    firstDay:1,
    firstTime: 17,
    buttonText: {
        today: 'aujourd\'hui',
        day: 'jour',
        week:'semaine',
        month:'mois'
    }, 
    axisFormat: 'H:mm',
    monthNames: [
        'Janvier','Février','Mars','Avril',
        'Mai','Juin','Juillet','Août',
        'Septembre','Octobre','Novembre','Décembre',
    ],
    monthNamesShort:[
        'janv.','févr.','mars','avr.','mai','juin',
        'juil.','août','sept.','oct.','nov.','déc.',
    ],
    dayNames: [
        'Dimanche','Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi',
    ],
    dayNamesShort: [
        'Dim', 'Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam',
    ],
    datetimepicker: {
        dateFormat: 'dd-mm-yy',
        timeFormat: 'HH:mm',
    },

};
