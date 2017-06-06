add_user_form = document.querySelector("#add_user_form");
add_user_button = document.querySelector("#add_user_button");
user_options = document.querySelector("#user_options");
check_boxes = document.querySelectorAll(".check_box");

for (i = 0; i < check_boxes.length; ++i){
    check_boxes[i].addEventListener("click", function(){
        for (i = 0; i < check_boxes.length; ++i){
            if (check_boxes[i].checked){
            user_options.classList.remove("invisible");
            return;
            }
        }
        user_options.classList.add("invisible");
    }, false);
}

function page_load() {
    add_user_form.classList.add("invisible");
    user_options.classList.add("invisible");
    if ("{{message}}" != ""){
    alert("{{message}}");
    }
}

history.pushState({}, null, '/admintools/users');

add_user_button.addEventListener("click", function(){
    if (this.innerHTML == 'Add User'){
        add_user_form.classList.remove("invisible");
        this.innerHTML = "Hide";
        }
    else{
        add_user_form.classList.add("invisible");
        this.innerHTML = "Add User";
    }
}, false);
