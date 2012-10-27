(function ($) {
  var $html = $('html'),
      originalImage = $html.css('background-image');
  $('[data-large-image]').each(function (index, el) {
    var $el = $(el),
        imageUrl = $el.data('large-image'),
        img = new Image();

    img.src = imageUrl;

    $el.hover(
      function () {
        $html.css('background-image', 'url(' + imageUrl + ')');
      },
      function () {
        $html.css('background-image', originalImage);
      }
    );
  });
})(window.jQuery);