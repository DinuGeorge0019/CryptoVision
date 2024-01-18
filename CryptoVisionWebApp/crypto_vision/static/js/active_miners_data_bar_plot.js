
window.addEventListener('load', function() {

    // Replace single quotes with double quotes, but not inside date strings
    var validJsonString = document.getElementById('active_miners_and_value_data').textContent.replace(/'([^']*)'/g, '"$1"');

    // Now you can parse the JSON string
    var data = JSON.parse(validJsonString);

    var dates = data.map(item => item.date.date);
    var counts = data.map(item => parseInt(item.count));

    var trace = {
        x: dates,
        y: counts,
        type: 'bar',
        marker: {
            color: 'rgba(0, 0, 255, 1)' // Blue color
        }
    };

    var plotData = [trace];

    var layout = {
        title: 'BTC Active Miners',
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
            title: 'Active Miners',
            titlefont: {
                color: 'rgba(217, 217, 217, 1)'
            },
            tickfont: {
                color: 'rgba(217, 217, 217, 1)'
            }
        }
    };

    var config = {displayModeBar: false};

    Plotly.newPlot('active_miners_plot', plotData, layout, config);
});