var lastData = {};
var isFetching = false;
var interval;

function hasChanged(){
    var query = $("#search").val();
    $.getJSON('http://2.lp1.eu:5000/search/'+query, success);
    
    function success(data) {
	$("#contentDiv").empty();
	if (!isFetching)
	    $("#contentDiv").html("<p>Do you mean :</p>");
	else
	    $("#contentDiv").html("<p>Nothing found, fetching...</p>");
	lastData = data;
	console.log(data);
	console.log(data.length);
	$.each(data, function(key) {
	    var htmlContent = $("#contentDiv").html()+"<p style='color:red' onclick='onLinkClick(this);'>"+key+"</p>";
	    $("#contentDiv").html(htmlContent);
	});
	if ($.isEmptyObject(data)){
	    if (isFetching == false){
		isFetching = true;
		console.log("data is null, fetching");
		$.getJSON('http://2.lp1.eu:5000/fetch/'+query, fetch_success);
		$("#contentDiv").html("Loading...");
		interval = setInterval(function() {
		    if (isFetching)
			hasChanged();
		}, 8000);
	    }
	}
    }
    
    function fetch_success(data) {
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
