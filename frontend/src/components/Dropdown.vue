<template>
    <div class="menu-item" @click="isOpen = !isOpen">
      <a href="#">
        {{ title }}
      </a>
      <svg viewBox="0 0 1030 638" width="10">
        <path d="M1017 68L541 626q-11 12-26 12t-26-12L13 68Q-3 49 6 24.5T39 0h952q24 0 33 24.5t-7 43.5z" fill="#FFF"></path>
      </svg>
      <transition name="fade" appear>
        <div class="sub-menu" v-if="isOpen">
          <div v-for="(item, i) in items" :key="i" class="menu-item">
            <a :href="item.link" @click="item.filterFunc()">{{ item.title }} </a>           
          </div>
        </div>
      </transition>
    </div>
  </template>
  
  <script>
  export default {
    name: 'dropdown',
    props: {filterFunc : Function},
    props: ['title', 'items'],
    //props: {FilterFunc : Function},
    data () {
      return {
        isOpen: false
      }
    }
  }
  </script>
  
  <style>
  .menu-item svg {
    width: 10px;
    margin-left: 10px;
  }
  
  .menu-item .sub-menu {
    position: absolute;
    background-color: #222;
    top: calc(100% + 3px);
    outline-color: blue;
    left: 50%;
    transform: translateX(-50%);
    width: max-content;
    border-radius: 0px 0px 16px 16px;
  }
  
  .fade-enter-active,
  .fade-leave-active {
    transition: all .5s ease-out;
  }
  
  .fade-enter,
  .fade-leave-to {
    opacity: 0;
  }
  </style>