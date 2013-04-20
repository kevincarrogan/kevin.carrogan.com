(function () {

    var src = new EventSource('.'),
        $trackInformation = $('.track-information'),
        $newTrackInformation = $('.new-track-information');

    src.addEventListener('lastfm', function (evt) {
        var trackData = JSON.parse(evt.data);

        // Add new content
        $newTrackInformation.find('.track').text(trackData['title']);
        $newTrackInformation.find('.artist').text(trackData['artist']);

        // Transition in the new track
        $newTrackInformation.addClass('track-in');

        // Transition out the old track
        $trackInformation.addClass('track-out');

        $trackInformation.get(0).addEventListener('webkitTransitionEnd', function (evt) {
            $trackInformation.removeClass('track-transition');
            $trackInformation.removeClass('track-out');
            $trackInformation.find('.track').text(trackData['title']);
            $trackInformation.find('.artist').text(trackData['artist']);
            setTimeout(function () { $trackInformation.addClass('track-transition'); }, 0);
        }, true);

        $newTrackInformation.get(0).addEventListener('webkitTransitionEnd', function (evt) {
            $newTrackInformation.removeClass('track-transition');
            $newTrackInformation.removeClass('track-in');
            setTimeout(function () { $newTrackInformation.addClass('track-transition'); }, 0);
        }, true);

    });

}());
