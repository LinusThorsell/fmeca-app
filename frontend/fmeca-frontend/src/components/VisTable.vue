<script>
import { ref, watchEffect } from 'vue'
import { vis_table_store } from './vis-table-store.js'
import html2pdf from 'html2pdf.js';

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
            }, 10000);
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
                getProjects,
                selected_project,

                loadProjectFromStore,
            }
        },

        /*components: {
        },*/
        methods: {
            generatePdf() {
                //html2pdf(document.getElementById('vis-table'));
                //console.log(document.getElementById('vis-table').innerHTML)
                print()
            }
        },
    }

    var selector, rule, i, /*rowStyles=[],*/ colStyles=[];

    const array_columns = 6;
    const array_rows = 6;
    const default_column_width = 100;

    var selected_project = ref(0);

/*
    watchEffect(() => {
    // tracks A0 and A1
        A2.value = A0.value + A1.value
    })*/

    // Gets entire table ( TODO : interface with backend here )
    function setupTable() {    
/*
        if (vis_table_store.getRowCount(selected_project) === 0) {
            const temp_array = []
            console.log("Array empty, creating example")
            for (var column = 0; column < array_columns+1; column++) {
                temp_array[column] = [];
                for (var row = 0; row < array_rows+1; row++) {
                    temp_array[column][row] = "";
                }
            }
            vis_table_store.setArray(selected_project, temp_array)
        }*/
        // return table_array;
        
        //vis_table_store.generateEmpty()
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
        console.log(vis_table_store.getColumnCount(selected_project.value))
        for(i = 0; i < vis_table_store.getColumnCount(selected_project.value); i++)
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
        //console.log(column_id)
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

    function stringifyPartitions(obj) {
        console.log("To stringify into partitions")
        console.log(obj)

        let build_partition_string = ""
        obj.forEach(partitions => {
            build_partition_string += partitions.name + "\n"
        });
        console.log("returning: " + build_partition_string)
        return build_partition_string;
    }
    
    var have_fetched = false;
    var debug = false;
    function getTableFromBackend() {
        // Simple GET request using fetch
        if (!have_fetched && debug) {
            for (let r = 0; r < 5; r++) {
                for (let c = 0; c < 5; c++) {
                    vis_table_store.set(selected_project, r, c, "row: " + r + " column: " + c)
                }
            }

            have_fetched = true
            vis_table_store.set(selected_project, 1,2, "yeay|hey|baeee")
        }

        if (!have_fetched && !debug) {

            fetch("http://localhost:8000/projects/")
                .then(response => response.json())
                .then(data => {
                    console.log(data)
                    /*data.forEach((element, index) => {
                        vis_table_store.set(0, index, element.project_id)
                    }); */
                    data.forEach((project, index) => {
                        console.log(index)
                        console.log(project.name)
                        vis_table_store.generateEmpty(index, array_rows, array_columns)
                        vis_table_store.set(index, 0, 0, project)
                        //vis_table_store.set(index, 1, 1, project.name)
                        
                        project.node_set.forEach((node, n_index) => {
                            vis_table_store.set(index, n_index+1, 1, node.name);

                            let cpu_string = "";
                            let cpu_partition_string = "";

                            node.cpu_set.forEach(cpu => {
                                cpu_string += cpu.name + "|"
                                
                                cpu_partition_string += stringifyPartitions(cpu.partition_set) + "|"
                            })
                            cpu_string = cpu_string.slice(0, -1);
                            cpu_partition_string = cpu_partition_string.slice(0, -1)
                            
                            vis_table_store.set(index, n_index+1, 2, cpu_string)
                            vis_table_store.set(index, n_index+1, 3, cpu_partition_string)

                        })

                        /*project.node_set.forEach((node, index) => {
                            vis_table_store.set(index, index+1, 1, project.name)
                        });*/
                    });
                    //vis_table_store.set(0, 1, data) 
            });

            have_fetched = true
        }
    }
    function getProjects() {
        let projects = []

        projects = vis_table_store.getProjectNames()

        return projects;
    }

    function loadProjectFromStore()
    {
        let selection = document.getElementById("project-select").value;
        selected_project.value = vis_table_store.switchProject(selection);
    }

    </script>
 
<style>
   @import './style/VisTable.css'
</style>

<template>
    {{ $log("Rerender") }}
    {{ setupTable() }}
    {{ getTableFromBackend() }}
    
    <button @click="generatePdf">Generate PDF</button>
    <br> 
    <label for="project-select">Choose a project:</label>
    <select name="projects" id="project-select">
        <option value="">Please choose a project</option>
        <option v-for="project in getProjects()" :value="project">{{project}}</option>
        <!--option value="proj1">Project 1</option>
        <option value="proj2">Project 2</option-->
    </select>
    <button @click="loadProjectFromStore()">Load Selected Project</button>

    <div id="vis-table">
        <div v-for="row in vis_table_store.getRowCount(selected_project)" class="vis-row">
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
            
            <div v-if="row-1 === 0" v-for="column in vis_table_store.getColumnCount(selected_project)" 
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
            
            <div v-if="row-1 !== 0" v-for="column in vis_table_store.getColumnCount(selected_project)" 
                class="vis-columnbox" 
                :class="getClass(column-1, row-1)"
            >
                <div 
                    class="vis-textarea-container"
                    v-for="item in vis_table_store.get(selected_project, (row), (column))"
                >
                    
                    <textarea class="vis-textarea">{{ item }}</textarea>
                </div>

            </div>
        </div>
    </div>
</template>









