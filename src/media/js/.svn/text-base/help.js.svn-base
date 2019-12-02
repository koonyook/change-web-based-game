var loadonce = false;
function LoadHelpMenu()
{
	if(loadonce)
		return;
	loadonce = true;
	$.getJSON("/help/get_enabled_menu/",function(data) 
	{
		$('#help_list').html('');
		for(var key in data)
		{
			if(data[key]["enabled"])
				$('#help_list').append('<li><div id="help_title_'+data[key]["tag"]+'" class="help_menu_button button">'+data[key]["name"]+'</div></li>');
		}
		$('.help_menu_button').click(function()
		{
			$('.help_menu_button').removeClass("help_menu_button_selected");
			$(this).addClass("help_menu_button_selected");
			LoadContentHelp($(this).attr("id").substring(11));
		});
	});
	$('#help_close').click(function(){
		CloseHelp();
	});
}
function ShowHelp()
{
	LoadHelpMenu();
	$('#help_box').fadeIn("fast");
	//$('#help_content').html('');
}
function LoadContentHelp(topic)
{
	$.post("/help/get_help/", {
		topic: topic
	},function(data)
	{
		$('#help_content').html(data);
		$('#help_content').scrollTop(0);
	});
}
function CloseHelp()
{
	$('#help_box').hide();
}