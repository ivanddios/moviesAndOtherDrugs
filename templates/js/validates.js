function changeColors(element, color){
    element.style.borderColor = color; // Input
    element.previousElementSibling.style.backgroundColor = color; //Previous Element in the same div (icon)
}

function checkText(textInput) {
    var expr = /([A-Za-z0-9ñÑ-áéíóúÁÉÍÓÚ]+[\s]*)+$/;
    console.log(textInput.value);
    if (expr.test(textInput.value) && textInput.value.length > 0 && textInput.value.length < 225) {
        changeColors(textInput, "green");
        return true;
    } else {
        changeColors(textInput, "red");
        return false;
    }
}

function validateList(form) {
    if (checkText(form.edName) && checkText(form.edDescription)) {
        document.getElementById("saveButton").disabled = false;
    } else {
        document.getElementById("saveButton").disabled = true;
    }
}


function searchInTable() {
    let filter = document.getElementById("searchBox").value.toUpperCase(),
        tr = document.getElementById("dataTable").getElementsByTagName("tr");

    for (let i = 0; i < tr.length; i++) {
        let isFound = true, j=0;
        while(isFound && j < tr[i].childElementCount-1){  /* childElementCount - 1 because the last tr's child is a td where are the actions buttons */
                let td = tr[i].getElementsByTagName("td")[j];
            if (td) {
                if (td.innerText.toUpperCase().indexOf(filter) > -1) {
                    tr[i].style.display = '';
                    isFound = false;
                } else {
                    tr[i].style.display = 'none';
                }
            }
            j++;
        }
    }
}