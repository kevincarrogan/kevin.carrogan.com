/*global _, google, Hogan*/
$(function () {
    (function () {
        var locations = []
          , mapOptions
          , map
          , geocoder
          , bounds;

        geocoder = new google.maps.Geocoder();
        bounds = new google.maps.LatLngBounds();

        mapOptions = {
            center: bounds.getCenter(),
            zoom: 8,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        map = new google.maps.Map($('#personal-map').get(0), mapOptions);

        _.each($('a[data-map]'), function (elem) {
            var location = $(elem).data('map')
              , marker;
            geocoder.geocode(
                {
                    address: location
                },
                function (result) {
                    marker = new google.maps.Marker({
                        map: map,
                        position: result[0].geometry.location
                    });
                    map.setCenter(result[0].geometry.location);
                    bounds.extend(result[0].geometry.location);
                }
            );
        });
        map.fitBounds(bounds);
    }());

    (function () {
        if (!Modernizr.touch) {
            _.each($('a[data-static-map]'), function (anchor) {
                var $anchor = $(anchor)
                  , location = $anchor.data('static-map');
                $anchor.popover(
                {
                    'placement': 'bottom',
                    'title': location,
                    'content': '<img height="250px" width="250px" src="http://maps.googleapis.com/maps/api/staticmap?center=' + location + '&zoom=10&size=250x250&maptype=roadmap&sensor=false&markers=color:red%7C' + location + '" />'
                }
                );
            });
        }
    }());

    (function () {
        if (!Modernizr.touch) {
            var template_text = '' +
                '<table class="table table-bordered table-striped">' +
                    '<tbody>' +
                        '{{#recent_tracks}}' +
                        '<tr>' +
                            '<td>{{title}}</td>' +
                        '</tr>' +
                        '{{/recent_tracks}}' +
                    '</tbody>' +
                '</table>'
              , template = Hogan.compile(template_text);
            _.each($('a.recently-played'), function (anchor) {
                var $anchor = $(anchor);
                $anchor.popover(
                {
                    'placement': 'bottom',
                    'title': 'Last.FM',
                    'content': template.render({recent_tracks: $anchor.data('recent-tracks')})
                }
                );
            });
        }
    }());

});