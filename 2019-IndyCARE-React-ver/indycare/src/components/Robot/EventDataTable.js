import React from 'react';
import $ from 'jquery';
import DataTable from 'datatables.net-dt';
import DownIcon from '../../resources/Robot/icon-download.svg';

$.DataTable = DataTable;

export class EventDataTable extends React.Component {
    // constructor(props) {
    //     super(props);
    //     // this.myRef = React.createRef();
    // }

    componentDidMount(nextProps, nextState) {
        this.table = $(this.refs.main).DataTable({
            data: this.props.data,
            process: true,
            searching: false,
            paging: false,
            lengthChange: false,
            bInfo: false,
            scrollXInner: '550px',
            scrollX: '530px',
            scrollY: false,
            order: [[0, 'desc']],
            columns: [
                {"data": "occurrence_time"},
                {"data": "code"},
                {"data": "down"}
            ],
            language: {
                "emptyTable": "저장된 이벤트 데이터가 없습니다."
            }
        });
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        if (this.props.data.length > 0 && prevProps.data !== this.props.data) {
            let table = $(this.refs.main).DataTable();
            table.clear();
            table.rows.add(this.props.data);
            table.rows().every((index) => {
                let str = table.cell(index, 2).data();
                table.cell(index, 2).data(str + '<img alt="" src=' + DownIcon + '></a>');
                return true;
            });
            table.draw();
        }
    }

    getFile = (a, b) => {
        console.log("GET FILE:", a, b);
    };

    componentWillUnmount() {
        $(this.refs.main)
            .DataTable()
            .destroy(true);
    }

    render() {
        return (
            <table id="dataTable" className="" ref='main'>
                <thead>
                <tr>
                    <th>DATE</th>
                    <th>EVENT</th>
                    <th>LOG</th>
                </tr>
                </thead>
            </table>
        );
    }
}