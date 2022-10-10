import { reactive } from 'vue'

export const vis_table_store = reactive({
    array: [],
    setArray(new_array) {
        console.log("Setting array to")
        console.log(new_array)
        //console.log(this.array)
        //array = e
        this.array = new_array
        console.log(this.array)
    },
    getColumnCount() {
        return this.array.length-1
    },
    getRowCount() {
        if (typeof this.array[0] !== 'undefined') {
            return this.array[0].length
        }
        else {
            return 0
        }
    },
    get(row, column) {
        try {
            return this.array[row-1][column]
        }
        catch (error) {
            console.log("Err: " + error)
        }
    },
    set(row, column, data) {
        this.array[row][column] = data
    }
})
