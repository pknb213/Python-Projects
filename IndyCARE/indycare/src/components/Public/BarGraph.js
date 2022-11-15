import React from 'react';
import Chart from 'chart.js';

let myBarChart;

// Chart.default.global.defaultFontFamily = "'PT Sans', sans-serif";
// Chart.default.global.legend.display = false;

export default class BarGraph extends React.PureComponent {
    chartRef = React.createRef();

    componentDidMount() {
        this.buildChart();
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        this.buildChart();
    }

    buildChart = () => {
        let myChartRef = this.chartRef.current.getContext("2d");
        myChartRef.canvas.width = '490px';
        myChartRef.canvas.height = '300px';
        let gradientStroke = myChartRef.createLinearGradient(0, 0, 0, 400);
        gradientStroke.addColorStop(0, "#439CFA");
        gradientStroke.addColorStop(1, "#439CFA");
        let gradientFill = myChartRef.createLinearGradient(0, 0, 0, 400);
        gradientFill.addColorStop(0, "rgba(173,215,255,1)");
        gradientFill.addColorStop(1, "rgba(173,215,255,0.4");

        const {data} = this.props;

        if (typeof myBarChart !== "undefined") myBarChart.destroy();

        myBarChart = new Chart(myChartRef, {
            type: 'bar',
            data: {
                // Bring in data
                //labels: ['a', 'b', 'c', 'd', 'e', 'f'],
                // labels: labels
                datasets: [
                    {
                        label: "Count",
                        //data: [16, 46, 23, 72, 55, 78],
                        data: data,
                        fill: true,
                        borderColor: gradientStroke,
                        pointBorderColor: gradientStroke,
                        pointBackgroundColor: gradientStroke,
                        pointBorderWidth: 2,
                        pointHoverRadius: 2,
                        pointRadius: 2,
                        backgroundColor: gradientFill,
                        //hoverBackgroundColor:
                        hoverBorderColor: "#FACD83",
                        borderWidth: 2.5,
                    }
                ]
            },
            options: {
                //Customize chart options
                legend: {
                    position: "bottom"
                },
                tooltips: {
                    mode: 'index',
                    intersect: false,
                },
                hover: {
                    mode: 'nearest',
                    intersect: false,
                    animationDuration: 0
                },
                scales: {
                    xAxes: [{
                        barThickness: 45,
                        type: 'time',
                        time: {
                            padding: 15,
                            fontStyle: "bold",
                            parser: 'YY-MM-DD HH:mm:ss',
                            unit: 'minute',
                            // unitStepSize: 10,
                            displayFormat: {
                                hour: 'MM-DD HH:mm'
                            }
                        },
                        ticks: {
                            autoSkip: true,
                            maxTicksLimit: 10,
                            source: 'auto'
                        }
                    }],
                    yAxes: [{
                        scaleLabel: {
                            //display: true,
                            //labelString: 'Work Count'
                        },
                        ticks: {
                            fontColor: "rgba(0,0,0,0.8)",
                            fontStyle: "bold",
                            suggestedMax: 100,
                            beginAtZero: true,
                            stepSize: 10
                        }
                    }],
                    tooltips: {
                        intersect: false,
                        mode: 'index',
                        callbacks: {
                            label: function (tooltipItem, myData) {
                                var label = myData.datasets[tooltipItem.datasetIndex].label || '';
                                if (label) {
                                    label += ': ';
                                }
                                label += parseFloat(tooltipItem.value).toFixed(2);
                                return label;
                            }
                        }
                    }
                }
            }
        })
    };

    render() {
        return (
            <div className="chart_section">
                <h3>WorK Count [CNT]</h3>
                <div className="chart_cnt">
                    <canvas id="myCountChart" ref={this.chartRef}/>
                </div>
            </div>
        );
    }
}