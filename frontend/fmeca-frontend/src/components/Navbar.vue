<template>
    <nav class="nav-background">
      <div class="menu-item"><a href="#">Fortnite hacks</a></div>
      <div class="menu-item"><a href="#">Gripen X(Unreleased)</a></div>
      <Dropdown title="Top 4 företag" :items="services" />
      <div class="menu-item"><a href="#">Adam fan page</a></div>
      <!-- sökbar som aktiveras genom enter -->
      <input type="text" @keydown.enter="filteredList(input)" v-model="input" placeholder="Filter..." />

    </nav>
  </template>
  
  <script>
  //Searchbarfunction
  import {filterColumn, filterSearch} from './VisTable.vue'

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
        ],
        input: '',
        filteredList
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
  background: white url("assets/search-icon.svg") no-repeat 15px center;
  background-size: 15px 15px;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  box-shadow: rgba(50, 50, 93, 0.25) 0px 2px 5px -1px,
    rgba(0, 0, 0, 0.3) 0px 1px 3px -1px;
}

.item {
  width: 350px;
  margin: 0 auto 10px auto;
  padding: 10px 20px;
  color: white;
  border-radius: 5px;
  box-shadow: rgba(0, 0, 0, 0.1) 0px 1px 3px 0px,
    rgba(0, 0, 0, 0.06) 0px 1px 2px 0px;
}

.fruit {
  background-color: rgb(97, 62, 252);
  cursor: pointer;
}

.error {
  background-color: tomato;
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