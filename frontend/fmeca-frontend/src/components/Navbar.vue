<template>
  <nav id="nav-bar-id" class="nav-background">
    <button @click="generatePdf">Generate PDF</button>
    <br> 
    <!-- <label for="project-select">Choose a project:</label> -->
    <select name="projects" id="project-select">
        <option value="">Please choose a project</option>
        <option v-for="project in getProjects()" :value="project">{{project}}</option>
        <!--option value="proj1">Project 1</option>
        <option value="proj2">Project 2</option-->
    </select>
    <button @click="loadProjectFromStore()">Load Selected Project</button>
    <!-- TODO TOG BORT <div class="menu-item"><a href="#">fortnite</a></div> -->
    <!-- TODO TOG BORT <div class="menu-item"><a href="#">Gripen X(Unreleased)</a></div> -->
    <!-- TODO TOG BORT <Dropdown title="Change view" :items="services" /> -->
    <!-- <label for="project-select">Choose a project</label> -->
    <!-- <select name ="projects" id="project-select"> -->
      <!-- <option value =""> Please choose a project</option> -->
      <!-- <option v-for="project in getProjects()" value ="project">{{project}}</option> -->
    <!-- </select> -->
    <!-- TODO TOG BORT <div class="menu-item"><a href="#">Adam fan page</a></div>-->
    <!-- sökbar som aktiveras genom enter -->
    <input type="text" @keydown.enter="filteredList(input)" v-model="input" placeholder="Filter..." />

  </nav>
</template>

<script>
//Searchbarfunction
import {getProjects, loadProjectFromStore} from './VisTable.vue'

function filteredList(input) 
{  
//Input är det som skrivs in
// filterSearch(input);
console.log(input);
//localStorage.setItem("columnfilter", input);

}


import Dropdown from './Dropdown.vue';

export default {
  name: 'navbar',
  components: {
    Dropdown,
    
  },
  data () {
    return {
      getProjects,
      loadProjectFromStore,
      /*services: [
        {
          title: 'S',
          link: '#fortnite',
          filterFunc: function name() {
              console.log("hey");
          }
        },
        {
          title: 'A',
          link:'#',
          filterFunc: function name() {
              console.log("din");
          }
        },
        {
          title: 'A',
          link: '#',
          filterFunc: function name() {
              console.log("kuk");
          }
        },
        {
          title: 'B',
          link: '#',
          filterFunc: function name() {
              console.log("nörd");
          }
        }
      ]*/
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
