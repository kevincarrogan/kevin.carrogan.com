/*global _, google, Hogan, Modernizr*/
$(function () {
  'use strict';
    (function ($) {
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
                var location = $(elem).data('map'),
                    result;
                geocoder.geocode(
                    {
                        address: location
                    },
                    function (result) {
                        new google.maps.Marker({
                            map: map,
                            position: result[0].geometry.location
                        });
                        bounds.extend(result[0].geometry.location);
                        $(elem).hover(
                          function (evt) {
                            map.panTo(result[0].geometry.location);
                          },
                          function (evt) {
                            map.panTo(bounds.getCenter());
                          }
                        );
                        map.setCenter(bounds.getCenter());
                        map.fitBounds(bounds);
                    }
                );
            });
        }
    }(window.jQuery));

    (function ($) {
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
    }(window.jQuery));

    (function ($) {
        if (!Modernizr.touch) {
            var template_text = '' +
                '<table class="table table-bordered table-striped">' +
                    '<tbody>' +
                        '{{#items}}' +
                        '<tr>' +
                            '<td>{{.}}</td>' +
                        '</tr>' +
                        '{{/items}}' +
                    '</tbody>' +
                '</table>'
              , template = Hogan.compile(template_text);
            _.each($('a.feed'), function (anchor) {
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
                    content: template.render({items: $anchor.data('items')})
                }
                );
            });
        }
    }(window.jQuery));

});
