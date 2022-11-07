import { reactive } from 'vue'

export const vis_table_store = reactive({
    array: [[]],
    setArray(num, new_array) {
        console.log("Setting array to")
        console.log(new_array)
        //console.log(this.array)
        //array = e
        this.array[num] = new_array
        console.log(this.array[num])
    },
    getColumnCount(num) {
        return this.array[num].length-1
    },
    getRowCount(num) {
        if (typeof this.array[num] == 'undefined') {
            return 0
        }

        if (typeof this.array[num][0] !== 'undefined') {
            return this.array[num][0].length
        }
        else {
            return 0
        }
    },
    get(num, row, column) {
        try {
            if (this.array[num][row-1][column].includes("|")) {
                let temp = this.array[num][row-1][column].split("|")
                return temp
            }
            else {
                return [this.array[num][row-1][column]]
            }

        }
        catch (error) {
            console.log("Err: " + error)
        }
    },
    set(num, row, column, data) {
        this.array[num][row][column] = data
    }
})
