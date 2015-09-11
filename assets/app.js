$(document).ready(function(){
    var m = new L.Map("map").setView([47.63, -122.33], 12);
    var layer = new L.StamenTileLayer("toner-lite");
    m.addLayer(layer);

    var infoBoxText = "This map shows the increase in walking distance, in minutes, from points in Seattle to the nearest bus stop once the proposed cuts to King County Metro bus service go into effect. Assumes 3.0 mph walking speed. Distances were calculated using the Manhattan distance, as most streets in Seattle are oriented N-S. Service levels represent 'peak' hours.";

    var titleBox = L.control({position: 'topleft'});
    titleBox.onAdd = function (map) {
        var div = L.DomUtil.create('div', 'info text');
            div.innerHTML += '<h2>' + 'What is this?' + '</h4>' 
        return div;
    };
    titleBox.addTo(m);

    var textBox = L.control({position: 'topleft'});
    textBox.onAdd = function(map) {
        var div = L.DomUtil.create('div', 'info text');
            div.innerHTML += '<h4>' + infoBoxText + '</h4>' 
        return div;
    };
    textBox.addTo(m);

    d3.json("datasets/legend_ticks_data.json", function(err, data) {
        var legend = L.control({position: 'bottomright'});
        legend.onAdd = function(map) {

            var div = L.DomUtil.create('div', 'info legend'),
                grades = data,
                labels = ['<strong> Increase in walking time to nearest bus stop </strong>']

            // loop through our density intervals and generate a label with a colored square for each interval
            for (var i = 0; i < grades.length; i++) {
                div.innerHTML +=
                    '<i style="background:' + colorbrewer.YlOrRd[9][i] + '"></i> <b>' +
                    grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + ' mins <br>' : ' mins +</b>');
            }

            return div;
        };
        legend.addTo(m);
    });

    //add the data
    d3.json("datasets/delta_distance.json",function(err,data){
        function onEachFeature(feature, layer) {
            layer.setStyle({"color": colorbrewer.YlOrRd[9][feature.properties.color_idx]});
            layer.setStyle({"stroke": 0});
            layer.setStyle({"fillOpacity": 0.75});
        }

        //New GeoJSON layer
        var geojsonLayer = new L.GeoJSON(data, {
            onEachFeature: onEachFeature
        });

        //Add layer to map
        m.addLayer(geojsonLayer);
    });
});