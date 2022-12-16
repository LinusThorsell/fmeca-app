<template>
  <nav id="nav-bar-id" class="nav-background">
    <button @click="generatePdf">Generate PDF</button>
    <br> 
    <select name="projects" id="project-select">
        <option value="">Please choose a project</option>
        <option v-for="project in getProjects()" :value="project">{{project}}</option>
    </select>
    <button @click="loadProjectFromStore()">Load Selected Project</button>
    <!-- Searchbar with filtering -->
    <input type="text" @keydown.enter="filteredList(input)" v-model="input" placeholder="Filter..." />

  </nav>
</template>

<script>

function generatePdf() 
{
print()
}

import {getProjects, loadProjectFromStore, selected_project, removeAllColumns, createFilteredTable, restoreColumns} from './VisTable.vue'
import {vis_table_store} from './vis-table-store.js'
//Searching and filtering
function filteredList(input) 
{  
//Removes the table
removeAllColumns();
//Creates an array that iterates through data from backend
let temp_array = vis_table_store.getArray(selected_project.value)
temp_array.forEach((array_outer, index_x) => {
  array_outer.forEach((array_inner, index_y) => {
    //Compares the input and data from backend, makes it string and lower case
    let stringinput = input +"";
    let stringinner = array_inner + "";
    stringinput = stringinput.toLowerCase();
    stringinner = stringinner.toLowerCase();
  
    
    // createFilteredTable(index_x);
    //Prints out the new filtered table
     if(stringinner.includes(stringinput,0) && stringinput!= "")
        {
            createFilteredTable(index_x);       
        }
        //Shows the whole table if nothing is written
      else if(stringinput == "")
        {
         restoreColumns();
        }
     });
  });
}


import Dropdown from './Dropdown.vue';


export default {
  name: 'navbar',
  components: {
    Dropdown,
    
  },
  data () {
    return {
      vis_table_store,
      selected_project,
      removeAllColumns,
      createFilteredTable,
      filteredList,
      generatePdf,
      getProjects,
      loadProjectFromStore,
      restoreColumns,
      
    }
  },
  
}
</script>

<style>
.nav-background {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color:#444;
  padding: 5px;
  height: 75px;
}

.menu-item {
  color: #FFF;
  background-color: #443;
  padding: 10px 20px;
  position: relative;
  text-align: center;
  border-bottom: 3px solid transparent;
  display: flex;
  transition: 0.4s;
}

.menu-item.active,
.menu-item:hover {
  background-color: #444;
  border-bottom-color: #FF5858;
}

.menu-item a {
  color: inherit;
  text-decoration: none;
}
</style>
