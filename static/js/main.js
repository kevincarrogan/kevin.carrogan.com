(function ($) {
  var $html = $('html'),
      originalImage = $html.css('background-image');
  $('[data-large-image]').each(function (index, el) {
    var $el = $(el);

    $el.hover(
      function () {
        $html.css('background-image', 'url(' + $el.data('large-image') + ')');
      },
      function () {
        $html.css('background-image', originalImage);
      }
    );
  });
})(window.jQuery);