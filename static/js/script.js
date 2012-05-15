/*global _, google, Hogan*/
$(function () {
    (function () {
        if (!Modernizr.touch) {
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
        }
    }());

    (function () {
        if (!Modernizr.touch) {
            _.each($('a[data-static-map]'), function (anchor) {
                var $anchor = $(anchor)
                  , location = $anchor.data('static-map');
                $anchor.popover(
                {
                    placement: function (tip, element) {
                        var offset = $(element).offset()
                          , height = $(document).outerHeight()
                          , width = $(document).outerWidth()
                          , vert = 0.5 * height - offset.top
                          , vertPlacement = vert > 0 ? 'bottom' : 'top'
                          , horiz = 0.5 * width - offset.left
                          , horizPlacement = horiz > 0 ? 'right' : 'left'
                          , placement = Math.abs(horiz) > Math.abs(vert) ?  horizPlacement : vertPlacement;
                        return placement;
                    },
                    content: '<img height="250px" width="250px" src="http://maps.googleapis.com/maps/api/staticmap?center=' + location + '&zoom=10&size=250x250&maptype=roadmap&sensor=false&markers=color:red%7C' + location + '" />'
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
                    placement: function (tip, element) {
                        var offset = $(element).offset()
                          , height = $(document).outerHeight()
                          , width = $(document).outerWidth()
                          , vert = 0.5 * height - offset.top
                          , vertPlacement = vert > 0 ? 'bottom' : 'top'
                          , horiz = 0.5 * width - offset.left
                          , horizPlacement = horiz > 0 ? 'right' : 'left'
                          , placement = Math.abs(horiz) > Math.abs(vert) ?  horizPlacement : vertPlacement;
                        return placement;
                    },
                    content: template.render({recent_tracks: $anchor.data('recent-tracks')})
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
                        '{{#recent_bookmarks}}' +
                        '<tr>' +
                            '<td>{{title}}</td>' +
                        '</tr>' +
                        '{{/recent_bookmarks}}' +
                    '</tbody>' +
                '</table>'
              , template = Hogan.compile(template_text);
            _.each($('a.recent-bookmarks'), function (anchor) {
                var $anchor = $(anchor);
                $anchor.popover(
                {
                    placement: function (tip, element) {
                        var offset = $(element).offset()
                          , height = $(document).outerHeight()
                          , width = $(document).outerWidth()
                          , vert = 0.5 * height - offset.top
                          , vertPlacement = vert > 0 ? 'bottom' : 'top'
                          , horiz = 0.5 * width - offset.left
                          , horizPlacement = horiz > 0 ? 'right' : 'left'
                          , placement = Math.abs(horiz) > Math.abs(vert) ?  horizPlacement : vertPlacement;
                        return placement;
                    },
                    content: template.render({recent_bookmarks: $anchor.data('recent-bookmarks')})
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
                        '{{#recent_tweets}}' +
                        '<tr>' +
                            '<td>{{title}}</td>' +
                        '</tr>' +
                        '{{/recent_tweets}}' +
                    '</tbody>' +
                '</table>'
              , template = Hogan.compile(template_text);
            _.each($('a.recent-tweets'), function (anchor) {
                var $anchor = $(anchor);
                $anchor.popover(
                {
                    placement: function (tip, element) {
                        var offset = $(element).offset()
                          , height = $(document).outerHeight()
                          , width = $(document).outerWidth()
                          , vert = 0.5 * height - offset.top
                          , vertPlacement = vert > 0 ? 'bottom' : 'top'
                          , horiz = 0.5 * width - offset.left
                          , horizPlacement = horiz > 0 ? 'right' : 'left'
                          , placement = Math.abs(horiz) > Math.abs(vert) ?  horizPlacement : vertPlacement;
                        return placement;
                    },
                    content: template.render({recent_tweets: $anchor.data('recent-tweets')})
                }
                );
            });
        }
    }());

});