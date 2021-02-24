var ee = require('@google/earthengine');
var privateKey = require("./privateKey.json");
var CLIENT_ID = 0123456789;

var initialize = function() {
  ee.initialize(null, null, function() {
  }, function(e) {
    console.error('Initialization error: ' + e);
  });
};
ee.data.authenticateViaOauth(CLIENT_ID, initialize, function(e) {
  console.error('Authentication error: ' + e);
}, null, function() {
  ee.data.authenticateViaPopup(initialize);
});

ee.data.authenticateViaPrivateKey(privateKey, runAnalysis, function(e) {
  console.error('Authentication error: ' + e);
});

// ee.data.authenticateViaOauth(CLIENT_ID);
ee.data.authenticateViaPrivateKey(privateKey);
ee.initialize();

var geometry = ee.Geometry.Rectangle([-179.999, -90, 180, 90], 'EPSG:4326', false);
var dataset = new ee.ImageCollection('MODIS/006/MCD43A4')
                    .filterDate('2020-10-01', '2021-02-07')
                    .filterBounds(geometry);

var trueColor = dataset.select([
    'Nadir_Reflectance_Band1', 'Nadir_Reflectance_Band4',
    'Nadir_Reflectance_Band3'
]).max();

var trueColorVis = {
  min: 0.0,
  max: 4000.0,
  gamma: 1.4,
};
var trueColor = trueColor.visualize(trueColorVis);

Map.setCenter(-7.03125, 31.0529339857, 2);
Map.addLayer(trueColor, null, 'True Color');

Export.image.toDrive({
  image: trueColor,
  description: 'test',
  scale: 10000,
  region: geometry
});
