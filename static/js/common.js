$(function(){
    bindToggler();
});

function bindToggler(){
    $('#menu-btn, .w3-bar-item').click(function(){
        $('#main').toggleClass('toggle');
    })
}

function w3_open() {
//  document.getElementById("main").style.marginLeft = "0%";
//  document.getElementById("mySidebar").style.width = "13%";
//  document.getElementById("mySidebar").style.display = "block";
//  document.getElementById("openNav").style.display = 'none';
}

function w3_close() {
//  document.getElementById("main").style.marginLeft = "0%";
//  document.getElementById("mySidebar").style.display = "none";
//  document.getElementById("openNav").style.display = "inline-block";
}