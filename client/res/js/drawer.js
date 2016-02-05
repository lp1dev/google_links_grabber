var isDrawerOpened = false;
var mainContainer, navigationDrawer, filter, header;
document.addEventListener("DOMContentLoaded", function(event) {
    mainContainer = document.getElementById("mainContainer");
    navigationDrawer = document.getElementById("drawer");
    header = document.getElementById("headerContent");
    filter = document.getElementById("filter");
    mainContainer.style.marginLeft = 0;
    header.style.marginLeft = 0;
});

function isMobile(){
    if( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) )
	return true
    return false;
}

function drawer(){
    if (isDrawerOpened)
	closeDrawer();
    else
	openDrawer();
    isDrawerOpened = !isDrawerOpened;
}


function openDrawer(){
    navigationDrawer.className = "drawer";
    if (isMobile()){
	filter.style.visibility = "visible";
    }
    else{
	mainContainer.style.marginLeft = navigationDrawer.style.width;
	header.style.marginLeft = navigationDrawer.style.width;
    }
}

function closeDrawer(){
    navigationDrawer.className = "drawer shadowed closed";
    if (isMobile()){
	filter.style.visibility = "hidden";	
    }
    else{
	mainContainer.style.marginLeft = 0;
	header.style.marginLeft = 0;
    }
}
