import React from 'react';
import Chart from 'chart.js';

let myLineChart;

// Chart.default.global.defaultFontFamily = "'PT Sans', sans-serif";
// Chart.default.global.legend.display = false;

export default class LineGraph extends React.PureComponent {
    chartRef = React.createRef();

    componentDidMount() {
        this.buildChart();
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        this.buildChart();
    }

    buildChart = () => {
        let myChartRef = this.chartRef.current.getContext("2d");
        myChartRef.canvas.width = '1200px';
        myChartRef.canvas.height = '300px';
        let {data} = this.props;
        if (data === null) data = new Array(5);

        if (typeof myLineChart !== "undefined") myLineChart.destroy();

        myLineChart = new Chart(myChartRef, {
            type: 'line',
            data: {
                // Bring in data
                //labels: ['a', 'b', 'c', 'd', 'e', 'f'],
                // labels: labels
                datasets: [
                    {
                        label: "Joint 1",
                        //data: [16, 46, 23, 72, 55, 78],
                        // data: [{'x': '11-06 03:16:00', 'y': 53},
                        // {'x': '11-06 03:15:00', 'y': 11},
                        // {'x': '11-06 03:14:00', 'y': 34},
                        // {'x': '11-06 03:13:00', 'y': 78}],
                        data: data[0],
                        fill: false,
                        backgroundColor: "rgba(255,99,132,0.2)",
                        borderColor: "rgba(255,99,132)",
                        borderWidth: 1,
                        lineTension: 0.2,
                        pointRadius: 1.5
                    },
                    {
                        label: "Joint 2",
                        //data: [77, 42, 12, 33, 55, 88],
                        // data: [{'x': '11-06 03:16:00', 'y': 34},
                        // {'x': '11-06 03:15:00', 'y': 21},
                        // {'x': '11-06 03:14:00', 'y': 66},
                        // {'x': '11-06 03:13:00', 'y': 54}],
                        data: data[1],
                        fill: false,
                        backgroundColor: "rgba(255,205,86,0.2)",
                        borderColor: "rgba(255,205,86)",
                        borderWidth: 1,
                        lineTension: 0.2,
                        pointRadius: 1.5
                    },
                    {
                        label: "Joint 3",
                        //data: [77, 42, 12, 33, 55, 88],
                        // data: [{'x': '11-06 03:16:00', 'y': 34},
                        // {'x': '11-06 03:15:00', 'y': 21},
                        // {'x': '11-06 03:14:00', 'y': 66},
                        // {'x': '11-06 03:13:00', 'y': 54}],
                        data: data[2],
                        fill: false,
                        backgroundColor: "rgba(75,192,192,0.2)",
                        borderColor: "rgba(75,192,192)",
                        borderWidth: 1,
                        lineTension: 0.2,
                        pointRadius: 1.5
                    },
                    {
                        label: "Joint 4",
                        //data: [77, 42, 12, 33, 55, 88],
                        // data: [{'x': '11-06 03:16:00', 'y': 34},
                        // {'x': '11-06 03:15:00', 'y': 21},
                        // {'x': '11-06 03:14:00', 'y': 66},
                        // {'x': '11-06 03:13:00', 'y': 54}],
                        data: data[3],
                        fill: false,
                        backgroundColor: "rgba(255,159,64,0.2)",
                        borderColor: "rgba(255,159,64)",
                        borderWidth: 1,
                        lineTension: 0.2,
                        pointRadius: 1.5
                    },
                    {
                        label: "Joint 5",
                        //data: [77, 42, 12, 33, 55, 88],
                        // data: [{'x': '11-06 03:16:00', 'y': 34},
                        // {'x': '11-06 03:15:00', 'y': 21},
                        // {'x': '11-06 03:14:00', 'y': 66},
                        // {'x': '11-06 03:13:00', 'y': 54}],
                        data: data[4],
                        fill: false,
                        backgroundColor: "rgba(54,162,235,0.2)",
                        borderColor: "rgba(54,162,23)",
                        borderWidth: 1,
                        lineTension: 0.2,
                        pointRadius: 1.5
                    },
                    {
                        label: "Joint 6",
                        //data: [77, 42, 12, 33, 55, 88],
                        // data: [{'x': '11-06 03:16:00', 'y': 34},
                        // {'x': '11-06 03:15:00', 'y': 21},
                        // {'x': '11-06 03:14:00', 'y': 66},
                        // {'x': '11-06 03:13:00', 'y': 54}],
                        data: data[5],
                        fill: false,
                        backgroundColor: "rgba(255,99,132,0.2)",
                        borderColor: "rgba(255,99,132)",
                        borderWidth: 1,
                        lineTension: 0.2,
                        pointRadius: 1.5
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
                animation: false,
                scales: {
                    xAxes: [{
                        //barThickness: 30,
                        type: 'time',
                        time: {
                            padding: 15,
                            fontStyle: "bold",
                            parser: 'YY-MM-DD HH:mm:ss',
                            unit: 'minute',
                            unitStepSize: 5,
                            displayFormat: {
                                hour: 'MM-DD HH:mm'
                            }
                        },
                        ticks: {
                            autoSkip: true,
                            source: 'auto'
                        }
                    }],
                    // yAxes: [{
                    //     scaleLabel: {
                    //         labelString: 'Temperature',
                    //     },
                    //     ticks: {
                    //         fontColor: "rgba(0,0,0,1)",
                    //         fontStyle: "bold",
                    //         maxTicksLimit: 10,
                    //         //minValue: 20,
                    //         //padding: 15,
                    //         beginAtZero: false,
                    //         stepValue: 5,
                    //         steps: 10
                    //     }
                    // }]
                }
            }
        })
    };

    render() {
        return (
            <div className="chart_section">
                <h3>Temperature [TMP]</h3>
                <div className="chart_tmp">
                    <canvas id="myTempChart" ref={this.chartRef}/>
                </div>
            </div>
        );
    }
}