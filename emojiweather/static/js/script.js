EmojiWeather = (function ($) {
    return {
        emptyForm: function () {
            var $form = $('.js-search');
            if ($form.hasClass('js-search-success')) {
                $form.find('input[name="q"]').val('');
            }
        },
        submitSeachForm: function () {
            var $form = $('.js-search');
            var $submit = $form.find(':submit');
            $form.on('submit', function () {
                $(this).find('button').prop('disabled', true);
                var icon = $submit.find('svg').prop('outerHTML');
                var feedback = ['Searching', 'Searching.', 'Searching..', 'Searching...'];
                var counter = 0;
                setInterval(function () {
                    $submit.html(icon + feedback[counter]);
                    if (counter < feedback.length - 1) {
                        counter++;
                    } else {
                        counter = 0;
                    }
                }, 300);
            });
        },
        geolocateAndSubmit: function () {
            $('.js-geolocate').on('click', function () {
                var $form = $('.js-search');
                var $q = $form.find('input[name="q"]');
                $q.prop('disabled', true);
                var feedback = ['Locating', 'Locating.', 'Locating..', 'Locating...'];
                var counter = 0;
                var insertLocating = setInterval(function () {
                    $q.val(feedback[counter]);
                    if (counter < feedback.length - 1) {
                        counter++;
                    } else {
                        counter = 0;
                    }
                }, 300);
                if ('geolocation' in window.navigator && $form.length) {
                    var success = function (pos) {
                        clearInterval(insertLocating);
                        var latitude = pos.coords.latitude;
                        var longitude = pos.coords.longitude;
                        $q.prop('disabled', false).val(latitude + ', ' + longitude);
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
        insertDateTime: function (tz) {
            setInterval(function () {
                $('.js-moment').text(moment().tz(tz).format('MMMM Do, YYYY, H:mm:ss A'));
            }, 1000);
        },
        init: function () {
            var self = this;
            self.emptyForm();
            self.submitSeachForm();
            self.geolocateAndSubmit();
        }
    };
})(jQuery);

jQuery(function () {
    'use strict';
    EmojiWeather.init();
});
