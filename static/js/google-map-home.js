// Google Map For Home
(function($) {
    "use strict";

function init() {    
    var map;    
    var marker;
    var i;
    var bounds = new google.maps.LatLngBounds();
    var mapOptions = {
        
        zoom: 0,
        center: new google.maps.LatLng(41.7906594,-88.1567997),
        panControl: false,
        panControlOptions:{
            position: google.maps.ControlPosition.BOTTOM_LEFT
        },
        zoomControl:true,
        zoomControlOptions: {
            style: google.maps.ZoomControlStyle.SMALL,
            position: google.maps.ControlPosition.RIGHT_BOTTOM
        },
        disableDoubleClickZoom: true,
        mapTypeControl: true,
        mapTypeControlOptions: {
            style: google.maps.MapTypeControlStyle.DEFAULT,
        },
        scaleControl: true,
        scrollwheel: false,
        streetViewControl: true,
        streetViewControlOptions: {
            position: google.maps.ControlPosition.RIGHT_BOTTOM
        },
        draggable : true,
        overviewMapControl: true,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        styles: [ 
           { featureType: "administrative", elementType: "all", stylers: [ { visibility: "on" }, { saturation: -100 }, { lightness: 20 } ] },
           { featureType: "road", elementType: "all", stylers: [ { visibility: "on" }, { saturation: -100 }, { lightness: 40 } ] },
           { featureType: "water", elementType: "all", stylers: [ { visibility: "on" }, { saturation: -10 }, { lightness: 30 } ] },
           { featureType: "landscape.man_made", elementType: "all", stylers: [ { visibility: "simplified" }, { saturation: -60 }, { lightness: 10 } ] },
           { featureType: "landscape.natural", elementType: "all", stylers: [ { visibility: "simplified" }, { saturation: -60 }, { lightness: 60 } ] },
           { featureType: "poi", elementType: "all", stylers: [ { visibility: "off" }, { saturation: -100 }, { lightness: 60 } ] }, 
           { featureType: "transit", elementType: "all", stylers: [ { visibility: "off" }, { saturation: -100 }, { lightness: 60 } ] }
        ]
        
    }
    
    map = new google.maps.Map(document.getElementById('homeMap'), mapOptions);
    map.setTilt(45);
    
    // Multiple Markers
    var markers = [
        ['Druid Hills City, United State', 41.7946052,-88.1615305],
        ['Maple Hills', 41.7942,-88.1615526],
        ['Wedgefield', 41.7935725,-88.160356],
        ['Cress Creek', 41.7940624,-88.156912],
        ['Mill', 41.7926756,-88.154887],
        ['Meisch', 41.7941134,-88.1497371],
        ['Meisch', 41.791877,-88.1646245],
        ['Meisch', 41.792123,-88.1635623],
        ['Meisch', 41.792212,-88.1622185],
        ['Meisch', 41.7924557,-88.1607381],
        ['Meisch', 41.7902639,-88.1625539],
        ['Meisch', 41.7901319,-88.1617037],
        ['717 Burning Tree Ln', 41.7893399,-88.1575584],
        ['Burning Tree/West', 41.788783,-88.161186],
        ['Joynton Avenue, Zetland', 41.78947,-88.1586728],
        ['Joynton Avenue, Zetland', 41.788806,-88.1557974],
        ['Joynton Avenue, Zetland', 41.7895159,-88.1541988],
        ['Joynton Avenue, Zetland', 41.7920967,-88.1526029],
        ['Joynton Avenue, Zetland', 41.7933181,-88.1517044],
        ['Joynton Avenue, Zetland', 41.7929267,-88.150154],
        ['Joynton Avenue, Zetland', 41.7902945,-88.1478875]
    ];
    
    var image = [
        ['images/google-map/marker2-1.png'],
        ['images/google-map/marker1-1.png'],
        ['images/google-map/marker2-2.png'],
        ['images/google-map/marker2-1.png'],
        ['images/google-map/marker2-2.png'],
        ['images/google-map/marker2-2.png'],
        ['images/google-map/marker1-3.png'],
        ['images/google-map/marker1-1.png'],
        ['images/google-map/marker1-2.png'],
        ['images/google-map/marker2-2.png'],
        ['images/google-map/marker1-2.png'],
        ['images/google-map/marker1-2.png'],
        ['images/google-map/marker1-1.png'],
        ['images/google-map/marker1-1.png'],
        ['images/google-map/marker1-2.png'],
        ['images/google-map/marker1-1.png'],
        ['images/google-map/marker1-2.png'],
        ['images/google-map/marker1-1.png'],
        ['images/google-map/marker1-1.png'],
        ['images/google-map/marker1-3.png'],
        ['images/google-map/marker2-3.png']
    ];
    
    // Info Window Content
    var infoWindowContent = [
        [
            '<div class="info_content">' +
                '<div class="row m0 imageRow">' +
                    '<img src="images/google-map/estate-view.jpg" alt="">' +
                '</div>' +
                '<div class="row m0 description">' +
                   '<h6 class="location">awesome villa for simple family</h6>' +
                   '<p><i class="fa fa-map-marker"></i>Sydney, Australia</p>' +
				   '<span class="price-bg  font-montserrat">$ 256,596</span>' +
				   '<a href="Property-Details.html" class="btn">more details</a>' +
                '</div>' +        
            '</div>'
        ],
        
        [
            '<div class="info_content">' +
                '<div class="row m0 imageRow">' +
                    '<img src="images/google-map/estate-view.jpg" alt="">' +
                '</div>' +
                '<div class="row m0 description">' +
                   '<h6 class="location">awesome villa for simple family</h6>' +
                   '<p><i class="fa fa-map-marker"></i>Sydney, Australia</p>' +
				   '<span class="price-bg  font-montserrat">$ 256,596</span>' +
				   '<a href="Property-Details.html" class="btn">more details</a>' +
                '</div>' +        
            '</div>'
        ],
        [
            '<div class="info_content">' +
                '<div class="row m0 imageRow">' +
                    '<img src="images/google-map/estate-view.jpg" alt="">' +
                '</div>' +
                '<div class="row m0 description">' +
                   '<h6 class="location">awesome villa for simple family</h6>' +
                   '<p><i class="fa fa-map-marker"></i>Sydney, Australia</p>' +
				   '<span class="price-bg  font-montserrat">$ 256,596</span>' +
				   '<a href="Property-Details.html" class="btn">more details</a>' +
                '</div>' +        
            '</div>'
        ],
        [
            '<div class="info_content">' +
                '<div class="row m0 imageRow">' +
                    '<img src="images/google-map/estate-view.jpg" alt="">' +
                '</div>' +
                '<div class="row m0 description">' +
                   '<h6 class="location">awesome villa for simple family</h6>' +
                   '<p><i class="fa fa-map-marker"></i>Sydney, Australia</p>' +
				   '<span class="price-bg  font-montserrat">$ 256,596</span>' +
				   '<a href="Property-Details.html" class="btn">more details</a>' +
                '</div>' +        
            '</div>'
        ],
        [
            '<div class="info_content">' +
                '<div class="row m0 imageRow">' +
                    '<img src="images/google-map/estate-view.jpg" alt="">' +
                '</div>' +
                '<div class="row m0 description">' +
                   '<h6 class="location">awesome villa for simple family</h6>' +
                   '<p><i class="fa fa-map-marker"></i>Sydney, Australia</p>' +
				   '<span class="price-bg  font-montserrat">$ 256,596</span>' +
				   '<a href="Property-Details.html" class="btn">more details</a>' +
                '</div>' +        
            '</div>'
        ],
        [
            '<div class="info_content">' +
                '<div class="row m0 imageRow">' +
                    '<img src="images/google-map/estate-view.jpg" alt="">' +
                '</div>' +
                '<div class="row m0 description">' +
                   '<h6 class="location">awesome villa for simple family</h6>' +
                   '<p><i class="fa fa-map-marker"></i>Sydney, Australia</p>' +
				   '<span class="price-bg  font-montserrat">$ 256,596</span>' +
				   '<a href="Property-Details.html" class="btn">more details</a>' +
                '</div>' +        
            '</div>'
        ],
        [
            '<div class="info_content">' +
                '<div class="row m0 imageRow">' +
                    '<img src="images/google-map/estate-view.jpg" alt="">' +
                '</div>' +
                '<div class="row m0 description">' +
                   '<h6 class="location">awesome villa for simple family</h6>' +
                   '<p><i class="fa fa-map-marker"></i>Sydney, Australia</p>' +
				   '<span class="price-bg  font-montserrat">$ 256,596</span>' +
				   '<a href="Property-Details.html" class="btn">more details</a>' +
                '</div>' +        
            '</div>'
        ],
        [
            '<div class="info_content">' +
                '<div class="row m0 imageRow">' +
                    '<img src="images/google-map/estate-view.jpg" alt="">' +
                '</div>' +
                '<div class="row m0 description">' +
                   '<h6 class="location">awesome villa for simple family</h6>' +
                   '<p><i class="fa fa-map-marker"></i>Sydney, Australia</p>' +
				   '<span class="price-bg  font-montserrat">$ 256,596</span>' +
				   '<a href="Property-Details.html" class="btn">more details</a>' +
                '</div>' +        
            '</div>'
        ],
        [
            '<div class="info_content">' +
                '<div class="row m0 imageRow">' +
                    '<img src="images/google-map/estate-view.jpg" alt="">' +
                '</div>' +
                '<div class="row m0 description">' +
                   '<h6 class="location">awesome villa for simple family</h6>' +
                   '<p><i class="fa fa-map-marker"></i>Sydney, Australia</p>' +
				   '<span class="price-bg  font-montserrat">$ 256,596</span>' +
				   '<a href="Property-Details.html" class="btn">more details</a>' +
                '</div>' +        
            '</div>'
        ],
        [
            '<div class="info_content">' +
                '<div class="row m0 imageRow">' +
                    '<img src="images/google-map/estate-view.jpg" alt="">' +
                '</div>' +
                '<div class="row m0 description">' +
                   '<h6 class="location">awesome villa for simple family</h6>' +
                   '<p><i class="fa fa-map-marker"></i>Sydney, Australia</p>' +
				   '<span class="price-bg  font-montserrat">$ 256,596</span>' +
				   '<a href="Property-Details.html" class="btn">more details</a>' +
                '</div>' +        
            '</div>'
        ],
        [
            '<div class="info_content">' +
                '<div class="row m0 imageRow">' +
                    '<img src="images/google-map/estate-view.jpg" alt="">' +
                '</div>' +
                '<div class="row m0 description">' +
                   '<h6 class="location">awesome villa for simple family</h6>' +
                   '<p><i class="fa fa-map-marker"></i>Sydney, Australia</p>' +
				   '<span class="price-bg  font-montserrat">$ 256,596</span>' +
				   '<a href="Property-Details.html" class="btn">more details</a>' +
                '</div>' +        
            '</div>'
        ],
        [
            '<div class="info_content">' +
                '<div class="row m0 imageRow">' +
                    '<img src="images/google-map/estate-view.jpg" alt="">' +
                '</div>' +
                '<div class="row m0 description">' +
                   '<h6 class="location">awesome villa for simple family</h6>' +
                   '<p><i class="fa fa-map-marker"></i>Sydney, Australia</p>' +
				   '<span class="price-bg  font-montserrat">$ 256,596</span>' +
				   '<a href="Property-Details.html" class="btn">more details</a>' +
                '</div>' +        
            '</div>'
        ],
        [
            '<div class="info_content">' +
                '<div class="row m0 imageRow">' +
                    '<img src="images/google-map/estate-view.jpg" alt="">' +
                '</div>' +
                '<div class="row m0 description">' +
                   '<h6 class="location">awesome villa for simple family</h6>' +
                   '<p><i class="fa fa-map-marker"></i>Sydney, Australia</p>' +
				   '<span class="price-bg  font-montserrat">$ 256,596</span>' +
				   '<a href="Property-Details.html" class="btn">more details</a>' +
                '</div>' +        
            '</div>'
        ],
        [
            '<div class="info_content">' +
                '<div class="row m0 imageRow">' +
                    '<img src="images/google-map/estate-view.jpg" alt="">' +
                '</div>' +
                '<div class="row m0 description">' +
                   '<h6 class="location">awesome villa for simple family</h6>' +
                   '<p><i class="fa fa-map-marker"></i>Sydney, Australia</p>' +
				   '<span class="price-bg  font-montserrat">$ 256,596</span>' +
				   '<a href="Property-Details.html" class="btn">more details</a>' +
                '</div>' +        
            '</div>'
        ],
        [
            '<div class="info_content">' +
                '<div class="row m0 imageRow">' +
                    '<img src="images/google-map/estate-view.jpg" alt="">' +
                '</div>' +
                '<div class="row m0 description">' +
                   '<h6 class="location">awesome villa for simple family</h6>' +
                   '<p><i class="fa fa-map-marker"></i>Sydney, Australia</p>' +
				   '<span class="price-bg  font-montserrat">$ 256,596</span>' +
				   '<a href="Property-Details.html" class="btn">more details</a>' +
                '</div>' +        
            '</div>'
        ],
        [
            '<div class="info_content">' +
                '<div class="row m0 imageRow">' +
                    '<img src="images/google-map/estate-view.jpg" alt="">' +
                '</div>' +
                '<div class="row m0 description">' +
                   '<h6 class="location">awesome villa for simple family</h6>' +
                   '<p><i class="fa fa-map-marker"></i>Sydney, Australia</p>' +
				   '<span class="price-bg  font-montserrat">$ 256,596</span>' +
				   '<a href="Property-Details.html" class="btn">more details</a>' +
                '</div>' +        
            '</div>'
        ],
        [
            '<div class="info_content">' +
                '<div class="row m0 imageRow">' +
                    '<img src="images/google-map/estate-view.jpg" alt="">' +
                '</div>' +
                '<div class="row m0 description">' +
                   '<h6 class="location">awesome villa for simple family</h6>' +
                   '<p><i class="fa fa-map-marker"></i>Sydney, Australia</p>' +
				   '<span class="price-bg  font-montserrat">$ 256,596</span>' +
				   '<a href="Property-Details.html" class="btn">more details</a>' +
                '</div>' +        
            '</div>'
        ],
        [
            '<div class="info_content">' +
                '<div class="row m0 imageRow">' +
                    '<img src="images/google-map/estate-view.jpg" alt="">' +
                '</div>' +
                '<div class="row m0 description">' +
                   '<h6 class="location">awesome villa for simple family</h6>' +
                   '<p><i class="fa fa-map-marker"></i>Sydney, Australia</p>' +
				   '<span class="price-bg  font-montserrat">$ 256,596</span>' +
				   '<a href="Property-Details.html" class="btn">more details</a>' +
                '</div>' +        
            '</div>'
        ],
        [
            '<div class="info_content">' +
                '<div class="row m0 imageRow">' +
                    '<img src="images/google-map/estate-view.jpg" alt="">' +
                '</div>' +
                '<div class="row m0 description">' +
                   '<h6 class="location">awesome villa for simple family</h6>' +
                   '<p><i class="fa fa-map-marker"></i>Sydney, Australia</p>' +
				   '<span class="price-bg  font-montserrat">$ 256,596</span>' +
				   '<a href="Property-Details.html" class="btn">more details</a>' +
                '</div>' +        
            '</div>'
        ],
        [
            '<div class="info_content">' +
                '<div class="row m0 imageRow">' +
                    '<img src="images/google-map/estate-view.jpg" alt="">' +
                '</div>' +
                '<div class="row m0 description">' +
                   '<h6 class="location">awesome villa for simple family</h6>' +
                   '<p><i class="fa fa-map-marker"></i>Sydney, Australia</p>' +
				   '<span class="price-bg  font-montserrat">$ 256,596</span>' +
				   '<a href="Property-Details.html" class="btn">more details</a>' +
                '</div>' +        
            '</div>'
        ],
    ];
    
    // Display multiple markers on a map    
    var infoWindow = new google.maps.InfoWindow(), marker, i;
    
    // Loop through our array of markers & place each one on the map  
    for( i = 0; i < markers.length; i++ ) {
        var position = new google.maps.LatLng(markers[i][1], markers[i][2]);
        bounds.extend(position);
        marker = new google.maps.Marker({
            position: position,
            map: map,
            icon: image[i][0],
            title: markers[i][0]
        });
        
        // Allow each marker to have an info window    
        google.maps.event.addListener(marker, 'click', (function(marker, i) {
            return function() {
                infoWindow.setContent(infoWindowContent[i][0]);
                infoWindow.open(map, marker);
            }
        })(marker, i));
        
        // Allow each marker to have an info window    
        google.maps.event.addListener(map, 'click', (function(marker, i) {
            return function() {
                infoWindow.close(map, marker);
            }
        })(marker, i));

        // Automatically center the map fitting all markers on the screen
        map.fitBounds(bounds);
    }
    
    
  
    google.maps.event.addListener(infoWindow, 'domready', function() {

        // Reference to the DIV that wraps the bottom of infowindow
        var iwOuter = $('.gm-style-iw');

        var iwBackground = iwOuter.prev();
        // Removes background shadow DIV
        iwBackground.children(':nth-child(1)').css({'display' : 'none'});

        // Removes white background DIV
        iwBackground.children(':nth-child(2)').css({'display' : 'none'});
        
        // Removes background shadow DIV
        iwBackground.children(':nth-child(3)').css({'display' : 'none'});

        // Removes white background DIV
        iwBackground.children(':nth-child(4)').css({'display' : 'none'});

        // Moves the infowindow 115px to the right.
        iwOuter.parent().parent().css({left: '22px',top: '27px'});
        
        // Moves the shadow of the arrow 76px to the left margin.
        iwBackground.children(':nth-child(1)').attr('style', function(i,s){ return s + 'left: 76px !important;'});

        // Moves the arrow 76px to the left margin.
        iwBackground.children(':nth-child(3)').attr('style', function(i,s){ return s + 'left: 76px !important;'});

        // Changes the desired tail shadow color.
        iwBackground.children(':nth-child(3)').find('div').children().css({'box-shadow': 'rgba(72, 181, 233, 0.6) 0px 1px 6px', 'z-index' : '1'});

        // Reference to the div that groups the close button elements.
        var iwCloseBtn = iwOuter.next();

        // Apply the desired effect to the close button
        iwCloseBtn.css({opacity: '0', right: '38px', top: '3px', border: '7px solid #48b5e9', 'border-radius': '13px', 'box-shadow': '0 0 5px #3990B9'});
        
    });
}
google.maps.event.addDomListener(window, 'load', init)
    
})(jQuery);