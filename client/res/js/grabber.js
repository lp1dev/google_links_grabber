var lastData = {};
var isFetching = false;
var interval;
var search_url = "http://2.lp1.eu:5000/search/"
var fetch_url = "http://2.lp1.eu:5000/fetch/"

$(document).ready(function(){
    $("#search").on('input', function(){
	var query = $("#search").val()

	console.log("input has changed");
	$("#contentDiv").empty();
	if (query.length > 1)
	    $.getJSON(search_url+$("#search").val().toLowerCase(), predictive_input);
    });
});

function predictive_input(data){
    $.each(data, function(key) {
	var htmlContent = $("#contentDiv").html()+"<p style='color:red' onclick='onLinkClick(this);'>"+key+"</p>";
	$("#contentDiv").html(htmlContent);
    });
}

function hasChanged(){
    var query = $("#search").val().toLowerCase();
    $.getJSON(search_url+query, search_success);

    function search_success(data) {
	$("#contentDiv").empty();
	if (isFetching)
	    $("#contentDiv").html("<p>Nothing in database, seeking external sources...</p>");
	lastData = data;
	console.log(data);
	if ($.isEmptyObject(data)){
	    if (isFetching == false){
		isFetching = true;
		$.getJSON(fetch_url+query, fetch_success);
		$("#contentDiv").html("Loading...");
		interval = setInterval(function() {
		    if (isFetching)
			hasChanged();
		}, 8000);
	    }
	}
	else{
	    if (isFetching == true)
		isFetching = false;
	    clearInterval(interval);
	}
    }
    
    function fetch_success(data) {
	isFetching = false;
	clearInterval(interval);
    }
}

function onLinkClick(div){
    var selectedData = lastData[$(div).html()][0];
    console.log(selectedData);
    $("#contentDiv").empty();
    for (var i = 0; i < selectedData.length; i++)
    {
	var link = selectedData[i];
	console.log($("#contentDiv").html());
	$("#contentDiv").html($("#contentDiv").html()+"<p><a href='"+link+"'>"+link+"</a></p>");
    }
}
