<style></style>
<script>
import { getClass } from "./VisTable.vue";

export default {
  name: "ContentColumnBox",
  emits: ["editComment"],
  props: {
    column: Number,
    row: Number,
    store: null,
    selected_project: Number,
  },
  methods: {
    editComment(target, value) {
      this.$emit("editComment", target, value);
    },
  },
  data() {
    return {
      getClass,
    };
  },
};
</script>
<template>
  <div
    v-if="row - 1 !== 0"
    v-for="column in store.getColumnCount(selected_project)"
    class="vis-columnbox"
    :class="getClass(column - 1, row - 2)"
  >
    <div
      class="vis-textarea-container"
      v-for="item in store.get(selected_project, row, column)"
    >
      <textarea
        class="vis-textarea"
        onfocus="this.parentElement.children[1].className = 'vis-comment vis-textarea vis-textarea-comment'; 
                        this.className = 'vis-textarea'"
        >{{ item }}</textarea
      >
      <textarea
        class="vis-comment vis-textarea vis-textarea-comment"
        onfocus="this.parentElement.children[0].className = 'vis-textarea vis-textarea-comment'; 
                        this.className = 'vis-textarea'"
        @input="editComment($event.target, $event.target.value)"
      ></textarea>
    </div>
  </div>
</template>
