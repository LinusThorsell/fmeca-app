<script>
import { vis_table_store } from './vis-table-store.js'

    export default {
        mounted() {
            generateCustomStylesheet()

            setTimeout(() => {
                /*
                    Function to fix bug on most chromium based browsers.
                    Required for resizing to work on a majority of browsers
                    that do not support native custom stylesheets.

                    Firefox will gain a performance advantage for supporting this,
                    while for example Google Chrome has to be forced to reload the
                    styles by nudging the elements downwards slightly.
                */

                // Get all the 'Loading...' text elements, and nudge the rest down slightly.
                document.getElementsByClassName("chrome_is_messy_fix")[0].style.height="100px";
                // Wait until the stylesheet is triggered to reload, then hide elements.
                setTimeout(() => {
                    Array.from(document.getElementsByClassName("chrome_is_messy_fix")).forEach(div => {
                        div.style.display="none";
                    });
                }, 500);
            }, 1500);
        },
        

        data() {
            return {
                removeColumn,
                restoreColumns,
                setupTable,
                getRow,
                getColumn,
                addRow,
                addColumn,

                getClass,
                handleResize,
                getTableFromBackend,
                vis_table_store,
            }
        },
        //methods: {
           /* setTable(table) {
                this.table_array = table
            },*/
        //},
    }
    
    var selector, rule, i, /*rowStyles=[],*/ colStyles=[];

    const array_columns = 4;
    const array_rows = 4;
    const default_column_width = 100;

    // Gets entire table ( TODO : interface with backend here )
    function setupTable() {    

        if (vis_table_store.getRowCount() === 0) {
            const temp_array = []
            console.log("Array empty, creating example")
            for (var column = 0; column < array_columns+1; column++) {
                temp_array[column] = [];
                for (var row = 0; row < array_rows+1; row++) {
                    temp_array[column][row] = "";
                }
            }
            vis_table_store.setArray(temp_array)
        }
        // return table_array;
    }
   
    // Gets a specific row ( index ) as an array from the input array ( table_array ).
    function getRow(index, table_array) {
        const Row = [];
        for (var column = 0; column < table_array.length; column++) {
            Row[column] = table_array[column][index];
        }
    
        return Row;
    }

    // Gets a specific column ( index ) as an array from the input array ( table_array )
    function getColumn(index, table_array) {
        return table_array[index]
    }

    function removeColumn(column) {
        console.log(column)
        colStyles[column-1].display="none";
    }

    function restoreColumns() {
        console.log(vis_table_store.getColumnCount())
        for(i = 0; i < vis_table_store.getColumnCount(); i++)
        {
            colStyles[i].display = "flex";
        }
    }
    
    // TODO : Fix, Is currently not working with rest of program structure.
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
    // TODO : Fix, Implement function
    function addColumn() {
    
    }

    // Gets the class for a specific vis-columnbox element.
    // These styles are used by the generated stylesheet to allow resizing.
    function getClass(column, row) {
        return "vis-column-" + column + " vis-row-" + row;
    }
    
    // Calculates with of a row, to resize table container element to fit all content.
    function calculateWidthOfRows() {
        var max_width = 0;

        var rows = document.querySelector('.vis-row')
        Array.from(rows.childNodes).forEach(column => {
            if (column.offsetWidth > 0) {
                max_width += column.offsetWidth;
            }
        });

        document.getElementById("vis-table").style.width = max_width + 100 + "px";
    }

    // Called by vue-resize-observer when a column is resized.
    // Changes stylesheet to resize elements
    function handleResize({ width }, { __currentTarget__ }) {
        
        var column_array = __currentTarget__.classList[2]
        var column_id = column_array.slice(column_array.lastIndexOf('-')+1)
        console.log(column_id)
        colStyles[parseInt(column_id)].width=width+"px"

        calculateWidthOfRows()
    }

    // Generates custom stylesheet.
    // Used to effectively resize big amounts of elements fast.
    function generateCustomStylesheet() {
        console.log("Generating stylesheet")
        document.getElementsByTagName('head')[0].appendChild(document.createElement('style'));
        var sheet=document.styleSheets[1];

        // Generate stylesheet for row height.
        // Not currently in use because native resizing is working.
        /*for (i=0; i<array_rows; i++) {
            selector=".vis-row-"+i;
            rule="{height:" + default_column_width + "px;}";
            if (sheet.insertRule)
                sheet.insertRule(selector+rule, 0);//This puts the rule at index 0
            
            rowStyles[i]=(sheet.cssRules)[0].style; }*/
        
        // Creates classes for vis-columnbox width.
        for (i=0; i<array_columns; i++) {
            selector=".vis-column-"+i;
            rule="{width: " + default_column_width + "px; display: flex; flex-direction: column;}";
            if (sheet.insertRule)
                sheet.insertRule(selector+rule, 0);
            colStyles[i]=(sheet.cssRules)[0].style;
        }
        
        // Debug print
        // console.log(document.styleSheets)
    }
    
    var have_fetched = false;
    function getTableFromBackend() {
        // Simple GET request using fetch
        if (!have_fetched) {
            for (let r = 0; r < 5; r++) {
                for (let c = 0; c < 5; c++) {
                    vis_table_store.set(r, c, "row: " + r + " column: " + c)
                }
            }

            have_fetched = true
            vis_table_store.set(1,2, "yeay|hey|baeee")
        }

        if (!have_fetched) {

            fetch("http://localhost:8000/projects/")
                .then(response => response.json())
                .then(data => {
                    console.log(data)
                    /*data.forEach((element, index) => {
                        vis_table_store.set(0, index, element.project_id)
                    }); */
                    vis_table_store.set(1, 1, data[0].project_id)
                    data[0].node_set.forEach((node, index) => {
                        vis_table_store.set(index+1, 1, node.name)
                    });
                    //vis_table_store.set(0, 1, data) 
            });
            have_fetched = true
        }
    }
    </script>
    
<style>
   @import './style/VisTable.css'
</style>

<template>
    {{ $log("Rerender") }}
    {{ setupTable() }}
    {{ getTableFromBackend() }}
    <div id="vis-table">
        <div v-for="row in vis_table_store.getRowCount()" class="vis-row">
            <div v-if="row-1 !== 0">
                <div class="vis-columnbox vis-resizable-row"> Resizable Row </div>
            </div>
            <div v-if="row-1 === 0"
                class="vis-columnbox"
                style="
                    border: 1px solid black;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                "
            >
                <p 
                    style="
                        margin: 0; 
                        padding: 0; 
                        font-size: 20px; 
                        color: gray;
                        "
                    >
                        FMECA<br>Analys<br>
                        <button @click="restoreColumns()">Restore Table</button>
                    </p>
            </div>
            
            <div v-if="row-1 === 0" v-for="column in vis_table_store.getColumnCount()" 
                class="vis-columnbox vis-resizable-column" 
                :class="getClass(column-1, row-2)"
                v-resize="handleResize"
            >
                Resizable Column
                <button @click="removeColumn(column)">
                    Hide {{ column }}
                </button>
                
                <div class="chrome_is_messy_fix">Loading...</div>
            
            </div>
            
            <div v-if="row-1 !== 0" v-for="column in vis_table_store.getColumnCount()" 
                class="vis-columnbox" 
                :class="getClass(column-1, row-1)"
            >
                <div 
                    class="vis-textarea-container"
                    v-for="item in vis_table_store.get((row), (column))"
                >
                    
                    <textarea class="vis-textarea">{{ item }}</textarea>
                </div>

            </div>
        </div>
    </div>
</template>









