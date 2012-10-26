(function ($) {
  var $body = $('body'),
      originalImage = $body.css('background-image');
  $('[data-large-image]').each(function (index, el) {
    var $el = $(el);

    $el.hover(
      function () {
        $body.css('background-image', 'url(' + $el.data('large-image') + ')');
      },
      function () {
        $body.css('background-image', originalImage);
      }
    );
  });
})(window.jQuery);