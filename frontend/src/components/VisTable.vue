<script setup>
  onUpdated(() => {
    fixChrome()
  })
</script>

<script>
import { onUpdated, ref } from "vue";
import ColumnHead from "./ColumnHead.vue";
import RowHead from "./RowHead.vue";
import TableTitle from "./TableTitle.vue";
import ContentColumnBox from "./ContentColumnBox.vue";
import { vis_table_store } from "./vis-table-store.js";
export default {
  mounted() {
    generateCustomStylesheet();
  },
  data() {
    return {
      removeColumn,
      removeAllColumns,
      createFilteredTable,
      restoreColumns,
      getRow,
      getColumn,
      getClass,
      handleResize,
      vis_table_store,
      getProjects,
      selected_project,
      loadProjectFromStore,
      sendCommentsToBackend,
      notes: [{}],
      getColumnTitle,
      getColumnBoxContent,
      isReady,
      hasRendered,
      fixChrome,
    };
  },
  methods: {
    editComment(target, comment) {
      while (this.notes.length <= selected_project.value) {
        this.notes.push({});
      }
      let on = target.parentElement.childNodes[0].innerHTML;
      this.notes[selected_project.value][on] = comment;
      target.value = this.notes[selected_project.value][on];
    },
  },
  components: { ColumnHead, RowHead, TableTitle, ContentColumnBox },
};
var selector,
  rule,
  i,
  rowStyles = [],
  colStyles = [];

export var isReady = ref(false);
var hasRendered = ref(false);

export const array_columns = 7;
export const array_rows = 7;
const default_column_width = 100;
export var selected_project = ref(0);

function getRow(index, table_array) {
  const Row = [];
  for (var column = 0; column < table_array.length; column++) {
    Row[column] = table_array[column][index];
  }

  return Row;
}
// Gets a specific column ( index ) as an array from the input array ( table_array )
function getColumn(index, table_array) {
  return table_array[index];
}

function removeColumn(column) {
  colStyles[column - 1].display = "none";
}

export function removeAllColumns(column) {
  for (
    i = 0;
    i < vis_table_store.getColumnCount(selected_project.value) + 1;
    i++
  ) {
    rowStyles[i].display = "none";
  }
}
export function createFilteredTable(index_x) {
  rowStyles[index_x - 1].display = "flex";
}
export function restoreColumns() {
  console.log(vis_table_store.getColumnCount(selected_project.value));
  for (i = 0; i < vis_table_store.getColumnCount(selected_project.value); i++) {
    colStyles[i].display = "flex";
  }
  for (i = 0; i < vis_table_store.getRowCount(selected_project.value); i++) {
    rowStyles[i].display = "flex";
  }
}

export function getClass(column, row) {
  return "vis-column-" + column + " vis-row-" + row;
}

// Calculates with of a row, to resize table container element to fit all content.
function calculateWidthOfRows() {
  var max_width = 0;
  var rows = document.querySelector(".vis-row");

  if (rows == null) {
    return;
  }

  Array.from(rows.childNodes).forEach((column) => {
    if (column.offsetWidth > 0) {
      max_width += column.offsetWidth;
    }
  });
  document.getElementById("vis-table").style.width = max_width + 200 + "px";
  document.getElementById("nav-bar-id").style.width = max_width - 10 + "px";
}

// Called by vue-resize-observer when a column is resized.
// Changes stylesheet to resize the elements that should change size.
function handleResize({ width }, { __currentTarget__ }) {
  var column_array = __currentTarget__.classList[2];
  var column_id = column_array.slice(column_array.lastIndexOf("-") + 1);

  colStyles[parseInt(column_id)].width = width + "px";
  calculateWidthOfRows();
}

// Generates custom stylesheet.
// Used to effectively resize big amounts of elements fast.
function generateCustomStylesheet() {
  document
    .getElementsByTagName("head")[0]
    .appendChild(document.createElement("style"));

  var sheet = document.styleSheets[1];

  // Generate stylesheet for row height.
  for (i = 0; i < array_rows; i++) {
    selector = ".vis-row-" + i;
    rule = "{min-height: 50px;}";
    if (sheet.insertRule) sheet.insertRule(selector + rule, 0); //This puts the rule at index 0

    rowStyles[i] = sheet.cssRules[0].style;
  }

  // Creates classes for vis-columnbox width.
  for (i = 0; i < array_columns; i++) {
    selector = ".vis-column-" + i;
    rule =
      "{width: " +
      default_column_width +
      "px; display: flex; flex-direction: column;}";
    if (sheet.insertRule) sheet.insertRule(selector + rule, 0);
    colStyles[i] = sheet.cssRules[0].style;
  }
}

function fixChrome() {
    if (document.getElementsByClassName("chrome_is_messy_fix")[0] == null) {
        return;
    }

  /*
            Function to fix bug on most chromium based browsers.
            Required for resizing to work on a majority of browsers
            that do not support native custom stylesheets.
            Firefox will gain a performance advantage for supporting this,
            while for example Google Chrome has to be forced to reload the
            styles by nudging the elements downwards slightly.
        */
  // Get all the 'Loading...' text elements, and nudge the rest down slightly.
  document.getElementsByClassName("chrome_is_messy_fix")[0].style.height =
    "100px";
  // Wait until the stylesheet is triggered to reload, then hide elements.
  setTimeout(() => {
    Array.from(document.getElementsByClassName("chrome_is_messy_fix")).forEach(
      (div) => {
        div.style.display = "none";
      }
    );
  }, 500);
}

export function onFetched() {
  // Loop through vis_table_store array
  let columns_to_make_bigger = [];
  let rows_to_make_bigger = [];
  let temp_array = vis_table_store.getArray(selected_project.value);

  for (let column = 0; column < temp_array.length; column++) {
    colStyles[column].minWidth = "150px";
    for (let row = 0; row < temp_array[column].length; row++) {
      rowStyles[row].minHeight = "50px";
      // If the element is a partition, parse it into a string.
      if (temp_array[column][row].toString().split("|").length > 1) {
        let temp_array_split = temp_array[column][row].toString().split("|");

        if (temp_array_split.toString().split("\n").length > 1) {
          let highest_split_count = 0;
          temp_array_split.forEach((element, index) => {
            let split_count = element.split("\n").length;
            if (split_count > highest_split_count) {
              highest_split_count = split_count;
            }
          });

          rows_to_make_bigger.push({
            row: column - 1,
            size: temp_array_split.length * (highest_split_count - 1),
          });
        } else {
          rows_to_make_bigger.push({
            row: column - 1,
            size: temp_array[column][row].toString().split("|").length,
          });
        }

        temp_array[column][row]
          .toString()
          .split("|")
          .forEach((name, index) => {
            if (name.length > 10) {
              columns_to_make_bigger.push(row - 1);
            }
          });
      } else {
        if (temp_array[column][row].toString().length > 10) {
          columns_to_make_bigger.push(column);
        }
      }
    }
    isReady.value = true;
  }

  // remove duplicate elements from columns_to_make_bigger array
  columns_to_make_bigger = [...new Set(columns_to_make_bigger)];

  columns_to_make_bigger.forEach((column) => {
    if (column != 0) {
      colStyles[column].minWidth = "200px";
    }
    calculateWidthOfRows();
  });
  calculateWidthOfRows();

  // only keep largest size
  rows_to_make_bigger = rows_to_make_bigger.filter(
    (row, index, self) =>
      index ===
      self.findIndex(
        (t) => t.row === row.row && t.size === Math.max(t.size, row.size)
      )
  );

  rows_to_make_bigger.forEach((row) => {
    let style = (row.size * 50).toString() + "px";
    rowStyles[row.row].minHeight = style;
  });
}

export function getProjects() {
  let projects = [];
  projects = vis_table_store.getProjectNames();
  return projects;
}
export function loadProjectFromStore() {
  let selection = document.getElementById("project-select").value;
  selected_project.value = vis_table_store.switchProject(selection);
  onFetched();
}

function getXYFromClassName(element) {
  let x = element[1];
  let y = element[2];

  x = x.slice(x.lastIndexOf("-") + 1);
  y = y.slice(y.lastIndexOf("-") + 1);

  x = parseInt(x) + 1;
  y = parseInt(y) + 2;

  return [x, y];
}

function sendCommentsToBackend() {
  let projects = vis_table_store.getProjectNames();
  let comments = this.notes;

  let data = {
    project: projects[selected_project.value],
    comments: comments[selected_project.value],
  };

  fetch("http://localhost:8000/comments/", {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
}

let columnTitles = ["Padding", "Node", "CPU", "Partitions"];
function getColumnTitle(column) {
  if (column < columnTitles.length) {
    return columnTitles[column];
  } else {
    return "Column";
  }
}

function getColumnBoxContent(row, column) {
  return vis_table_store.get(selected_project.value, row, column);
}
</script>

<template>
  {{ $log("Rerender") }}
  {{ vis_table_store.getTableFromBackend() }}

  <div v-if="!isReady">
    <h1>Loading...</h1>
  </div>
  <div v-if="isReady">
    <!-- Container for table -->
    <div id="vis-table">
      <!-- Main table Content -->
      <!-- Loops row by row. -->
      <div
        v-for="row in vis_table_store.getRowCount(selected_project)"
        class="vis-row"
      >
        <!-- Only gets drawn on row 0, column 0 in the table -->
        <TableTitle @restoreColumns="restoreColumns" :row="row" />

        <!-- Gets drawn on the rest of column 0 -->
        <RowHead :row="row" />

        <!-- Gets drawn on entire row 0 -->
        <div
          v-if="row - 1 === 0"
          v-for="column in vis_table_store.getColumnCount(selected_project)"
          class="vis-columnbox vis-resizable-column"
          :class="getClass(column - 1, row - 2)"
          v-resize="handleResize"
        >
          <ColumnHead
            @removeColumn="removeColumn"
            :column="column"
            :text="getColumnTitle(column)"
          />
        </div>

        <!-- Main content boxes, drawn on everything that is not row 0 or column 0 -->
        <ContentColumnBox
          :row="row"
          :column="column"
          :store="vis_table_store"
          :selected_project="selected_project"
          @editComment="editComment"
        />
      </div>
    </div>
    {{ fixChrome() }}
  </div>
</template>
<style>
@import "./style/VisTable.css";
</style>
