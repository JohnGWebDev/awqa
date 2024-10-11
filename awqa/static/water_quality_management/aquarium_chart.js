CANVAS = document.getElementById('aquariumChart');
var chartInnerWidth = document.getElementById('tabsContainer').clientWidth - 20;
console.log(chartInnerWidth)
const dataElement = document.getElementById('chart-data');
const chartData = JSON.parse(dataElement.textContent);

var entry_fields = [];
for (entry in chartData) {
    entry_fields.push(chartData[entry].fields);
}

var date_created_list = [];
var pH_list = [];
var high_range_pH_list = [];
var ammonia_list = [];
var nitrate_list = [];
var nitrite_list = [];

for (entry in entry_fields) {
    currentEntry = entry_fields[entry];
    date_created_list.push(currentEntry.date_created);
    pH_list.push(currentEntry.ph);
    high_range_pH_list.push(currentEntry.high_range_ph);
    ammonia_list.push(currentEntry.ammonia);
    nitrate_list.push(currentEntry.nitrate);
    nitrite_list.push(currentEntry.nitrite);
}

var pH = {
    x: date_created_list,
    y: pH_list,
    name: 'pH',
    type: 'scatter'
};
var high_range_pH = {
    x: date_created_list,
    y: high_range_pH_list,
    name: 'High Range pH',
    type: 'scatter'
};
var ammonia = {
    x: date_created_list,
    y: ammonia_list,
    name: 'Ammonia (ppm)',
    type: 'scatter'
};
var nitrates = {
    x: date_created_list,
    y: nitrate_list,
    name: 'Nitrates (ppm)',
    type: 'scatter'
};
var nitrites = {
    x: date_created_list,
    y: nitrite_list,
    name: 'Nitrites (ppm)',
    type: 'scatter'
};
var data = [pH, high_range_pH, ammonia, nitrates, nitrites];
var layout = {
    title: {
        text: 'Water Quality Chart',
        font: {
            family: "Fredoka",
            size: 22,
            weight: 'lighter',
        }
    },
    width: chartInnerWidth,
    autosize: true,
    margin: {
        b: 30,
        l: 30,
        r: 30,
    },
    showlegend: true,
    legend: {
        x: 1,
        xanchor: 'right',
        y: 1
    }
}
var config = {responsive: true}

Plotly.newPlot(CANVAS, data, layout, config);