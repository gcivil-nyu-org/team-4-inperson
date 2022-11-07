/*
Handlers for Course/Professor Result Filtering
 */
function getListOfChecked() {
  var listOfChecked = [];
  var checkBoxes = document.querySelectorAll("input[type=checkbox]:checked");
  for (var i = 0; i < checkBoxes.length; i++) {
    listOfChecked.push(checkBoxes[i].id);
  }
  return listOfChecked;
}

function resultCheckBoxClicked() {
    var listOfChecked = getListOfChecked();
    console.log(listOfChecked);
    var listOfItems = document.getElementsByClassName("detail-sub-course-desc");
    for (var i = 0; i < listOfItems.length; i++) {
        var element = listOfItems[i];
        var isFound = false;
        for (var j = 0; j < listOfChecked.length; j++) {
            if (element.textContent.includes(listOfChecked[j])) {
                isFound = true;
                break;
            }
        }
        if (isFound) {
            element.style.display = "block";
        } else {
            element.style.display = "none";
        }
    }
}
