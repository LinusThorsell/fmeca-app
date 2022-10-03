<script>
import '../worker/vis-table-worker.js'

    //var vis_table_worker = null;

    var selector, rule, i, /*rowStyles=[], // not currently in use*/ colStyles=[];

    const table_array = [];
    const columnWidths = [];

    const array_columns = 100;
    const array_rows = 100;
    const default_column_width = 150;


    function getTable() {    
    
        if (table_array.length === 0) {
            console.log("Array empty, creating example")
            for (var column = 0; column < array_columns; column++) {
                table_array[column] = [];
                for (var row = 0; row < array_rows; row++) {
                    table_array[column][row] = "Column: " + column + " Row: " + row;
                }
            }
        }
        
        //setupResizeEventListeners()
        
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

    function getClass(column, row) {
        return "vis-column-" + column + " vis-row-" + row;
    }
    function getColumnWidth(column) {
        return "width: " + columnWidths[column] + "px;"
    }
    
    function calculateWidthOfRows() {
        var max_width = 0;

        var rows = document.querySelector('.vis-row')
        Array.from(rows.childNodes).forEach(column => {
            if (column.offsetWidth > 0) {
                max_width += column.offsetWidth;
            }
        });
        
        /*var temp_width = max_width + 1000 + "px;"
        document.querySelectorAll('.vis-row').forEach(row => {
            row.style.width = temp_width;
        });*/

        document.getElementById("vis-table").style.width = max_width + 100 + "px";
    }

    //const resizeWorker = new Worker(vistableworker)
    function handleResize({ width }, { __currentTarget__ }) {
        
        var column_array = __currentTarget__.classList[2]
        var column_id = column_array.slice(column_array.lastIndexOf('-')+1)
        console.log(column_id)
        colStyles[parseInt(column_id)].width=width+"px"
       // console.log(colStyles[parseInt(__currentTarget__.classList[2].slice(-1))]);

        calculateWidthOfRows()

        //colStyles[__currentTarget__.classList[2]:1]
        //vis_table_worker.postMessage({ 
        //    action: "fix_column_sizes", 
        //    document: "" 
        //})

        // console.log(column[2].offsetWidth)
        /*column.forEach((col, index) => {
            var diff = Math.abs(column[index].offsetWidth - width)
            if (3 < diff && index <= 10) {
                // change width.
                // let temp = Math.floor(width/10)*10;
                col.style.width = width + "px";
                calculateWidthOfRows()
            h}
            else if (30 < diff && 2 < index && index <= 30) {
                col.style.width = width + "px";
                calculateWidthOfRows()
            }
            else if (60 < diff && 20 < index && index <= 100) {
                col.style.width = width + "px";
                calculateWidthOfRows()
            }
        })*/
    }

    function generateCustomStylesheet() {
        console.log("Generating stylesheet")
        
        //var numRows=9, numCols=9;
        
        document.getElementsByTagName('head')[0].appendChild(document.createElement('style'));
        var sheet=document.styleSheets[1];
//Or instead of creating a new sheet we could just get the first exisiting one like this:
//var sheet=document.styleSheets[0]; 
//Create rules dynamically
        /*for (i=0; i<array_rows; i++) {
            selector=".vis-row-"+i;
            rule="{height: 300px;}";
            if (sheet.insertRule)
                sheet.insertRule(selector+rule, 0);//This puts the rule at index 0
            
            rowStyles[i]=(sheet.cssRules)[0].style;//Remember you have to fetch the rules-array from the sheet and not hold on to the old rules-array, since a new one is created during each insertion. Oh, and IE does things differently again; cssRules instead of rules
        }*/
        
        for (i=0; i<array_columns; i++) {
            selector=".vis-column-"+i;
            rule="{width: " + default_column_width + "px;}";
            if (sheet.insertRule)
                sheet.insertRule(selector+rule, 0);
            colStyles[i]=(sheet.cssRules)[0].style;
        }

        console.log(document.styleSheets)
    }
    
    export default {
        mounted() {
            //vis_table_worker = new Worker(new URL('./../worker/vis-table-worker.js', import.meta.url))
            generateCustomStylesheet()
            //calculateWidthOfRows()
            //console.log(document.styleSheets)
        },

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
                handleResize,
            }
        }
    }

    </script>
    
<style>
   @import './style/VisTable.css'
</style>

<template>
    {{ $log("Rerender") }}
    <div id="vis-table">
        <div v-for="row in getTable()[0].length" class="vis-row">
            <div class="vis-columnbox vis-resizable-row"> Resizable Row </div>
            
            <div v-if="row-1 === 0" v-for="column in getTable().length" 
                class="vis-columnbox vis-resizable-column" 
                :class="getClass(column-1, row-2)"
                v-resize="handleResize"
            >
                Resizable Column
            </div>
            
            <div v-if="row-1 !== 0" v-for="column in getTable().length" 
                class="vis-columnbox" 
                :class="getClass(column-1, row-1)"
            >
                
                <!-- <div v-if="row === 1" class="vis-columnbox vis-resizable-column"> Resizable Column </div> -->
                <textarea class="vis-textarea">row: {{ row-1 }} and col: {{ column-1 }}</textarea>
            </div>
        </div>
    </div>
    <!--{{ setupResizeEventListeners() }}-->
</template>









