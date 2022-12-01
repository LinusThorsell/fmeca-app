<script>
import {ref} from "vue";

export default {
  data() {
    return {
      jsonData: 'yeetus',
    };
  },
};


export function renderJSONTree(in_data) {
console.log(in_data);
    this.jsonData = 'knowngoodvalue';
}

</script>

<template>
  <main>
    <br />
    <br />

    <p>RAW JSON Tree Viewer</p>

    <p>{{this.jsonData}}</p>

    <json-viewer
    :key="jsonData"
      :value="jsonData"
      :expand-depth="5"
      copyable
      boxed
      sort
    ></json-viewer>

  </main>
</template>
