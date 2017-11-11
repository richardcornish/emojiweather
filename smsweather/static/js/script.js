$(document).ready(function () {
    var $form = $('form');
    var $q = $form.find('input[name="q"]');
    $q.focus();
    $q.get(0).setSelectionRange(0, $q.val().length);
    if ('geolocation' in window.navigator && $form.length) {
        var success = function (pos) {
            var latitude = pos.coords.latitude;
            var longitude = pos.coords.longitude;
            $q.val(latitude + ',' + longitude);
            $form.trigger('submit', function () {
                $.get({
                    url: $form.attr('action'),
                    data: $form.serialize()
                });
            });
        };
        var error = function (err) {
            console.warn(err.code, err.message);
        };
        var options = {
            enableHighAccuracy: true,
            timeout: 5000,
            maximumAge: 0
        };
        if (!$q.val()) {
            navigator.geolocation.getCurrentPosition(success, error, options);
        }
    }
});
