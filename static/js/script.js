/*global _, google*/
$(function () {
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
});