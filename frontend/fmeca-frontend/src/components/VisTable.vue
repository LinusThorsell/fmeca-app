<script>
export default {
    data() {
        return {
            getTable,
            getColumns
        }
    }
}

function getTable() {
    const array_columns = 50;
    const array_rows = 10;

    const table_array = [];

    for (var column = 0; column < array_columns; column++) {
        table_array[column] = [];
        for (var row = 0; row < array_rows; row++) {
            table_array[column][row] = "Column: " + column + " Row: " + row;
        }
    }

    console.log("Full array")
    console.log(table_array);

    return table_array;
}

function getColumns(table_array) {
    const Columns = [];
    for (var column = 0; column < table_array.length; column++) {
        Columns[column] = table_array[column][0];
    }

    console.log("Columns of array")
    console.log(Columns)

    return Columns;
}

</script>

<style>
    table {
        font-family: Arial, Helvetica, sans-serif;
        border-collapse: collapse;
    }

    td, th {
        border: 1px solid #000;
        text-align: left;
        padding: 0.2em;

        font-size: 1em;

        /* not working */
        width: 20em;
    }
    tr:nth-child(even) {
        background-color: #dddddd;
    }

</style>
    
<template>
    <table>
        <tr>
            <th v-for="column in getColumns(getTable())">
                {{ column }}
            </th>
        </tr>
        <tr v-for="rows in getTable()[0].length-1">
            <td v-for="cols in getTable().length">
                {{ getTable()[cols-1][rows] }}
            </td>
        </tr>
    </table>
</template>
