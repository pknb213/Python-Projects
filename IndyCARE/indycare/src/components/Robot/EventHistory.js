import React from 'react';
import iconHistory from "../../resources/Robot/icon-history.svg";
import iconMore from "../../resources/Robot/icon-more.svg";
import {EventDataTable} from "./EventDataTable";
import $ from "jquery";
import {Modal} from "./Modal";
import Axios from "axios";

export class EventHistoryView extends React.Component {
    constructor(props) {
        super(props);
        this.openModal = this.openModal.bind(this);
        this.closeModal = this.closeModal.bind(this);
        this.getMainData = this.getMainData.bind(this);
        this.getModalData = this.getModalData.bind(this);
        this.state = {
            source: new EventSource("http://121.67.47.157:8884/stream?channel="
                + this.props.sn + "_event"),
            mainRes: [],
            modalRes: []
        };
    }

    componentDidMount() {
        let modal = $(this.refs.modal)[0];
        const {source} = this.state;
        source.addEventListener('message', event => {
            this.getMainData();
            this.getModalData();
        });
        window.onclick = (event) => {
            if (event.target === modal) {
                modal.style.display = "none";
            }
        };
        this.getMainData();
        this.getModalData();
    }

    getMainData = () => {
        Axios.get('http://121.67.47.157:8884/datatable/events/' + this.props.sn + '/limit')
            .then(res => {
                this.setState({mainRes: res.data});
            }).catch(e => {
            alert(e);
        });
    };

    getModalData = () => {
        Axios.get('http://121.67.47.157:8884/datatable/events/' + this.props.sn + '/all')
            .then(res => {
                this.setState({modalRes: res.data});
            }).catch(e => {
            alert(e);
        });
    };

    // 가능하면 Modal은 하위 Component의 isOpen State를 전달함으로써 컨트롤 해야 함. 현재 CSS 이용.
    openModal = () => {
        $(this.refs.modal)[0].style.display = 'block';
    };

    closeModal = () => {
        $(this.refs.modal)[0].style.display = 'none';
    };

    render() {
        return (
            <div className="event_history">
                <div className="section_title">
                    <img src={iconHistory} alt="icon_event_history"/>
                    <h3>Event History</h3>
                    <div className="more">
                        <button id="history_Btn" onClick={this.openModal}>
                            <span>더보기</span>
                            <img src={iconMore} alt="icon_more"/>
                        </button>
                        <div id="history_Modal" className="more_modal" ref='modal'>
                            <div className="modal-content">
                                <span className="close" ref='close' onClick={this.closeModal}>&times;</span>
                                <Modal sn={this.props.sn} data={this.state.modalRes}/>
                            </div>
                        </div>
                    </div>
                </div>
                <EventDataTable sn={this.props.sn} data={this.state.mainRes}/>
            </div>
        );
    }
}