function callOnload()
{
    alert("Hi");

}

function allowAlphabets()
{
	var key = window.event.keyCode;
	if(!((key>64 && key<91) || (key>96 && key<123)))
	{
		window.event.returnValue = false;
	}
}

