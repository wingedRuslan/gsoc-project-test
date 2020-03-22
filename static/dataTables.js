// Add Table with DataTables (plug-in for the jQuery Javascript library)

/* Formatting function for row details */
function format (data) {
    // `data` contains all values from selected row
    // return information in <Body> (6th column) as a child row
    return '<table cellpadding="5" cellspacing="0" border="0">'+
            '<tr>'+
                '<td>Body:</td>'+
                '<td>' + data["6"] + '</td>'+
            '</tr>'+
            '</table>';
}

$(document).ready( function () {
    // run the DataTables function on the selected table
    var table = $('#table_id').DataTable({
        "columnDefs": [
            // Hide the <Body> column
            { "visible": false, "targets": 6 },
            // Add a column for the plus icon
            {
                "className":      'details-control',
                "orderable":      false,
                "data":           null,
                "defaultContent": '',
                "targets": 0
            },
        ],
        // output table in chronological order (sorted by "CreationDate")
        "order": [[ 4, "asc" ]]
    });

    // Add event listener for opening and closing details
    $('#table_id tbody').on('click', 'td.details-control', function () {
        var tr = $(this).closest('tr');
        var row = table.row( tr );

        if ( row.child.isShown() ) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        }
        else {
            // Open this row
            row.child( format(row.data()) ).show();
            tr.addClass('shown');
        }
    });
});
