
function page_load() {
    if ("{{message}}" != ""){
        alert("{{message}}");
    }
}

var tools_menu = document.querySelector("#tools_menu");
var tools_menu_options = document.createElement("span");
var main_menu = document.querySelector("#header_bar");

var tools_option_1 = document.createElement("div");
get_os_button = document.createElement("button");
get_os_button.classList.add("submenu_button");
get_os_button.innerHTML = "<a href = '{% url "tools:get_os" %}'>Get OS</a>";
tools_option_1.appendChild(get_os_button);
tools_menu_options.appendChild(tools_option_1);

var tools_option_2 = document.createElement("div");
locate_host_button = document.createElement("button");
locate_host_button.classList.add("submenu_button");
locate_host_button.innerHTML = "<a href = '{% url "tools:locate_host" %}'>Locate Host</a>";
tools_option_2.appendChild(locate_host_button);
tools_menu_options.appendChild(tools_option_2);

tools_menu_options.style.visibility = "hidden";
tools_menu_options.classList.add("tools_menu");
tools_menu.appendChild(tools_menu_options);

hide_tools_menu = function(){
    tools_menu_options.style.visibility = "hidden";
}
show_tools_menu=function(){
   tools_menu_options.style.visibility = "visible";
}

admin_tools_menu = document.querySelector("#admin_tools_menu");
admin_tools_menu_options = document.createElement("span");
admin_tools_menu_options.classList.add("tools_menu");

var admin_tools_option_1 = document.createElement("div");
users_button = document.createElement("button");
users_button.classList.add("submenu_button");
users_button.innerHTML="<a href='{% url "admintools:users" %}'>Users</a>";
admin_tools_option_1.appendChild(users_button);
admin_tools_option_1.style.textAlign = "left";
admin_tools_menu_options.appendChild(admin_tools_option_1);

var admin_tools_option_2 = document.createElement("div");
devices_button = document.createElement("button");
devices_button.classList.add("submenu_button");
devices_button.innerHTML = "<a href = '{% url "admintools:device_database" %}'>Device Database</a>";
admin_tools_option_2.appendChild(devices_button);
admin_tools_option_2.style.textAlign = "left";
admin_tools_menu_options.appendChild(admin_tools_option_2);

var admin_tools_option_3 = document.createElement("div");
com_str_button = document.createElement("button");
com_str_button.classList.add("submenu_button");
com_str_button.innerHTML = "<a href = '{% url "admintools:community_string" %}'>Community String</a>";
admin_tools_option_3.appendChild(com_str_button);
admin_tools_option_3.style.textAlign = "left";
admin_tools_menu_options.appendChild(admin_tools_option_3);

admin_tools_menu_options.style.visibility = "hidden";
admin_tools_menu_options.classList.add("tools_menu");

admin_tools_menu.appendChild(admin_tools_menu_options);
get_os_button.classList.add("header_button");
locate_host_button.classList.add("header_button");
users_button.classList.add("header_button");
devices_button.classList.add("header_button");
com_str_button.classList.add("header_button");

hide_admin_tools_menu=function(){
    admin_tools_menu_options.style.visibility = "hidden";
}
show_admin_tools_menu=function(){
    admin_tools_menu_options.style.visibility = "visible";
}

main_menu.style.visibility="hidden";
main_menu.style.position="absolute";

show_main_menu = function(){
    event.stopPropagation();
    if(main_menu.style.visibility == "hidden"){
        main_menu.style.visibility = "visible";
        body.addEventListener("click", function(){
        admin_tools_menu_options.style.visibility = "hidden";
        tools_menu_options.style.visibility = "hidden";
        main_menu.style.visibility = "hidden";
        }, false);
    }
    else{
        main_menu.style.visibility = "hidden";
    }
}

body = document.querySelector("html");