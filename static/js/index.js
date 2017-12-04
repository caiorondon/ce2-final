$(function() {

  var map;
  var marker;
  var flag = false;
  var start_marker;
  var end_marker;
  var steps = 20;
  var airplane;
  var airplane_id;

  function createRandomString( length ) {
    var str = "";
    for ( ; str.length < length; str += Math.random().toString( 36 ).substr( 2 ) );
    return str.substr( 0, length );
  }

  function set_location(location){
    map.removeMarkers();
    map.removePolygons();

    GMaps.geocode({
    address: location,
    callback: function(results, status) {
      if (status == 'OK') {
        var latlng = results[0].geometry.location;
        map.setCenter(latlng.lat(), latlng.lng());
        marker = map.addMarker({
          lat: latlng.lat(),
          lng: latlng.lng()
        });

        map.drawCircle({
          lat: latlng.lat(),
          lng: latlng.lng(),
          radius: 3000,
          fillColor: 'yellow',
          fillOpacity: 0.5,
          strokeWeight: 0
        });

      } else {
        set_location("UNB");
        alert("Não foi possível encontrar esse local");
      }
    }
    });
  };

  function init(){
    map = new GMaps({
      div: '#gmaps',
      lat: 0,
      lng: 0,
      zoom: 13
    });

    set_location('UNB');
  };

  init();

  $('.set-location-a').click(function(event){
    event.preventDefault();
    var end = prompt("Digite um novo endereço", "UnB");

    if (end == null || end == "") {
      set_location("UNB");
    } else {
      set_location(end);
    }
  });

  $('.start-path-a').click(function(event){
    event.preventDefault();

    alert("Marque no mapa o ponto de inicio da trajetoria");

    var click = GMaps.on('click', map.map, function(event) {
      map.removeMarker(start_marker);
      var lat = event.latLng.lat();
      var lng = event.latLng.lng();

      var markerImage = new google.maps.MarkerImage("static/sources/start.png",
                new google.maps.Size(30, 30),
                new google.maps.Point(0, 0),
                new google.maps.Point(15, 15));

      start_marker = map.addMarker({
        lat: lat,
        lng: lng,
        title: 'Start',
        icon: markerImage
      });

      google.maps.event.removeListener(click);
    });
  });

  $('.end-path-a').click(function(event){
    event.preventDefault();

    alert("Marque no mapa o ponto que representa o fim da trajetoria");

    var click = GMaps.on('click', map.map, function(event) {
      map.removeMarker(end_marker);
      var lat = event.latLng.lat();
      var lng = event.latLng.lng();

      var markerImage = new google.maps.MarkerImage("static/sources/stop.png",
                new google.maps.Size(30, 30),
                new google.maps.Point(0, 0),
                new google.maps.Point(15, 15));

      end_marker = map.addMarker({
        lat: lat,
        lng: lng,
        title: 'End',
        icon: markerImage,
        size: "small"
      });

      google.maps.event.removeListener(click);
    });
  });

  $('.start-simulation-a').click(function(event){
    event.preventDefault();

    if (start_marker == null || end_marker == null){
      alert("Inicio/fim do trajeto precisa ser definido.");
      return;
    }

    var path = [];

    for (i = 0; i < steps; i++){
      var lt, lg;

      lt = end_marker.getPosition().lat() - start_marker.getPosition().lat();
      lt = lt / (steps - 1) * (i);
      lt = start_marker.getPosition().lat() + lt;

      lg = end_marker.getPosition().lng() - start_marker.getPosition().lng();
      lg = lg / (steps - 1) * (i);
      lg = start_marker.getPosition().lng() + lg;

      path.push([lt, lg]);

    }

    console.log(path);
    map.removePolylines();
    map.drawPolyline({
      path: path,
      strokeColor: '#131540',
      strokeOpacity: 0.6,
      strokeWeight: 3
    });

    // send device position
    var sendInfo = {
       type: 'meta', // altitude de 4 km
       latitude: marker.getPosition().lat(),
       longitude: marker.getPosition().lng()
   };

   airplane_id = createRandomString(6);

   $.ajax({
       type: "POST",
       url: "/",
       dataType: "json",
       data: sendInfo
   });

    $.each(path, function( index, value ) {
      setTimeout(function(){
        map.removeMarker(airplane);

        var markerImage = new google.maps.MarkerImage("static/sources/airplane.png",
                  new google.maps.Size(40, 40),
                  new google.maps.Point(0, 0),
                  new google.maps.Point(20, 20));

        airplane = map.addMarker({
          lat: value[0],
          lng: value[1],
          title: 'Airplane',
          icon: markerImage,
          size: "small"
        });


        var sendInfo = {
           type: 'data', // altitude de 4 km
           altitude: '4000', // altitude de 4 km
           airplane_id: airplane_id,
           latitude: value[0].toString(),
           longitude: value[1].toString()
       };

       $.ajax({
           type: "POST",
           url: "/",
           dataType: "json",
           data: sendInfo
       });
      }, 3000 * index);
    });


  });

});
