<style></style>
<script>
export default {
  name: "TableTitle",
  props: {
    row: Number,
  },
  methods: {
    restoreColumns() {
      this.$emit("restoreColumns");
    },
  },
};
</script>
<template>
  <div
    v-if="row - 1 === 0"
    class="vis-columnbox"
    style="
      border: 1px solid black;
      display: flex;
      justify-content: center;
      align-items: center;
    "
  >
    <p style="margin: 0; padding: 0; font-size: 20px; color: gray">
      FMECA<br />Analys<br />
      <button @click="restoreColumns()">Restore Table</button>
    </p>
  </div>
</template>
