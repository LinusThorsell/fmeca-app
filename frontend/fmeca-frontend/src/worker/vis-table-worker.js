// Work on stuff with this worker :)

const fix_column_sizes = "fix_column_sizes"

function fix_column_sizes_function(document) {
    console.log("in function")
    console.log(document.querySelectorAll(".vis-column"))
}

self.onmessage = ({ data }) => {
    console.log("starting worker: " + data.action)
    
    if (data.action = fix_column_sizes) {
        console.log("Fixing columns globally")
        fix_column_sizes_function(data.document)
    }
}
