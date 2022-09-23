<template>
<div id="vueapp">

    <div class="dropdown">
      <button class="dropdown-toggle" v-on:click="isShowDrop1 = !isShowDrop1">
        Dropdown
      </button>
      <ul class="dropdown-menu" v-show="isShowDrop1">
        <li><a>Item 1</a></li>
        <li><a>Item 2</a></li>
        <li><a>Item 3</a></li>
      </ui>
    </div>
    
    </div>
    
    <script src="https://unpkg.com/vue@2.3.3/dist/vue.js"></script>
</template>

<style>
    .dropdown {
  position: relative;
}

.dropdown-toggle {
  background-color: white;
}

.dropdown-menu {
  position: absolute;
  border-radius: 5px;
  border-top-color: #C9D7F1;
  border-right-color: #36C;
  border-bottom-color: #36C;
  border-left-color: #A2BAE7;
  border-style: solid;
  border-width: 1px;
  z-index: 22;
  padding: 0;
  background-color: white;
  overflow: hidden;
  font-size: small;
  font-family: Arial;
  line-height: 2em;
  word-spacing: 0;
  margin-top: 2px;
}

.dropdown-menu a {
  font-size: 1.25em;
  color: #00C;
  padding: .25em 2em .25em 1em;
  text-decoration: none;
  background: white;
  display: block;
  cursor: pointer;
}

.dropdown-menu a:hover {
  background: #00C;
  color: white;
}
</style>