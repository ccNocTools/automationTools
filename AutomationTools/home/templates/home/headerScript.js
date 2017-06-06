
tools_menu = document.querySelector("#tools_menu");
tools_menu_options = document.createElement("span");
main_menu = document.querySelector("#header_bar");

tools_option_1 = document.createElement("div");
get_os_button = document.createElement("button");
get_os_button.classList.add("submenu_button");
get_os_link = document.createElement("a");
get_os_link.setAttribute('href', '{% url "tools:get_os" %}');
get_os_link_text = document.createTextNode("Get OS");
get_os_button.appendChild(get_os_link_text);
get_os_link.appendChild(get_os_button);
tools_option_1.appendChild(get_os_link);
tools_menu_options.appendChild(tools_option_1);

tools_option_2 = document.createElement("div");
locate_host_button = document.createElement("button");
locate_host_button.classList.add("submenu_button");
locate_host_link = document.createElement("a");
locate_host_link_text = document.createTextNode("Locate Host");
locate_host_link.setAttribute('href', '{% url "tools:locate_host" %}');
locate_host_button.appendChild(locate_host_link_text);
locate_host_link.appendChild(locate_host_button);
tools_option_2.appendChild(locate_host_link);
tools_menu_options.appendChild(tools_option_2);

tools_menu_options.style.visibility = "hidden";
tools_menu_options.classList.add("tools_menu");
tools_menu.appendChild(tools_menu_options);
get_os_button.classList.add("header_button");
locate_host_button.classList.add("header_button");

function hide_tools_menu(){
    tools_menu_options.style.visibility = "hidden";
}
function show_tools_menu(){
   tools_menu_options.style.visibility = "visible";
}

{% if is_admin == "True" %}
    admin_tools_menu = document.querySelector("#admin_tools_menu");
    admin_tools_menu_options = document.createElement("span");
    admin_tools_menu_options.classList.add("tools_menu");

    admin_tools_option_1 = document.createElement("div");
    users_button = document.createElement("button");
    users_button.classList.add("submenu_button");
    users_link = document.createElement("a");
    users_link.setAttribute('href', '{% url "admintools:users" %}');
    users_link_text = document.createTextNode("Users");
    users_button.appendChild(users_link_text);
    users_link.appendChild(users_button);
    admin_tools_option_1.appendChild(users_link);
    admin_tools_menu_options.appendChild(admin_tools_option_1);

    admin_tools_option_2 = document.createElement("div");
    devices_button = document.createElement("button");
    devices_button.classList.add("submenu_button");
    devices_link = document.createElement("a");
    devices_link.setAttribute('href', '{% url "admintools:device_database" %}');
    devices_link_text = document.createTextNode("Device Database");
    devices_button.appendChild(devices_link_text);
    devices_link.appendChild(devices_button);
    admin_tools_option_2.appendChild(devices_link);
    admin_tools_menu_options.appendChild(admin_tools_option_2);

    admin_tools_option_3 = document.createElement("div");
    com_str_button = document.createElement("button");
    com_str_button.classList.add("submenu_button");
    com_str_link = document.createElement("a");
    com_str_link.setAttribute('href', '{% url "admintools:community_string" %}');
    com_str_link_text = document.createTextNode("Community String");
    com_str_button.appendChild(com_str_link_text);
    com_str_link.appendChild(com_str_button);
    admin_tools_option_3.appendChild(com_str_link);
    admin_tools_menu_options.appendChild(admin_tools_option_3);

    admin_tools_menu_options.style.visibility = "hidden";
    admin_tools_menu_options.classList.add("tools_menu");

    admin_tools_menu.appendChild(admin_tools_menu_options);
    users_button.classList.add("header_button");
    devices_button.classList.add("header_button");
    com_str_button.classList.add("header_button");

    function hide_admin_tools_menu(){
        admin_tools_menu_options.style.visibility = "hidden";
    }
    function show_admin_tools_menu(){
        admin_tools_menu_options.style.visibility = "visible";
    }
{% endif %}

main_menu.style.visibility="hidden";
main_menu.style.position="absolute";

show_main_menu = function(){
    event.stopPropagation();
    if(main_menu.style.visibility == "hidden"){
        main_menu.style.visibility = "visible";
        body.addEventListener("click", function(){
        {% if is_admin == "True"  %}
            admin_tools_menu_options.style.visibility = "hidden";
        {% endif %}
        tools_menu_options.style.visibility = "hidden";
        main_menu.style.visibility = "hidden";
        }, false);
    }
    else{
        main_menu.style.visibility = "hidden";
    }
}
body = document.querySelector("html");
