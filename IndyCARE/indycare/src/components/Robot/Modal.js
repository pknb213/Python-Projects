import React from 'react';
import $ from 'jquery';
import DataTable from 'datatables.net-dt';
import DownIcon from '../../resources/Robot/icon-download.svg';

$.DataTable = DataTable;

export class Modal extends React.Component {
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
            bInfo: false,
            order: [[0, 'asc']],
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

    componentWillUnmount() {
        $('.event_history')
            .find('dataTable_history')
            .DataTable()
            .destroy(true);
    }

    render() {
        return (
            <div className="history_table">
                <h2>All Event History</h2>
                <table id="dataTable_history" className="" ref="main">
                    <thead>
                    <tr>
                        <th>DATE</th>
                        <th>EVENT</th>
                        <th>LOG</th>
                    </tr>
                    </thead>
                </table>
            </div>
        )
    }
}

/*
<React.Fragment>
    {
        isOpen ?
            <React.Fragment>
                <div className="history_table">
                    <h2>All Event History</h2>
                    <table id="dataTable_history" className="">
                        <thead>
                        <tr>
                            <th>DATE</th>
                            <th>EVENT</th>
                            <th>LOG</th>
                        </tr>
                        </thead>
                    </table>
                </div>
            </React.Fragment>
            :
            null
    }
</React.Fragment>
*/