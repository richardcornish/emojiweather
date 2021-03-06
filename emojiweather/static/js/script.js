EmojiWeather = (function ($) {
    return {
        emptyForm: function () {
            var $form = $('.js-search');
            if ($form.hasClass('js-search-success')) {
                $form.find('input[name="q"]').val('');
            }
        },
        geolocateAndSubmit: function () {
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
        insertDateTime: function (tz) {
            setInterval(function () {
                $('.js-moment').text(moment().tz(tz).format('dddd, MMMM D, YYYY. h:mm:ss A'));
            }, 1000);
        },
        toggleUnits: function (el) {
            $(el).click(function(){
                $(this).text(function (i, text) {
                    if ($(this).data('units') === 'si') {
                        $(this).data('units', 'us');
                        temp = parseInt($(this).data('f'), 10);
                    } else {
                        $(this).data('units', 'si');
                        temp = parseInt($(this).data('c'), 10);
                    }
                    return temp.toString().replace('-', '\u2212');
                });
            });
        },
        init: function () {
            var self = this;
            self.emptyForm();
            self.geolocateAndSubmit();
        }
    };
})(jQuery);

jQuery(function () {
    'use strict';
    EmojiWeather.init();
});
