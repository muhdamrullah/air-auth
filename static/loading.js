$(function() {

    var loading = function() {
        // change the 'header' and 'submitbtn' accordingly
	document.getElementById("header").innerHTML = "1. Turn Your Phone Wi-Fi On";
	document.getElementById("submitbtn").innerHTML = "2. Join 'Authenticate' Wi-Fi";
	
    };

    // you won't need this button click
    // just call the loading function directly
    $('button').click(loading);

});
