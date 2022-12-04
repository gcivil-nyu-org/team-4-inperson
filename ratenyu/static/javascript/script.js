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
Handlers for Add Review form
 */
let courseTitlesDatalist = document.getElementById('courses_datalist');
let courseIdsDatalist = document.getElementById('course_ids_datalist');
let professorsDataList = document.getElementById('professors_datalist');
function courseNameInputted(e, addReviewCourseId, coursesData, professorsData) {
    removeErrorMessage('add-review-status', 'no-course-title-found-message');
    removeErrorMessage('add-review-status', 'no-course-title-id-match-message');

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
    removeErrorMessage('add-review-status', 'no-course-title-id-match-message');
    removeErrorMessage('add-review-status', 'no-course-professor-match-message');
    removeErrorMessage('add-review-status', 'no-course-id-found-message');

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
    removeErrorMessage('add-review-status', 'no-course-professor-match-message');

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

function reviewTextInputted() {
    removeErrorMessage('add-review-status', 'no-review-text-entered-message');
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

// Custom form validation
function validateForm(coursesData) {
    let courseTitle = document.forms['add_review_form']['add_review_course_title'].value;
    let courseId = document.forms['add_review_form']['add_review_course_id'].value;
    let professorName = document.forms['add_review_form']['add_review_professor_name'].value;
    let matchingCourseId = coursesData.find((course) => {
        return course['display_course_id'] === courseId;
    });
    let matchingCourseTitle = coursesData.find((course) => {
        return course['course_title'] === courseTitle;
    });

    // Validate Course Name, CourseID, and Course/Professor combo
    if (!matchingCourseTitle) {
        addErrorMessage('add-review-status',
            'No Course found with Course Title "' + courseTitle + '."',
            'no-course-title-found-message');
        return false;
    }
    if (!matchingCourseId) {
        addErrorMessage('add-review-status',
            'No Course found with Course ID "' + courseId + '."',
            'no-course-id-found-message');
        return false;
    } else {
        if (matchingCourseTitle['display_course_id'] !== matchingCourseId['display_course_id']) {
            addErrorMessage('add-review-status',
                'No match found for Course Title "' + courseTitle + '" and Course ID "' + courseId + '."',
                'no-course-title-id-match-message');
            return false;
        }
        let professorOptions = matchingCourseId['professors'].map(value => value['professor_name']);
        if (!professorOptions.includes(professorName)) {
            addErrorMessage('add-review-status',
                'No match found for Course ID "' + courseId + '" and Professor "' + professorName + '."',
                'no-course-professor-match-message');
            return false;
        }
    }

    // Validate Rating requirement
    return validateRatingRequirement();
}

function validateReviewTextAndRatingRequirement() {
    let reviewTextInput = document.querySelector('[name="review_text"]');
    if (reviewTextInput.value === "") {
        addErrorMessage('add-review-status',
            'Review Text cannot be empty.',
            'no-review-text-entered-message');
        return false;
    }
    return validateRatingRequirement();
}

function validateRatingRequirement() {
    let star = document.querySelector('.my-star.add-star.star-1');
    if (!star.classList.contains('is-active')) {
        addErrorMessage('add-review-status',
                'Please select a Review Rating.',
                'no-rating-entered-message');
            return false;
    }
    hideReviewForm();
    this.disabled = true;
    return true;
}

function addErrorMessage(divId, message, errorMessageId) {
    let divParent = document.getElementById(divId);
    let errorMessage = document.createElement('h4');
    errorMessage.id = errorMessageId;
    errorMessage.style.color = 'red';
    errorMessage.innerHTML = message;
    divParent.appendChild(errorMessage);
}

function removeErrorMessage(divId, errorMessageId) {
    let divParent = document.getElementById(divId);
    let errorMessage = document.getElementById(errorMessageId);
    if (errorMessage) {
        divParent.removeChild(errorMessage);
    }
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
                removeErrorMessage('add-review-status', 'no-rating-entered-message');
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


// Functions to display edit review form on Profile plage
function showEditForm(reviewId) {
    let staticText = document.querySelector("[name=static-review-text-" + CSS.escape(reviewId) + "]")
    staticText.style.display = "none";

    let editForm = document.querySelector("[name=edit-review-form-" + CSS.escape(reviewId) + "]")
    editForm.style.display = "block";

    let stars = editForm.childNodes[5];
    let rating_val = editForm.childNodes[8];
    let sr = stars.querySelectorAll('.prof-star');

    let curr_rating = rating_val.value;
    let max_star = curr_rating;

    while(1 <= max_star){
        if(!stars.querySelector('.star-'+max_star).classList.contains('is-active')){
            stars.querySelector('.star-'+max_star).classList.add('is-active');
        }
        --max_star;
    }

    let i = 0;
    //loop through stars
    while (i < sr.length) {
        //attach click event
        sr[i].addEventListener('click', function () {
            //current star
            let cs = parseInt(this.getAttribute("data-star"));
            //output current clicked star value
            rating_val.value = cs;
            let pre = cs;

            while(1 <= pre){
                //check if the classlist contains the active class, if not, add the class
                if(!stars.querySelector('.star-'+pre).classList.contains('is-active')){
                    stars.querySelector('.star-'+pre).classList.add('is-active');
                }
                //decrement our current index
                --pre;
            }

            let succ = cs+1;
            while(5 >= succ){
                //check if the classlist contains the active class, if yes, remove the class
                if(stars.querySelector('.star-'+succ).classList.contains('is-active')){
                    stars.querySelector('.star-'+succ).classList.remove('is-active');
                }
                //increment current index
                ++succ;
            }
        })//end of click event
        i++;
    }//end of while loop

}

function hideEditForm(reviewId) {
    let editForm = document.querySelector("[name=edit-review-form-" + CSS.escape(reviewId) + "]")
    editForm.style.display = "none";

    let staticText = document.querySelector("[name=static-review-text-" + CSS.escape(reviewId) + "]")
    staticText.style.display = "block";

}

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
        var visible = 0;
        listOfReviews.forEach(element => {
        let review_professor = element.getAttribute('review_professor');
        if (review_professor.includes(professor)) {
            element.style.display = "flex";
            visible++;
        } else {
            element.style.display = "none";
        }
    });
    if (visible == 0) {
        //insert no reviews tag in here
        document.getElementsByClassName("no-reviews")[0].style.display = "block";
    } else {
        document.getElementsByClassName("no-reviews")[0].style.display = "none";
    }
}

/*
Handlers for Professor Detail Filtering
 */
function courseSelect(course)
{
        let listOfReviews = document.querySelectorAll(".review");
        var visible = 0;
        listOfReviews.forEach(element => {
        let review_course = element.getAttribute('review_course');
        if (review_course.includes(course)) {
            element.style.display = "flex";
            visible++;
        } else {
            element.style.display = "none";
        }
        });
        if (visible == 0) {
            //insert no reviews tag in here
            document.getElementsByClassName("no-reviews")[0].style.display = "block";
        } else {
            document.getElementsByClassName("no-reviews")[0].style.display = "none";
        }
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
    window.location.reload();
}


function sortReviews(selectObject) {
    let reviews = document.getElementsByClassName('review');
    let reviewsArr = Array.from(reviews);
    switch (selectObject.value) {
        case 'RatingDesc':
            reviewsArr.sort((a,b) => {
                let nameA = a.children[0].children[2].textContent;
                let nameB = b.children[0].children[2].textContent;
                if (nameA > nameB) {
                    return -1;
                }
                else {
                    return 1;}
                });
            break;
        case 'RatingAsc':
            reviewsArr.sort((a,b) => {
                let nameA = a.children[0].children[2].textContent;
                let nameB = b.children[0].children[2].textContent;
                if (nameA < nameB) {
                    return -1;
                }
                else {
                    return 1;}
                });
            break;
        case 'RevDateDesc':
            reviewsArr.sort((a, b) => {
                let nameA = Date.parse(a.children[0].children[0].textContent);
                let nameB = Date.parse(b.children[0].children[0].textContent);
                if (nameA > nameB) {
                    return -1;
                } else {
                    return 1;
                }
            });
            break;
        case 'RevDateAsc':
            reviewsArr.sort((a, b) => {
                    let nameA = Date.parse(a.children[0].children[0].textContent);
                    let nameB = Date.parse(b.children[0].children[0].textContent);
                    if (nameA < nameB) {
                        return -1;
                    } else {
                        return 1;
                    }
                });
                break;
        }
    for (var i = 0; i < reviewsArr.length; i++) {
        reviews[0].parentElement.appendChild(reviewsArr[i]);
    }
}

function showSaveCourseForm() {
    let saveCourseForm = document.getElementById("save-course-form");
    saveCourseForm.style.display = "block";
}



/*
Handlers for Like/Dislike Button functionality
 */
function likeReview(review_id) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const likeButton = document.getElementById('like-' + review_id);
    const dislikeButton = document.getElementById('dislike-' + review_id);
    let likeCount = document.getElementById('like-count-' + review_id).innerHTML;
    let dislikeCount = document.getElementById('dislike-count-' + review_id).innerHTML;
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            if (likeButton.classList.contains('active')) {
                likeButton.classList.remove('active');
                document.getElementById('like-count-' + review_id).innerHTML = (parseInt(likeCount) - 1).toString();
            } else {
                if (dislikeButton.classList.contains('active')) {
                    dislikeButton.classList.remove('active');
                    document.getElementById('dislike-count-' + review_id).innerHTML = (parseInt(dislikeCount) - 1).toString();
                }
                likeButton.classList.add('active');
                document.getElementById('like-count-' + review_id).innerHTML = (parseInt(likeCount) + 1).toString();
            }
        }
    };
    xhttp.open("POST", review_id+"/like", true);
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    xhttp.send();
 }

 function dislikeReview(review_id) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const likeButton = document.getElementById('like-' + review_id);
    const dislikeButton = document.getElementById('dislike-' + review_id);
    let likeCount = document.getElementById('like-count-' + review_id).innerHTML;
    let dislikeCount = document.getElementById('dislike-count-' + review_id).innerHTML;
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            if (dislikeButton.classList.contains('active')) {
                dislikeButton.classList.remove('active');
                document.getElementById('dislike-count-' + review_id).innerHTML = (parseInt(dislikeCount) - 1).toString();
            } else {
                if (likeButton.classList.contains('active')) {
                    likeButton.classList.remove('active');
                    document.getElementById('like-count-' + review_id).innerHTML = (parseInt(likeCount) - 1).toString();
                }
                dislikeButton.classList.add('active');
                document.getElementById('dislike-count-' + review_id).innerHTML = (parseInt(dislikeCount) + 1).toString();
            }
        }
    };
    xhttp.open("POST", review_id+"/dislike", true);
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    xhttp.send();
 }


/*
Handlers for Like/Dislike functionality
 */
function likeReview(review_id) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const likeButton = document.getElementById('like-' + review_id);
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            if (likeButton.classList.contains('active')) {
                likeButton.classList.remove('active');
            } else {
                likeButton.classList.add('active');
            }
        }
    };
    xhttp.open("POST", review_id+"/like", true);
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    xhttp.send();
 }


/*
Handlers for Like/Dislike Button functionality
 */
function likeReview(review_id) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const likeButton = document.getElementById('like-' + review_id);
    const dislikeButton = document.getElementById('dislike-' + review_id);
    let likeCount = document.getElementById('like-count-' + review_id).innerHTML;
    let dislikeCount = document.getElementById('dislike-count-' + review_id).innerHTML;
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            if (likeButton.classList.contains('active')) {
                likeButton.classList.remove('active');
                document.getElementById('like-count-' + review_id).innerHTML = (parseInt(likeCount) - 1).toString();
            } else {
                if (dislikeButton.classList.contains('active')) {
                    dislikeButton.classList.remove('active');
                    document.getElementById('dislike-count-' + review_id).innerHTML = (parseInt(dislikeCount) - 1).toString();
                }
                likeButton.classList.add('active');
                document.getElementById('like-count-' + review_id).innerHTML = (parseInt(likeCount) + 1).toString();
            }
        }
    };
    xhttp.open("POST", review_id+"/like", true);
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    xhttp.send();
 }

 function dislikeReview(review_id) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const likeButton = document.getElementById('like-' + review_id);
    const dislikeButton = document.getElementById('dislike-' + review_id);
    let likeCount = document.getElementById('like-count-' + review_id).innerHTML;
    let dislikeCount = document.getElementById('dislike-count-' + review_id).innerHTML;
    let xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            if (dislikeButton.classList.contains('active')) {
                dislikeButton.classList.remove('active');
                document.getElementById('dislike-count-' + review_id).innerHTML = (parseInt(dislikeCount) - 1).toString();
            } else {
                if (likeButton.classList.contains('active')) {
                    likeButton.classList.remove('active');
                    document.getElementById('like-count-' + review_id).innerHTML = (parseInt(likeCount) - 1).toString();
                }
                dislikeButton.classList.add('active');
                document.getElementById('dislike-count-' + review_id).innerHTML = (parseInt(dislikeCount) + 1).toString();
            }
        }
    };
    xhttp.open("POST", review_id+"/dislike", true);
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    xhttp.send();
 }


if ( window.history.replaceState ) {
	window.history.replaceState( null, null, window.location.href );
   }


function searchPlaceholder(){

    let placeholderText = {
        "CourseID": "example: CS-GY 6003",
        "CourseName": "example: Algorithms",
        "ProfessorName": "example: John Doe"
    };

    let selection = document.getElementById("search_by");
    let inputBox = document.getElementById("query_search");
    let selectedVal = String(selection.value);
    inputBox.placeholder = String(placeholderText[selectedVal]);
}
