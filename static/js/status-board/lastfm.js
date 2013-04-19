(function () {
    var src = new EventSource('.'),
        $trackInformation = document.querySelector('.track-information'),
        $newTrackInformation = document.querySelector('.new-track-information');

    src.addEventListener('lastfm', function (evt) {
        var trackData = JSON.parse(evt.data);

        // Add new content
        $newTrackInformation.querySelector('.track').innerText = trackData['title'];
        $newTrackInformation.querySelector('.artist').innerText = trackData['artist'];

        // Transition in the new track
        $newTrackInformation.classList.add('track-in');

        // Transition out the old track
        $trackInformation.classList.add('track-out');

        $trackInformation.addEventListener('webkitTransitionEnd', function (evt) {
            $trackInformation.classList.remove('track-transition');
            $trackInformation.classList.remove('track-out');
            $trackInformation.querySelector('.track').innerText = trackData['title'];
            $trackInformation.querySelector('.artist').innerText = trackData['artist'];
            setTimeout(function () { $trackInformation.classList.add('track-transition'); }, 0);
        }, true);

        $newTrackInformation.addEventListener('webkitTransitionEnd', function (evt) {
            $newTrackInformation.classList.remove('track-transition');
            $newTrackInformation.classList.remove('track-in');
            setTimeout(function () { $newTrackInformation.classList.add('track-transition'); }, 0);
        }, true);

    });

}());
