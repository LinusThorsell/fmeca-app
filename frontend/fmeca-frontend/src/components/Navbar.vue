<template>
    <nav>
      <div class="menu-item"><a href="#">Fortnite hacks</a></div>
      <div class="menu-item"><a href="#">Gripen X(Unreleased)</a></div>
      <Dropdown title="Top 4 företag" :items="services" />
      <div class="menu-item"><a href="#">Adam fan page</a></div>
    </nav>
  </template>
  
  <script>
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
        ]
      }
    }
  }
  </script>
  
  <style>
  nav {
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  nav .menu-item {
    color: #FFF;
    padding: 10px 20px;
    position: relative;
    text-align: center;
    border-bottom: 3px solid transparent;
    display: flex;
    transition: 0.4s;
  }
  
  nav .menu-item.active,
  nav .menu-item:hover {
    background-color: #444;
    border-bottom-color: #FF5858;
  }
  
  nav .menu-item a {
    color: inherit;
    text-decoration: none;
  }
  </style>