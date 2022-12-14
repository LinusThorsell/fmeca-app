<style></style>
<script>
export default {
  name: 'ColumnHead',
  props: {
    column: Number,
    text: String
  },
  methods: {
    removeColumn() {
      this.$emit('removeColumn', this.column)
    }
  }
}
</script>
<template>
  <div>
    {{ column }}: {{ text }} <br>
    <button @click="removeColumn(column)">Hide {{ column }}</button>
    <div class="chrome_is_messy_fix">Loading...</div>
  </div>
</template>
