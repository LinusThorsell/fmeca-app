<script>

    const table_array = [];
    const columnWidths = [];

    function getTable() {
    
        const array_columns = 8;
        const array_rows = 4;
        const default_column_width = 150;
    
        if (table_array.length === 0) {
            console.log("Array empty, creating example")
            for (var column = 0; column < array_columns; column++) {
                table_array[column] = [];
                columnWidths[column] = default_column_width;
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

    function getClass(column) {
        return "vis-column-" + column
    }
    function getColumnWidth(column) {
        return "width: " + columnWidths[column] + "px;"
    }

    export default {
        data() {
            return {
                getTable,
                getRow,
                getColumn,
                addRow,
                addColumn,

                getClass,
                getColumnWidth,
                columnWidths: [],
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
        <!--<div class="vis-row">
            <div v-for="column in getTable().length" 
                class="vis-columnbox"
                :style="getColumnWidth(column-1)"
                :class="getClass(column-1)"
            >
                {{ column-1 }}
            </div>
        </div> -->
        <div v-for="row in getTable()[0].length" class="vis-row">
            <div class="vis-columnbox vis-resizable-row"> Resizable Row </div>
            
            <div v-if="row-1 === 0" v-for="column in getTable().length" 
                class="vis-columnbox vis-resizable-column" 
                :style="getColumnWidth(column-1)" 
                :class="getClass(column-1)"
            >
                Resizable Column
            </div>
            
            <div v-if="row-1 !== 0" v-for="column in getTable().length" 
                class="vis-columnbox" 
                :style="getColumnWidth(column-1)" 
                :class="getClass(column-1)"
            >
                
                <!-- <div v-if="row === 1" class="vis-columnbox vis-resizable-column"> Resizable Column </div> -->
                <textarea class="vis-textarea">row: {{ row-1 }} and col: {{ column-1 }}</textarea>
            </div>
        </div>
    </div>
</template>









