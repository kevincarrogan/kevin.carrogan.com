(function ($, mq) {
  var $html = $('html'),
      originalImage = $html.css('background-image');
  $('[data-large-image]').each(function (index, el) {
    var $el = $(el),
        imageUrl = $el.data('large-image'),
        img = new Image();

    img.src = imageUrl;

    $el.hover(
      function () {
        if (mq('only screen and (min-width: 50em)')) {
          $html.css('background-image', 'url(' + imageUrl + ')');
        }
      },
      function () {
        if (mq('only screen and (min-width: 50em)')) {
          $html.css('background-image', originalImage);
        }
      }
    );
  });
})(window.jQuery, window.Modernizr.mq);

(function ($, mq) {
  var $mapContainer = $('.personal-map'),
      location = [],
      mapOptions,
      map,
      geocoder,
      bounds;

  geocoder = new google.maps.Geocoder();
  bounds = new google.maps.LatLngBounds();

  mapOptions = {
    center: bounds.getCenter(),
    zoom: 8,
    mapTypeId: google.maps.MapTypeId.ROADMAP,
    disableDefaultUI: true,
    mapTypeControl: false,
    panControl: false,
    scaleControl: false,
    zoomControl: false,
    draggable: false
  };
  map = new google.maps.Map($mapContainer.get(0), mapOptions);

  $('a[data-map]').each(function (i, elem) {
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

  $('.personal-information').hover(
    function (evt) {
      if (mq('only screen and (min-width: 50em)')) {
        $mapContainer.css('opacity', 1);
      }
    },
    function (evt) {
      if (mq('only screen and (min-width: 50em)')) {
        $mapContainer.css('opacity', 0);
      }
    }
  );
})(window.jQuery, window.Modernizr.mq);