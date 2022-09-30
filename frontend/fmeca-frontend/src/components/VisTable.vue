<script>

    const table_array = [];
    
    function getTable() {
    
        const array_columns = 8;
        const array_rows = 4;
    
        if (table_array.length === 0) {
            console.log("Array empty, creating example")
            for (var column = 0; column < array_columns; column++) {
                table_array[column] = [];
                for (var row = 0; row < array_rows; row++) {
                    table_array[column][row] = "Column: " + column + " Row: " + row;
                }
            }
        }
    
        return table_array;
    }
    
    function getRow(index, table_array) {
        const Row = [];
        for (var column = 0; column < table_array.length; column++) {
            Row[column] = table_array[column][index];
        }
    
        // console.log("Columns of array")
        // console.log(Row)
        
        return Row;
    }
    function getColumn(index, table_array) {
        return table_array[index]
    }
    
    function addRow(row, table_array) {
        if (row.length !== table_array[0].length) {
            console.log("Error: in addRow. Input row not of same length as input array.")
        }
    
        var table_array_column_length = table_array[0].length
        for (var i = 0; i < getRow(0, table_array).length; i++) {
            table_array[i][table_array_column_length] = row[i];
        }
        console.log(table_array)
    }
    
    function addColumn() {
    
    }
 
    export default {
        data() {
            return {
                getTable,
                getRow,
                getColumn,
                addRow,
                addColumn,     
            }
        }
    }

    </script>
    
<style>
   @import './style/VisTable.css'
</style>

<template>
    <div id="vis-table">
        <!--<div id="vis-header">
            Header info
        </div> -->
        <div v-for="row in getTable()[0].length" class="vis-row">
            <div v-for="column in getTable().length" class="vis-columnbox">
                row: {{ row-1 }} and col: {{ column-1 }}
            </div>
        </div>
    </div>
</template>









