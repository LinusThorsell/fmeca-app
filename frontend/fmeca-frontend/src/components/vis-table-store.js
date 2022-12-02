import { reactive } from "vue";

export const vis_table_store = reactive({
  array: [[]],
  setArray(num, new_array) {
    console.log("Setting array to");
    console.log(new_array);
    this.array[num] = new_array;
    console.log(this.array[num]);
  },
  getColumnCount(num) {
    return this.array[num][0].length - 1;
  },
  getRowCount(num) {
    if (typeof this.array[num] == "undefined") {
      return 0;
    }

    if (typeof this.array[num][0] !== "undefined") {
      return this.array[num][0].length;
    } else {
      return 0;
    }
  },
  get(num, row, column) {
    try {
      if (this.array[num][row - 1][column].includes("|")) {
        let temp = this.array[num][row - 1][column].split("|");

        let highest_split_count = 0;
        temp.forEach((element, index) => {
          let split_count = element.split("\n").length;
          if (split_count > highest_split_count) {
            highest_split_count = split_count;
          }
        });

        let temp_temp = [];
        let multisplit = false;
        let split_count = 0;
        temp.forEach((element, index) => {
          if (element.includes("\n")) {
            split_count = element.split("\n").length;
            element.split("\n").forEach((element2, index2) => {
              if (element2.length > 0) {
                temp_temp.push(element2);
                multisplit = true;
              }
            });
            // Fill to match the maximum split count.
            for (let i = split_count; i < highest_split_count; i++) {
              temp_temp.push("");
            }
          }
          // this is an empty row, should scale to match the amount of splits
          else {
            for (let i = 0; i < highest_split_count - 1; i++) {
              temp_temp.push("");
            }
          }
        });

        if (multisplit) {
          temp = temp_temp;
        }
        return temp;
      } else {
        return [this.array[num][row - 1][column]];
      }
    } catch (error) {
      console.log("Err: " + error);
    }
  },
  getArray(num) {
    return this.array[num].slice(0);
  },
  set(num, row, column, data) {
    this.array[num][row][column] = data;
  },
  setComment(num, row, column, comment) {
    console.log("Setting comment");
    console.log(num + " " + row + " " + column + " " + comment);
    console.log(this.array[num][row][column]);
    console.log(comment);
  },
  getComment(num, row, column) {
    return this.array[num][row][column].comment;
  },
  getProjectNames() {
    if (typeof this.array[0][0] == "undefined") {
      return ["loading", "projects"];
    }

    var projectNames = [];
    this.array.forEach((project) => {
      projectNames.push(project[0][0].name);
      //console.log(project[0][0].name)
    });
    console.log(projectNames);
    return projectNames;
  },
  generateEmpty(num, rows, cols) {
    if (this.getRowCount(num) === 0) {
      const temp_array = [];
      console.log(
        "Generating empty array: " + num + " Array empty, creating example"
      );
      for (var col = 0; col < cols; col++) {
        temp_array[col] = [];
        for (var row = 0; row < rows; row++) {
          temp_array[col][row] = "";
        }
      }
      this.setArray(num, temp_array);
    }

    console.log("Generated empty table for: " + num);
  },
  switchProject(selected_project) {
    let index_of_project = null;
    this.array.forEach((project, index) => {
      if (selected_project === project[0][0].name) {
        index_of_project = index;
      }
    });
    return index_of_project;
  },
});
