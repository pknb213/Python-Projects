import React from 'react';
import './SecondTab.css'

class SecondTab extends React.Component {
    // constructor(props) {
    //     super(props);
    //
    // }

    render() {
        return (
            <div id="Chart_Information" className="tabcontent">
                <div className="chart_info">
                    <div className="chart_cnt">
                        <h3>Work Count[CNT]</h3>
                        <div className="chart_cnt_canvas">
                            <canvas id="myCountChart_second"/>
                        </div>
                    </div>
                    <div className="chart_tmp">
                        <h3>Temperature[TMP]</h3>
                        <div className="chart_tmp_canvas">
                            <canvas id="myTempChart_second"/>
                        </div>
                    </div>
                </div>
                <div className="chart_info_an">
                    <div className="chart_an_1">
                        <h3>Analog I/O</h3>
                        <div>
                            <canvas id="myAnalog"/>
                        </div>
                    </div>
                    <div className="chart_an_2">
                        <h3>Analog I/O</h3>
                        <div className="chart_an_2_canvas">
                            <canvas id="myAnalog_second"/>
                        </div>
                    </div>
                    <div className="chart_an_3">
                        <h3>Analog I/O</h3>
                        <div className="chart_an_3_canvas">
                            <canvas id="myAnalog_third"/>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

export default SecondTab;

