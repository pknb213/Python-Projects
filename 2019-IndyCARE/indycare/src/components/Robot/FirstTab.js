import React from 'react';
import './FirstTab.css'
import StateView from "./State";
import RobotInfoView from "./RobotInfoView";
import {EventScetion} from "./EventScetion";
import {ChartSection} from "./RobotChart";

class FirstTab extends React.Component {
    constructor(props) {
        super(props);
        console.log("FirstTab props : ");
        console.log(props);
    }

    render() {
        return (
            <div id="Robot_Information" className="tabcontent tab_contents">
                <RobotInfoView/>

                <StateView sn={this.props.sn}/>

                <EventScetion sn={this.props.sn}/>

                <ChartSection sn={this.props.sn}/>
            </div>
        );
    }
}

export default FirstTab;
