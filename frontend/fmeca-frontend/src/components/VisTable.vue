<script>
import { ref } from "vue";
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
      //setupTable,
      getRow,
      getColumn,
      addRow,
      addColumn,
      getClass,
      getRowClass,
      handleResize,
      getTableFromBackend,
      vis_table_store,
      getProjects,
      selected_project,
      loadProjectFromStore,
      sendCommentsToBackend,

      notes: [{}],
    };
  },
  /*components: {
        },*/
  methods: {
    editComment(target, comment) {
      while (this.notes.length <= selected_project.value) {
        this.notes.push({});
      }

      console.log("edit comment");
      console.log(target);

      let on = target.parentElement.childNodes[0].innerHTML;
      //let on = getParentClassName(target)
      console.log(on);
      console.log(comment);
      this.notes[selected_project.value][on] = comment;

      target.value = this.notes[selected_project.value][on];
    },
  },
};
var selector,
  rule,
  i,
  rowStyles = [],
  colStyles = [];

const array_columns = 6;
const array_rows = 6;
const default_column_width = 100;
export var selected_project = ref(0);

// Gets entire table ( TODO : interface with backend here )

// Gets a specific row ( index ) as an array from the input array ( table_array ).

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
  console.log(column);
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
export function createFilteredTable(input, array_inner, index, index_x) {
  console.log(input);
  console.log(array_inner);

  if (input.indexOf(index_x - 1) != -1 && array_inner != "") {
    console.log(array_inner);
    console.log("träff");
    rowStyles[index_x - 1].display = "flex";
  }
}
function restoreColumns() {
  console.log(vis_table_store.getColumnCount(selected_project.value));
  for (i = 0; i < vis_table_store.getColumnCount(selected_project.value); i++) {
    colStyles[i].display = "flex";
  }
}

function getClass(column, row) {
  return "vis-column-" + column + " vis-row-" + row;
}

function getRowClass(row) {
  return "vis-row-" + row;
}

// Calculates with of a row, to resize table container element to fit all content.
function calculateWidthOfRows() {
  var max_width = 0;
  var rows = document.querySelector(".vis-row");
  Array.from(rows.childNodes).forEach((column) => {
    if (column.offsetWidth > 0) {
      max_width += column.offsetWidth;
    }
  });
  document.getElementById("vis-table").style.width = max_width + 200 + "px";
  document.getElementById("nav-bar-id").style.width = max_width - 10 + "px";
}

// Called by vue-resize-observer when a column is resized.
// Changes stylesheet to resize elements
function handleResize({ width }, { __currentTarget__ }) {
  var column_array = __currentTarget__.classList[2];
  var column_id = column_array.slice(column_array.lastIndexOf("-") + 1);

  colStyles[parseInt(column_id)].width = width + "px";
  calculateWidthOfRows();
}

// Generates custom stylesheet.
// Used to effectively resize big amounts of elements fast.
function generateCustomStylesheet() {
  console.log("Generating stylesheet");
  document
    .getElementsByTagName("head")[0]
    .appendChild(document.createElement("style"));
  var sheet = document.styleSheets[1];
  // Generate stylesheet for row height.
  // Not currently in use because native resizing is working.
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
function stringifyPartitions(obj) {
  console.log("To stringify into partitions");
  console.log(obj);
  let build_partition_string = "";
  obj.forEach((partitions) => {
    build_partition_string += partitions.name + "\n";
  });
  console.log("returning: " + build_partition_string);
  return build_partition_string;
}

function onFetched() {
  console.log("Fetched data...");

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

  // Loop through vis_table_store array
  let columns_to_make_bigger = [];
  let rows_to_make_bigger = [];
  let temp_array = vis_table_store.getArray(selected_project.value);
  console.log(temp_array);
  for (let column = 0; column < temp_array.length; column++) {
    colStyles[column].minWidth = "150px";
    for (let row = 0; row < temp_array[column].length; row++) {
      rowStyles[row].minHeight = "50px";
      // If the element is a partition, parse it into a string.
      if (temp_array[column][row].toString().split("|").length > 1) {
        rows_to_make_bigger.push({
          row: column - 1,
          size: temp_array[column][row].toString().split("|").length,
        });
        temp_array[column][row]
          .toString()
          .split("|")
          .forEach((name, index) => {
            if (name.length > 10) {
              console.log(
                name,
                "larger than 10, ",
                name.length,
                "column: ",
                column,
                "row: ",
                row
              );
              columns_to_make_bigger.push(row - 1);
            }
          });
      } else {
        if (temp_array[column][row].toString().length > 10) {
          console.log(
            temp_array[column][row].toString(),
            "larger than 10, ",
            temp_array[column][row].toString().length,
            "column: ",
            column,
            "row: ",
            row
          );
          console.log(temp_array[column][row]);
          columns_to_make_bigger.push(column);
        }
      }
    }
  }
  console.log("columns to make bigger: ", columns_to_make_bigger);

  // remove duplicate elements from columns_to_make_bigger array
  columns_to_make_bigger = [...new Set(columns_to_make_bigger)];

  columns_to_make_bigger.forEach((column) => {
    //console.log("column: ", column)
    if (column != 0) {
      colStyles[column].minWidth = "200px";
    }
    calculateWidthOfRows();
  });
  calculateWidthOfRows();

  // remove all duplicate row from rows_to_make_bigger array and keep the one with largest size
  rows_to_make_bigger = rows_to_make_bigger.filter(
    (thing, index, self) => index === self.findIndex((t) => t.row === thing.row)
  );
  console.log("rows to make bigger: ", rows_to_make_bigger);
  rows_to_make_bigger.forEach((row) => {
    let style = (row.size * 50).toString() + "px";
    rowStyles[row.row].minHeight = style;
  });
}

var have_fetched = false;
var debug = false;
function getTableFromBackend() {
  // Simple GET request using fetch
  if (!have_fetched && debug) {
    for (let r = 0; r < 5; r++) {
      for (let c = 0; c < 5; c++) {
        vis_table_store.set(
          selected_project,
          r,
          c,
          "row: " + r + " column: " + c
        );
      }
    }
    have_fetched = true;
    vis_table_store.set(selected_project, 1, 2, "yeay|hey|baeee");
  }
  if (!have_fetched && !debug) {
    fetch("http://localhost:8000/projects/")
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        data.forEach((project, index) => {
          console.log(index);
          console.log(project.name);
          vis_table_store.generateEmpty(index, array_rows, array_columns);
          vis_table_store.set(index, 0, 0, project);

          project.node_set.forEach((node, n_index) => {
            vis_table_store.set(index, n_index + 1, 1, node.name);
            let cpu_string = "";
            let cpu_partition_string = "";
            node.cpu_set.forEach((cpu) => {
              cpu_string += cpu.name + "|";

              cpu_partition_string +=
                stringifyPartitions(cpu.partition_set) + "|";
            });
            cpu_string = cpu_string.slice(0, -1);
            cpu_partition_string = cpu_partition_string.slice(0, -1);
            console.log(cpu_string);
            console.log(cpu_partition_string);

            vis_table_store.set(index, n_index + 1, 2, cpu_string);
            vis_table_store.set(index, n_index + 1, 3, cpu_partition_string);
          });
        });
      })
      .then(() => {
        onFetched();
      });
    have_fetched = true;
  }
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
function getParentClassName(element) {
  console.log(element);
  console.log(element.parentElement);
  console.log(element.parentElement.parentElement);

  let vector2d_x_y_position = getXYFromClassName(
    element.parentElement.parentElement.classList
  );
  console.log(vector2d_x_y_position);
  console.log("get location in array");
  let className = vis_table_store.get(
    selected_project.value,
    vector2d_x_y_position[1],
    vector2d_x_y_position[0]
  );
  console.log(className);

  return className;
}

function sendCommentsToBackend() {
  console.log("Sending comments to backend");

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

  console.log(JSON.stringify(data));
}
</script>

<template>
  {{ $log("Rerender") }}
  <!--{{ setupTable() }} -->
  {{ getTableFromBackend() }}

  <div id="vis-table">
    <div
      v-for="row in vis_table_store.getRowCount(selected_project)"
      class="vis-row"
    >
      <div v-if="row - 1 !== 0">
        <div
          class="vis-columnbox vis-resizable-row"
          :class="getRowClass(row - 2)"
        >
          Resizable Row
        </div>
      </div>
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

      <div
        v-if="row - 1 === 0"
        v-for="column in vis_table_store.getColumnCount(selected_project)"
        class="vis-columnbox vis-resizable-column"
        :class="getClass(column - 1, row - 2)"
        v-resize="handleResize"
      >
        Resizable Column
        <button @click="removeColumn(column)">Hide {{ column }}</button>

        <div class="chrome_is_messy_fix">Loading...</div>
      </div>

      <div
        v-if="row - 1 !== 0"
        v-for="column in vis_table_store.getColumnCount(selected_project)"
        class="vis-columnbox"
        :class="getClass(column - 1, row - 2)"
      >
        <div
          class="vis-textarea-container"
          v-for="item in vis_table_store.get(selected_project, row, column)"
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
    </div>
  </div>
</template>
<style>
@import "./style/VisTable.css";
</style>
