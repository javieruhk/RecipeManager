function submit_form(element){
	document.getElementById(element).submit();
}

function underline_onmouseover(element) {  
	document.getElementById(element).style.textDecoration ='underline';
}

function not_underline_onmouseout(element){
	document.getElementById(element).style.textDecoration = 'none'
}