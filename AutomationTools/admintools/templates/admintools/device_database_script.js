add_device_form = document.querySelector("#add_device_form");
add_device_button = document.querySelector("#add_device_button");
delete_devices_button = document.querySelector("#delete_devices_button");

check_boxes = document.querySelectorAll(".check_box");

for (i = 0; i < check_boxes.length; ++i){
    check_boxes[i].addEventListener("click", function(){
        for (i = 0; i < check_boxes.length; ++i){
            if (check_boxes[i].checked){
            delete_devices_button.classList.remove("invisible");
            return;
            }
        }
        delete_devices_button.classList.add("invisible");
    }, false);
}

edit_buttons = document.querySelectorAll("input[class='edit_button']");

for(i = 0; i < edit_buttons.length; ++i){

    edit_buttons[i].addEventListener("click", function(){

        for(i = 0; i < check_boxes.length; ++i){
            check_boxes[i].checked = false;
            delete_devices_button.classList.add("invisible");
        }

        label_id = this.name + "_name_box";
        all_labels = document.querySelectorAll('label');
        for(j = 0; j < all_labels.length; ++j){
            if (all_labels[j].id == label_id){
                name_box_label = all_labels[j];
            }
        }

        label_id = this.name + "_type_box";
        for(j = 0; j < all_labels.length; ++j){
            if (all_labels[j].id == label_id){
                type_box_label = all_labels[j];
            }
        }

        all_inputs = document.querySelectorAll('input');
        input_id = this.name + "_input_box";
        for(j = 0; j < all_inputs.length; ++j){
            if (all_inputs[j].id == input_id){
                name_input_box = all_inputs[j];
                break;
            }
        }

        input_id = this.name + "_type_input_box";
        for(j = 0; j < all_inputs.length; ++j){
            if (all_inputs[j].id == input_id){
                type_input_box = all_inputs[j];
                break;
            }
        }

        if (this.value == 'Submit'){
            if ((this.id == name_input_box.value) && (type_box_label.innerHTML == type_input_box.value)){
                name_box_label.style.display = 'block';
                type_box_label.style.display = 'block';
                name_input_box.type = 'hidden';
                type_input_box.type = 'hidden';
                this.value = '   Edit  ';
            }
            else{
                devices_form = document.querySelector('#devices_form');
                confirmed = confirm("Are you sure?");
                if (confirmed)
                    devices_form.submit();
                else{
                    name_box_label.style.display = 'block';
                    type_box_label.style.display = 'block';
                    name_input_box.type = 'hidden';
                    type_input_box.type = 'hidden';
                    this.value = '   Edit  ';
                }
            }
        }
        else{
        name_box_label.style.display = 'none';
        type_box_label.style.display = 'none';
        name_input_box.type = 'text';
        type_input_box.type = 'text';
        name_input_box.value = this.id;
        type_input_box.value = type_box_label.innerHTML;
        name_input_box.style.width = "100%";
        type_input_box.style.width = "100%";
        this.value = 'Submit';
        }
    }, false);
}

function page_load() {
    if ("{{message}}" != ""){
    alert("{{message}}");
    }
}

history.pushState({}, null, '/admintools/device_database');

add_device_button.addEventListener("click", function(){
    if (add_device_button.innerHTML == "Add Device"){
        add_device_form.classList.remove("invisible");
        add_device_button.innerHTML = "Hide";
        }
    else{
        add_device_form.classList.add("invisible");
        add_device_button.innerHTML = "Add Device";
    }
}, false);


