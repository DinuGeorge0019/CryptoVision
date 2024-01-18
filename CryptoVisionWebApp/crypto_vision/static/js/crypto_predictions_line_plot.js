
window.addEventListener('load', function() {

    console.log('HELLO FROM CRYPTO');

    // Replace single quotes with double quotes, but not inside date strings
    var validJsonString = document.getElementById('crypto_predictions_result').textContent.replace(/'([^']*)'/g, '"$1"');

    console.log(validJsonString);

    // Now you can parse the JSON string
    var bitcoin_prices = JSON.parse(validJsonString);

    var dates = [];
    var now = new Date();
    
    for (var i = 0; i < bitcoin_prices.length; i++) {
        var newDate = new Date(now);
        newDate.setMinutes(now.getMinutes() + 30 * i);
        dates.push(newDate);
    }

    var trace = {
        x: dates,
        y: bitcoin_prices,
    
        increasing: {line: {color: 'rgba(164, 190, 58, 1)'}},
        decreasing: {line: {color: 'red'}},
    
        type: 'lines+markers',
        xaxis: 'x',
        yaxis: 'y'
    };

    var plotData = [trace];

    var layout = {
        showlegend: false,
        plot_bgcolor: "rgba(217, 217, 217, 1)",
        paper_bgcolor: "rgba(128, 128, 128, 0)",

        title: 'BTC Predicted Price For The Next 7 Days',
        titlefont: {
            color: 'rgba(217, 217, 217, 1)'
        },

        xaxis: {
            autorange: true,
            domain: [0, 1],
            title: 'Date',
            titlefont: {
                color: 'rgba(217, 217, 217, 1)'
            },
            tickfont: {
                color: 'rgba(217, 217, 217, 1)'
            },
            rangeslider: {
                visible: true
            },
            rangeselector: {
                buttons: [
                    {
                        count: 1,
                        label: '24h',
                        step: 'day',
                        stepmode: 'backward',
                        bgcolor: 'rgba(217, 217, 217, 1)'
                    },
                    {
                        count: 7,
                        label: '7d',
                        step: 'day',
                        stepmode: 'backward',
                        bgcolor: 'rgba(217, 217, 217, 1)'
                    },
                    {
                        step: 'all',
                        label: 'All',
                        bgcolor: 'rgba(217, 217, 217, 1)'
                    }
                ]
            }
        },
        yaxis: {
            autorange: true,
            domain: [0, 1],
            type: 'linear',
            title: 'Price in USD',
            titlefont: {
                color: 'rgba(217, 217, 217, 1)'
            },
            tickfont: {
                color: 'rgba(217, 217, 217, 1)'
            }
        }
    };

    var config = {displayModeBar: false};

    Plotly.newPlot('crypto_predictions_plot', plotData, layout, config);
});