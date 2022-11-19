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
}
/*
Handlers for auto-population and auto-fill on input boxes of Add Review form
 */
let courseTitlesDatalist = document.getElementById('courses_datalist');
let courseIdsDatalist = document.getElementById('course_ids_datalist');
let professorsDataList = document.getElementById('professors_datalist');
function courseNameInputted(e, addReviewCourseId, coursesData, professorsData) {
    // If input is empty, clear Course ID field and unfilter Professor Name
    if (e.target.value === "") {
        addReviewCourseId.value = "";
        replaceDataListOptions(professorsDataList, professorsData.map((obj) => obj['professor_name']));
    }

    let matchingCourse = coursesData.find((course) => {
        return course['course_title'] === e.target.value;
    });
    if (matchingCourse) {
        // Auto-populate Display Course ID
        addReviewCourseId.value = matchingCourse['display_course_id'];

        // Filter Professor Name options
        let newOptions = matchingCourse['professors'].map(value => value['professor_name']);
        replaceDataListOptions(professorsDataList, newOptions);
    }
}

function courseIdInputted(e, addReviewCourseName, coursesData, professorsData) {
    // If input is empty, clear Course Name field and unfilter Professor Name
    if (e.target.value === "") {
        addReviewCourseName.value = "";
        replaceDataListOptions(professorsDataList, professorsData.map((obj) => obj['professor_name']));
    }

    let matchingCourse = coursesData.find((course) => {
        return course['display_course_id'] === e.target.value;
    });
    if (matchingCourse) {
        // Auto-populate Course Name
        addReviewCourseName.value = matchingCourse['course_title'];

        // Filter Professor Name options
        let newOptions = matchingCourse['professors'].map(value => value['professor_name']);
        replaceDataListOptions(professorsDataList, newOptions);
    }
}

function professorNameInputted(e, addReviewCourseName, addReviewCourseId, coursesData, professorsData) {
    // If input is empty, unfilter Course Name and Course ID
    if (e.target.value === "") {
        replaceDataListOptions(courseTitlesDatalist, coursesData.map((obj) => obj['course_title']));
        replaceDataListOptions(courseIdsDatalist, coursesData.map((obj) => obj['display_course_id']));
    }

    let matchingProfessor = professorsData.find((professor) => {
        return professor['professor_name'] === e.target.value;
    })
    if (matchingProfessor) {
        // Filter Course Name and Course ID options
        let newCourseTitleOptions = matchingProfessor['courses'].map(value => value['course_title']);
        let newCourseIdOptions = matchingProfessor['courses'].map(value => value['display_course_id']);
        replaceDataListOptions(courseTitlesDatalist, newCourseTitleOptions);
        replaceDataListOptions(courseIdsDatalist, newCourseIdOptions);
    }
}

// Removes options from a given datalist that are not in newOptions
function filterOptions(dataList, newOptions) {
    let i, L = dataList.options.length - 1;
    for(i = L; i >= 0; i--) {
        let currentChild = dataList.children[i];
        if (!newOptions.includes(currentChild.value))
            dataList.removeChild(currentChild);
    }
}

// Replaces options in the given dataList with newOptions
function replaceDataListOptions(dataList, newOptions) {
    // Add new options if they are not present
    let existingOptions = [].slice.call(dataList.options).map((option) => option.value);
    newOptions.forEach((optionValue) => {
        if (!existingOptions.includes(optionValue)){
            let newOption = document.createElement('option');
            newOption.value = optionValue;
            dataList.appendChild(newOption);
        }
    });

    // Remove old options
    filterOptions(dataList, newOptions);
}

//adapted from https://medium.com/geekculture/how-to-build-a-simple-star-rating-system-abcbb5117365
document.addEventListener('DOMContentLoaded', function(){
    (function(){
        let sr = document.querySelectorAll('.my-star');
        let i = 0;
        //loop through stars
        while (i < sr.length){
            //attach click event
            sr[i].addEventListener('click', function(){
                //current star
                let cs = parseInt(this.getAttribute("data-star"));
                //output current clicked star value
                // document.querySelector('#output').value = cs;
                document.getElementById('review_rating').value=cs;
                /*our first loop to set the class on preceding star elements*/
                let pre = cs; //set the current star value
                //loop through and set the active class on preceding stars
                while(1 <= pre){
                    //check if the classlist contains the active class, if not, add the class
                    if(!document.querySelector('.star-'+pre).classList.contains('is-active')){
                        document.querySelector('.star-'+pre).classList.add('is-active');
                    }
                    //decrement our current index
                    --pre;
                }//end of first loop

                /*our second loop to unset the class on succeeding star elements*/
                //loop through and unset the active class, skipping the current star
                let succ = cs+1;
                while(5 >= succ){
                    //check if the classlist contains the active class, if yes, remove the class
                    if(document.querySelector('.star-'+succ).classList.contains('is-active')){
                        document.querySelector('.star-'+succ).classList.remove('is-active');
                    }
                    //increment current index
                    ++succ;
                }

            })//end of click event
            i++;
        }//end of while loop
    })();//end of function
})


// Function to display review form on course results page
function showReviewForm() {
    let reviewForm = document.getElementById("add-review");
    reviewForm.style.display = "block";
}

function hideReviewForm() {
    let reviewForm = document.getElementById("add-review");
    reviewForm.style.display = "none";
}

/*
Handlers for Course Detail Filtering
 */
function professorSelect(professor)
{
        let listOfReviews = document.querySelectorAll(".review");
        listOfReviews.forEach(element => {
        let review_professor = element.getAttribute('review_professor');
        if (review_professor.includes(professor)) {
            element.style.display = "flex";
        } else {
            element.style.display = "none";
        }
    });
}

/*
Handlers for Professor Detail Filtering
 */
function courseSelect(course)
{
        let listOfReviews = document.querySelectorAll(".review");
        listOfReviews.forEach(element => {
        let review_course = element.getAttribute('review_course');
        if (review_course.includes(course)) {
            element.style.display = "flex";
        } else {
            element.style.display = "none";
        }
    });
}

function hideProfile(elements) {
    elements = elements.length ? elements : [elements];
    for (let index = 0; index < elements.length; index++) {
        elements[index].style.display = 'none';
    }
    document.getElementById('edit_profile_div').style.display = 'block'
    let input_dropdown = document.getElementById('user_status_input')
    let student_status = document.getElementById('user_status').innerHTML

    for (let i, j = 0; i = input_dropdown.options[j]; j++) {
        if (String(i.value).trim() === String(student_status).trim()) {
            input_dropdown.selectedIndex = j;
            break;
        }
    }
}

function save(elements){
    elements = elements.length ? elements : [elements];
    for (let index = 0; index < elements.length; index++) {
        elements[index].style.display = 'none';
    }
    document.getElementById('profile_div').style.display = 'block'
}
