import React from 'react';
import CamView from "./Cam";
import {EventHistoryView} from "./EventHistory";

export class EventScetion extends React.Component {
    // constructor(props) {
    //     super(props);
    // }

    render() {
        return (
            <div className="event_section">
                <CamView sn={this.props.sn}/>
                <EventHistoryView sn={this.props.sn}/>
            </div>
        );
    }

}