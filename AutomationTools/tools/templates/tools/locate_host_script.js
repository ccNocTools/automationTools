mac_address_boxes = document.querySelectorAll(".mac_address_input");
host_switch_ip_box = document.querySelector("#host_switch_ip");
host_switch_select = document.querySelector("#host_switch_select");
password_box = document.querySelector("#password");
password_monkey = document.querySelector("#password_monkey");
password_monkey.style.cursor = "pointer";

function check_mac(){
    for (i = 0; i < mac_address_boxes.length; ++i){
        mac_address_box = mac_address_boxes[i];
        lastChar = mac_address_box.value.substr(mac_address_box.value.length - 1);
        if (!lastChar.match(/[0-9A-Fa-f]/)){
            mac_address_box.value = mac_address_box.value.substr(0, mac_address_box.value.length - 1);
        }
        if (mac_address_box.value.length == 4 && i != 2){
            mac_address_boxes[i+1].focus();
        }
        else{
            return;
        }
    }
}

function set_host_switch(){
    host_switch_ip_box.value = host_switch_select.value;
}

function show_password(){
    if (password_box.type == "password"){
        password_box.type = "text";
        password_monkey.innerHTML = "&#128053";
    }
    else{
        password_box.type = "password";
        password_monkey.innerHTML = "&#128584";
    }
}

function page_load() {
    if ("{{message}}" != ""){
    //alert("{{message}}");
    }
}