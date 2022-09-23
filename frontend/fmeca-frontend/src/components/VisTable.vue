<script>

    const table_array = [];
    
    function getTable() {
    
        const array_columns = 4;
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

    <!-- <template>
        <table>
            <tr>
                <th v-for="column in getRow(0, getTable())">
                    <div class="table_div">
                        <h5>{{ column }}</h5>
                    </div>
                </th>
            </tr>
            <tr v-for="rows in getTable()[0].length-1">
                <td>
                    <div class="table_div_col0" style="width: fit-content; padding-left: 0.5em; padding-right: 0.5em;">
                        <h5>{{ getTable()[0][rows] }} </h5>
                    </div>
                </td>
                <td v-for="cols in getTable().length-1">
                    <div class="table_div">
                        <textarea name="" id="" cols="30" rows="10">{{ getTable()[cols][rows] }}</textarea>
                    </div>
                </td>
            </tr>
    
            <button @click="addRow([1,2,3,4,5], getTable())">Add row</button>
        </table>
    </template> -->
    









