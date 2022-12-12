<style></style>
<script>
function getRowClass(row) {
  return "vis-row-" + row;
}

export default {
  name: "RowHead",
  props: {
    row: Number,
  },
  data() {
    return {
      getRowClass,
    };
  },
};
</script>
<template>
  <div v-if="row - 1 !== 0">
    <div class="vis-columnbox vis-resizable-row" :class="getRowClass(row - 2)">
      Row: {{ row - 1 }}
    </div>
  </div>
</template>
