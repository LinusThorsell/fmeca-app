<template>
    <nav class="nav-background">
      <div class="menu-item"><a href="#">fortnite</a></div>
      <div class="menu-item"><a href="#">Gripen X(Unreleased)</a></div>
      <Dropdown title="Change view" :items="services" />
      <label for="project-select">Choose a project</label>
      <select name ="projects" id="project-select">
        <option value =""> Please choose a project</option>
        <!-- <option v-for="project in getProjects()" value ="project">{{project}}</option> -->
      </select>
      <div class="menu-item"><a href="#">Adam fan page</a></div>
      <!-- sökbar som aktiveras genom enter -->
      <input type="text" @keydown.enter="filteredList(input)" v-model="input" placeholder="Filter..." />

    </nav>
  </template>
  
  <script>
  //Searchbarfunction
  import {filterColumn, filterSearch /*,getProjects*/} from './VisTable.vue'

  function filteredList(input) 
{  
  //Input är det som skrivs in
  filterSearch(input);
  console.log(input);
  //localStorage.setItem("columnfilter", input);

}
  //Dropdown code
  import Dropdown from './Dropdown.vue';
  
  export default {
    name: 'navbar',
    components: {
      Dropdown   
    },
    data () {
      return {
        services: [
          {
            title: 'Sweden',
            link: '#Sweden',
            filterFunc: function name() {
              for(project in getProjects())
                console.log("hey");
            }
          },
          {
            title: 'Brazil',
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
        ],
        input: '',
        filteredList,
        //getProjects
      }
    }
  }
  
  </script>
  
  <style>

input {
  display: block;
  width: 350px;
  margin: 20px auto;
  padding: 10px 45px;
  
  background-size: 15px 15px;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  box-shadow: rgba(50, 50, 93, 0.25) 0px 2px 5px -1px,
    rgba(0, 0, 0, 0.3) 0px 1px 3px -1px;
}

  .nav-background {
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: black;
    height: 75px;
  }
  
  .menu-item {
    color: #FFF;
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