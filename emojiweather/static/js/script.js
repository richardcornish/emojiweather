EmojiWeather = (function ($, google) {
    return {
        emptyForm: function () {
            var $form = $('.js-search');
            if ($form.hasClass('js-search-success')) {
                $form.find('input[name="q"]').val('');
            }
        },
        geolocateAndSubmit: function () {
            $('.js-geolocate').on('click', function () {
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
                $('.js-moment').text(moment().tz(tz).format('MMMM Do, YYYY, h:mm:ss A'));
            }, 1000);
        },
        drawMap: function (selector, latitude, longitude) {
            var minimal = [
                {
                    "elementType": "labels",
                    "stylers": [{
                        "visibility": "off"
                    }]
                },
                {
                    "featureType": "administrative",
                    "elementType": "geometry",
                    "stylers": [{
                        "visibility": "off"
                    }]
                },
                {
                    "featureType": "administrative.land_parcel",
                    "stylers": [{
                        "visibility": "off"
                    }]
                },
                {
                    "featureType": "administrative.neighborhood",
                    "stylers": [{
                        "visibility": "off"
                    }]
                },
                {
                    "featureType": "poi",
                    "stylers": [{
                        "visibility": "off"
                    }]
                },
                {
                    "featureType": "road",
                    "stylers": [{
                        "visibility": "off"
                    }]
                },
                {
                    "featureType": "road",
                    "elementType": "labels.icon",
                    "stylers": [{
                        "visibility": "off"
                    }]
                },
                {
                    "featureType": "transit",
                    "stylers": [{
                        "visibility": "off"
                    }]
                }
            ];
            var el = $(selector).get(0);
            var options = {
                zoom: 10,
                center: new google.maps.LatLng(latitude, longitude),
                mapTypeId: 'roadmap',
                styles: minimal,
                disableDefaultUI: true
            };
            new google.maps.Map(el, options);
        },
        init: function () {
            var self = this;
            self.emptyForm();
            self.geolocateAndSubmit();
        }
    };
})(jQuery, google);

jQuery(function () {
    'use strict';
    EmojiWeather.init();
});
