
window.addEventListener('load', function() {

    // Replace single quotes with double quotes, but not inside date strings
    var validJsonString = document.getElementById('active_miners_and_value_data').textContent.replace(/'([^']*)'/g, '"$1"');

    // Now you can parse the JSON string
    var data = JSON.parse(validJsonString);

    var dates = data.map(item => item.date.date);
    var values = data.map(item => parseInt(item.value));

    var trace = {
        x: dates,
        y: values,
        type: 'bar',
        marker: {
            color: 'rgba(255, 255, 0, 1)' // Yellow color
        }
    };

    var plotData = [trace];

    var layout = {
        title: 'BTC Mined Value',
        titlefont: {
            color: 'rgba(217, 217, 217, 1)'
        },
        showlegend: false,
        plot_bgcolor: "rgba(217, 217, 217, 1)",
        paper_bgcolor: "rgba(128, 128, 128, 0)",
        xaxis: {
            autorange: true,
            domain: [0, 1],
            title: 'Date',
            titlefont: {
                color: 'rgba(217, 217, 217, 1)'
            },
            tickfont: {
                color: 'rgba(217, 217, 217, 1)'
            }
        },
        yaxis: {
            autorange: true,
            domain: [0, 1],
            type: 'linear',
            title: 'Mined Value',
            titlefont: {
                color: 'rgba(217, 217, 217, 1)'
            },
            tickfont: {
                color: 'rgba(217, 217, 217, 1)'
            }
        }
    };

    var config = {displayModeBar: false};

    Plotly.newPlot('mined_value_plot', plotData, layout, config);
});