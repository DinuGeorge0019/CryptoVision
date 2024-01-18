
window.addEventListener('load', function() {

    var dataDict = JSON.parse(document.getElementById('crypto_his_data').textContent);

    for (var i = 0; i < dataDict.length; i++) {
        var symbol = dataDict[i].symbol;
        var data = JSON.parse(dataDict[i].record);  

        var parsedData = {
            dates: data.map(item => new Date(item.dateTime)),
            opens: data.map(item => parseFloat(item.open)),
            highs: data.map(item => parseFloat(item.high)),
            lows: data.map(item => parseFloat(item.low)),
            closes: data.map(item => parseFloat(item.close)),
        };
                
        var trace = {
            x: parsedData.dates,
            close: parsedData.closes,
            high: parsedData.highs,
            low: parsedData.lows,
            open: parsedData.opens,
        
            increasing: {line: {color: 'rgba(164, 190, 58, 1)'}},
            decreasing: {line: {color: 'red'}},
        
            type: 'candlestick',
            xaxis: 'x',
            yaxis: 'y'
        };
        
        var plotData = [trace];
        
        var layout = {
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
                },
            }
        };
        
        var config = {displayModeBar: false};

        Plotly.newPlot(symbol + '_his_plot', plotData, layout, config);

        // Hide the plot initially
        document.getElementById(symbol + '_his_plot').style.display = 'none';
    }

    // Add event listeners to the coin boxes
    var coinBoxes = document.getElementsByClassName('coin_box');
    for (var i = 0; i < coinBoxes.length; i++) {
        coinBoxes[i].addEventListener('click', function() {

            // Hide all plots
            for (var i = 0; i < dataDict.length; i++) {
                var symbol = dataDict[i].symbol;
                document.getElementById(symbol + '_his_plot').style.display = 'none';
                document.getElementById(symbol + '_table').style.display = 'none';
            }

            // Show the plot for the selected coin
            var symbol = this.querySelector('.coin h1').textContent;
            document.getElementById(symbol + '_his_plot').style.display = 'block';

            // Show the table for the selected symbol
            document.getElementById(symbol + '_table').style.display = 'block';

        });
    }

    // Trigger a click event on the first coin_box
    if (coinBoxes.length > 0) {
        coinBoxes[0].click();
    }

});