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
