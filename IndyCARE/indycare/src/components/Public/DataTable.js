import React from "react";
import Axios from 'axios';
import './DataTable.css';
import $ from 'jquery';
import DataTable from 'datatables.net-dt';
import Monitering from '../../resources/List/icon_monitoring.svg'

$.DataTable = DataTable;


class DataTableComponent extends React.Component {
    // constructor(props) {
    //     super(props);
    //
    // }

    componentDidMount(nextProps, nextState) {
        Axios.get('http://121.67.47.157:8884/datatable/robots/all')
            .then(res => {
                console.log(res);
                this.table = $(this.refs.main).DataTable({
                    data: res.data,
                    process: true,
                    searching: false,
                    paging: false,
                    lengthChange: false,
                    bInfo: false,
                    order: [[0, 'desc']],
                    columns: [
                        {data: 'sn'},
                        {data: 'model'},
                        {data: 'site'},
                        {data: 'company'},
                        {data: 'kpi'},
                        {data: 'header'},
                        {data: 'state'},
                        {data: 'enter'},
                    ]
                });
                this.table.rows().every((index)=> {
                     let str = this.table.cell(index, 7).data();
                     this.table.cell(index, 7).data(str + '<img alt="" src=' + Monitering + '></a>');
                     return true;
                });
            })
            .catch(e => {
                alert(e);
            })
            .finally(() => {

            });
    }

    componentDidUpdate() {
    }

    componentWillUnmount() {
        $('.data-table-wrapper')
            .find('dataTable')
            .DataTable()
            .destroy(true);
    }

    render() {
        return (
            <div className="list_contents_table">
                <table id="dataTable" className="table_style" ref='main'>
                    <thead>
                    <tr>
                        <th>SN</th>
                        <th>Model</th>
                        <th>Site</th>
                        <th>Company</th>
                        <th>KPI</th>
                        <th>Header</th>
                        <th>State</th>
                        <th>Enter</th>
                    </tr>
                    </thead>
                </table>
            </div>
        );
    }
}

export default DataTableComponent;