SmsWeather = (function ($) {
    return {
        geolocate: function () {
            $('.js-geolocate').on('click', function () {
                var $form = $('.js-search');
                var $q = $form.find('input[name="q"]');
                if ('geolocation' in window.navigator && $form.length) {
                    var success = function (pos) {
                        var latitude = pos.coords.latitude;
                        var longitude = pos.coords.longitude;
                        $q.val(latitude + ', ' + longitude);
                        $form.trigger('submit');
                    };
                    var error = function (err) {
                        console.warn(err.code, err.message);
                    };
                    var options = {
                        enableHighAccuracy: true,
                        timeout: 5000,
                        maximumAge: 0
                    };
                    navigator.geolocation.getCurrentPosition(success, error, options);
                }
            });
        },
        moment: function (tz) {
            setInterval(function () {
                $('.js-moment').text(moment().tz(tz).format('MMMM Do, YYYY, H:mm:ss A'));
            }, 1000);
        },
        init: function () {
            var self = this;
            self.geolocate();
        }
    };
})(jQuery);

jQuery(function () {
    'use strict';
    SmsWeather.init();
});
