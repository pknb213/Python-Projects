# React

### `DataTable Install method`
    
    npm install --save jszip
    npm install --save pdfmake
    npm install --save datatables.net-dt
    npm install --save datatables.net-autofill-dt
    npm install --save datatables.net-buttons-dt
    npm install --save datatables.net-colreorder-dt
    npm install --save datatables.net-fixedcolumns-dt
    npm install --save datatables.net-fixedheader-dt
    npm install --save datatables.net-keytable-dt
    npm install --save datatables.net-responsive-dt
    npm install --save datatables.net-rowgroup-dt
    npm install --save datatables.net-rowreorder-dt
    npm install --save datatables.net-scroller-dt
    npm install --save datatables.net-select-dt

### `Using the Module`

    require( 'jszip' );
    require( 'pdfmake' );
    require( 'datatables.net-dt' )();
    require( 'datatables.net-autofill-dt' )();
    require( 'datatables.net-buttons-dt' )();
    require( 'datatables.net-buttons/js/buttons.colVis.js' )();
    require( 'datatables.net-buttons/js/buttons.flash.js' )();
    require( 'datatables.net-buttons/js/buttons.html5.js' )();
    require( 'datatables.net-buttons/js/buttons.print.js' )();
    require( 'datatables.net-colreorder-dt' )();
    require( 'datatables.net-fixedcolumns-dt' )();
    require( 'datatables.net-fixedheader-dt' )();
    require( 'datatables.net-keytable-dt' )();
    require( 'datatables.net-responsive-dt' )();
    require( 'datatables.net-rowgroup-dt' )();
    require( 'datatables.net-rowreorder-dt' )();
    require( 'datatables.net-scroller-dt' )();
    require( 'datatables.net-select-dt' )();

### `Common Js method`
    var $  = require( 'jquery' );
    var dt = require( 'datatables.net' )( window, $ );
    
    class Table extends Component { 
        componentDidMount() {
            $(this.refs.main).DataTable({
               dom: '<"data-table-wrapper"t>',
               data: this.props.names,
               columns,
               ordering: false
            });
        }  
        componentWillUnmount(){
           $('.data-table-wrapper')
           .find('table')
           .DataTable()
           .destroy(true);
        }
        shouldComponentUpdate() {
            return false;
        }
        render() {
            return (
                <div>
                    <table ref="main" />
                </div>);
        }
    }

### `Reload`

    function reloadTableData(names) {
        const table = $('.data-table-wrapper')
                      .find('table')
                      .DataTable();
        table.clear();
        table.rows.add(names);
        table.draw();
}

    
    function updateTable(names) {
        const table = $('.data-table-wrapper')
                      .find('table')
                      .DataTable();
        let dataChanged = false;
        table.rows().every(function () {
            const oldNameData = this.data();
            const newNameData = names.find((nameData) => {
                return nameData.name === oldNameData.name;
            });
            
            if (oldNameData.nickname !== newNameData.nickname) {
                dataChanged = true;
                this.data(newNameData);
            }
            
            return true; // RCA esLint configuration wants us to 
                         // return something
        });
        
        if (dataChanged) {
            table.draw();
        }
    }
    
    shouldComponentUpdate(nextProps) {
        if (nextProps.names.length !== this.props.names.length) {
            reloadTableData(nextProps.names);
        } else {
            updateTable(nextProps.names);
        }
    return false;
}


# React-data-table-component

`import DataTable from 'react-data-table-component';`

###`Basic Table`

    const data = [{ id: 1, title: 'Conan the Barbarian', year: '1982' } ...];
    const columns = [
      {
        name: 'Title',
        selector: 'title',
        sortable: true,
      },
      {
        name: 'Year',
        selector: 'year',
        sortable: true,
        right: true,
      },
    ];
     
    class MyComponent extends Component {
      render() {
        return (
          <DataTable
            title="Arnold Movies"
            columns={columns}
            data={data}
          />
        )
      }
    );
    
###`Selectable Rows`

    const handleChange = (state) => {
      // You can use setState or dispatch with something like Redux so we can use the retrieved data
      console.log('Selected Rows: ', state.selectedRows);
    };
     
    class MyComponent extends Component {
      render() {
          return (
            <DataTable
              title="Arnold Movies"
              columns={columns}
              data={data}
              selectableRows // add for checkbox selection
              onRowSelected={handleChange}
            />
        )
      }
    );
    
    
###`clearing`
    
    // set the initial state
    state = { toggledClearRows: false }
    ...
     
    const handleChange = (state) => {
      // You can use setState or dispatch with something like Redux so we can use the retrieved data
      console.log('Selected Rows: ', state.selectedRows);
    };
     
    // Toggle the state so React Table Table changes to `clearSelectedRows` are triggered
    const handleClearRows = () => {
      this.setState({ toggledClearRows: !this.state.toggledClearRows})
    }
     
    class MyComponent extends Component {
      render() {
        return (
          <DataTable
            title="Arnold Movies"
            columns={columns}
            data={data}
            selectableRows // add for checkbox selection
            onRowSelected={handleChange}
            clearSelectedRows={this.state.toggledClearRows}
          />
        )
      }
    );


