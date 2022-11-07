/*
Handlers for Course/Professor Result Filtering
 */
function getListOfChecked() {
  let listOfChecked = [];
  let checkBoxes = document.querySelectorAll("input[type=checkbox]:checked");
  checkBoxes.forEach(checkBox => {
      listOfChecked.push(checkBox.id);
  })
  return listOfChecked;
}

function resultCheckBoxClicked() {
    let listOfChecked = getListOfChecked();
    let listOfItems = document.querySelectorAll(".detail-sub-course-desc");
    listOfItems.forEach(element => {
        let level = element.getAttribute('data-level').slice(-2);
        let last_offered = element.getAttribute('data-offered').slice(-4);
        console.log(level);
        console.log(last_offered);
        console.log(listOfChecked);
        if (listOfChecked.includes(level) && listOfChecked.includes(last_offered)) {
            element.style.display = "block";
        } else {
            element.style.display = "none";
        }
    });
/*
Handlers for auto-populating Course Name and Course ID on Add Review Handler
 */
function populateAddReviewCourseId(e, addReviewCourseId, coursesData) {
    let matchingCourse = coursesData.find((course) => {
        return course['course_title'] === e.target.value;
    });
    console.log(matchingCourse);
    if (matchingCourse) {
        addReviewCourseId.value = matchingCourse['course_id'];
    }
}

function populateAddReviewCourseName(e, addReviewCourseName, coursesData) {
    let matchingCourse = coursesData.find((course) => {
        return course['course_id'] === e.target.value;
    });
    console.log(matchingCourse);
    if (matchingCourse) {
        addReviewCourseName.value = matchingCourse['course_title'];
    }
}
