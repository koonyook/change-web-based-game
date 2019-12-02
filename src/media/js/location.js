var global_settings_count=0;
var global_researching = false;
function OpenResearchMinibox(){
	$('#research_box').fadeIn("fast");
}
function researching(checkresearch){
	if(checkresearch== true)
		global_researching = true;
	else if(checkresearch== false)
		global_researching = false;
	if(global_researching)
	{
		$('#researching_text').fadeIn();
		switch($('#researching_text').html())
		{
			case 'Researching':
				$('#researching_text').append('.');
				break;
			case 'Researching.':
				$('#researching_text').append('.');
				break;
			case 'Researching..':
				$('#researching_text').html('Researching');
				break;
		};
		setTimeout(researching,500);
	}
	else
	{
		$('#researching_text').hide();
	}
}
function location_js()
{
	// Home
		// Research Box
			$('#research_button').mouseover(function(event){
				$(this).stop();
				$(this).animate({
					opacity: 1.0,
				},1000);
			});
			$('#research_button').mouseout(function(event){
				$(this).stop();
				$(this).animate({
					opacity: 0.0,
				},1000);
			});
			$('#research_button').click(function(event){
				$('#research_box').fadeIn("fast");
			});
			$('#research_box_close').mouseover(function(event){
				$(this).css("background","url(/media/images/research/closehover.png)");
			});
			$('#research_box_close').mouseout(function(event){
				$(this).css("background","url(/media/images/research/close.png)");
			});
			$('#research_box_close').click(function(event){
				$('#research_box').hide();
			});
			$('#research_box').draggable({
					handle:'#research_box_title'
				});
			$('#create_union_button').click(function(){
				$('#create_union_box').fadeIn("fast");
			});
			$('#create_union_boxclose').click(function(){
				$('#create_union_box').fadeOut("fast");
			});
			$('#research_box_submit').click(function(){
				var research_arr = getItemList($('#research_box_slots'));
				var research_catas = getItemList($('#research_box_catas_slots'));
				researching(true);
				$.post("/user/research/",{
						items:research_arr,
						catas: research_catas
					},function(data){
						researching(false);
						$('#research_box_slots').html('');
						$('#research_box_catas_slots').html('');
						if(data["is_success"])
						{
							LoadItem();
							$("#sub_menu2").fadeOut();
							submenu2 = "";
							Alert(data["message"]);
							for(var loop in data["formula"]["items"])
							{
								AlertItem(data["formula"]["items"][loop]);
							}
						}
						else
						{
							Alert(data["message"]);
						}
				},'json');
			});
	// Union
			if(haveunion)
				$('#doc_bg').fadeIn();
			else
				$('#create_union_button').show();
			check_research_lock();
		// Create Union Box
			$('#create_union_boxok').click(function(){
				$.post("/core_union/new_union/",{
					union_name: $('#create_union_boxname').val()
				},function(data) 
				{
					Alert(data["message"]);
					// Disappear button
					$('#create_union_button').fadeOut("fast");
					// Disappear Dialog
					$('#create_union_box').fadeOut("fast");
				},'json');
			});
			$('#create_union_box').draggable({
				handle:'#create_union_boxtitle'
			});
	
		// Forum
			function feedtopic(){
				$('#forum_box_show_topic_list').html('');
				$.getJSON("/core_union/show_topic/",function(data) 
				{
					var mystr = '<table class="forum_table" ><thead><td>หัวข้อ</td><td>ตั้งโดย</td><td>ตอบ</td><td>ล่าสุด</td><td></td></thead></tr><tbody>';
					for(var loop in data)
					{
						mystr += '<tr><td><div id2="'+
							data[loop]["topic_id"]+'" class="forum_read_topic_button button">'+
							data[loop]["subject"]+'</div></td><td>'+
							data[loop]["owner"]+'</td><td>'+
							data[loop]["count_reply"]+'</td><td><div style="font-size:10px;">'+
							data[loop]["last_reply_at"].split(' ')[0]+'</div><div style="font-size:10px;">'+
							data[loop]["last_reply_at"].split(' ')[1]+'</div></td><td><div id2="'+
							data[loop]["topic_id"]+'" class="forum_delete_topic_button"><img src="/media/images/dialog/forum_del.png" class="button"/></div></tr>';
					}
					mystr += '</tbody></table>';
					$('#forum_box_show_topic_list').html(mystr);
					$('.forum_box_content').hide();
					$('#forum_box_show_topic').show();
					$('.forum_delete_topic_button').click(function(){
						$.post("/core_union/delete_topic/", {
							topic_id: $(this).attr('id2')
						},function(data){
							if(data["success"])
								feedtopic();
							Alert(data["message"]);
						},'json');
					});
					$('.forum_read_topic_button').click(function(){
						topicid = $(this).attr('id2')
						$.post("/core_union/read_topic/", {
							topic_id: topicid
						},function(data) 
						{
							if(data["error_message"]!="")
							{
								Alert(data["error_message"]);
							}
							else
							{
								var topicname = data["subject"];
								$('#forum_box_read_topic_title').html(data["subject"]);
								$('#forum_box_read_topic_message').html('');
								for(var loop in data["reply_list"])
								{
									$('#forum_box_read_topic_message').append(
									'<div class="forum_read_topic_each_post"><div class="forum_read_topic_lefthand"><div class="forum_read_topic_poster">'+data["reply_list"][loop]["player_name"]+
									'</div><div  class="forum_read_topic_postdate">'+data["reply_list"][loop]["reply_at"].split(' ')[0]+'</div><div  class="forum_read_topic_postdate2">'+data["reply_list"][loop]["reply_at"].split(' ')[1]+
									'</div></div><div class="forum_read_topic_righthand">'+data["reply_list"][loop]["message"]+
									'</div></div>'
									);
								}
								$('.forum_box_content').hide();
								$('#forum_box_read_topic').show();
								$('#forum_box_read_topic_reply').attr('id2',topicid);
								$('#forum_box_read_topic_reply').click(function(){
									$('#forum_box_reply_topic_title').html(topicname);
									$('#forum_box_reply_topic_reply').attr('id2',topicid);
									$('#forum_box_reply_topic_message').html('');
									$('.forum_box_content').hide();
									$('#forum_box_reply_topic').show();
									$('#forum_box_reply_topic_reply').click(function(){
										$.post("/core_union/reply_topic/", {
											topic_id: $('#forum_box_reply_topic_reply').attr('id2'),
											message: $('#forum_box_reply_topic_message').val()
										},function(data) 
										{
											if(data["success"])
											{
												$('#forum_box_reply_topic_message').val('');
												feedtopic();
											}
											Alert(data["message"]);
										},'json');
									});
								});
							}
						},'json');
					});
				});
			}
			$('#doc_forum').click(function(){
				$('.forum_box_content').hide();
				$('#forum_box_show_topic').show();
				feedtopic();
				$('#forum_box').fadeIn();
			});
			$('#forum_box_new_topic_button').click(function(){
				$('.forum_box_content').hide();
				$('#forum_box_new_topic').show();
			});
			$('#forum_box_new_topic_submit').click(function(){
				$.post("/core_union/new_topic/",{
					subject: $('#forum_box_new_topic_title').val(),
					message: $('#forum_box_new_topic_message').val()
				},function(data) 
				{
					if(data["success"])
					{
						$('#forum_box_new_topic_title').val('');
						$('#forum_box_new_topic_message').val('');
						feedtopic();
					}
					Alert(data["message"]);
				},'json');
			});
			$('#forum_box_close').click(function(){
				$('#forum_box').fadeOut();
			});
		// Setting
			$('#doc_setting').click(function(){
				$.getJSON("/core_union/show_setting/",function(data) 
				{
					if(data["error_message"])
						Alert(data["error_message"]);
					else
					{
						var enabled = data['enable_setting'];
						if(enabled)
						{
							$('#setting_save').show();
							$('#setting_auto_share').attr("read-only","True");
						}
						else
						{
							$('#setting_save').hide();
							$('#setting_auto_share').attr("read-only","False");
						}
						global_settings_count = data['setting'].length;
						$('#setting_person').html('');
						for(var loop in data['setting'])
						{
							var person = data['setting'][loop];
							var mystr = '<div id="setting_person_id'+loop+'" id2="'+person['setting_id']+'">';
							mystr += '<div class="setting_person_name">'+person['name']+'</div>';
							mystr += '<div><input type="checkbox" id="can_research" value="can_research" '+((enabled)?'':'disabled') + ' ' + ((person['can_research'])?'checked':'')+'/><span>การวิจัย</span></div>';
							mystr += '<div><input type="checkbox" id="can_transfer_item" value="can_transfer_item" '+((enabled)?'':'disabled') + ' ' + ((person['can_transfer_item'])?'checked':'')+'/><span>โอนไอเท็ม</span></div>';
							mystr += '<div><input type="checkbox" id="can_take_money" value="can_take_money" '+((enabled)?'':'disabled') + ' ' + ((person['can_take_money'])?'checked':'')+'/><span>โอนเงิน</span></div>';
							mystr += '<div><input type="checkbox" id="can_persuade"  value="can_persuade" '+((enabled)?'':'disabled') + ' ' + ((person['can_persuade'])?'checked':'')+'/><span>เชิญชวน</span></div>';
							mystr += '<div><input type="checkbox" id="can_set"  value="can_set" '+((enabled)?'':'disabled') + ' ' + ((person['can_set'])?'checked':'')+'/><span>บริหาร</span></div>';
							mystr += '<div><span>ส่วนปันผล</span><input type="textbox" id="share_rate"  value="'+person['share_rate']+'" '+(enabled?'':'readonly')+'/><span>%</span></div>';
							mystr += '</div>';
							$('#setting_person').append(mystr);
						}
						$('#setting_box').fadeIn();
					}
				});
			});
			$('#setting_save').click(function(){
				var myarr = new Array();
				myarr['setting_id'] = new Array();
				myarr['can_research'] = new Array();
				myarr['can_transfer_item'] = new Array();
				myarr['can_take_money'] = new Array();
				myarr['can_persuade'] = new Array();
				myarr['can_set'] = new Array();
				myarr['share_rate'] = new Array();
				for(var i=0;i<global_settings_count;i++)
				{
					var domtag = '#setting_person_id'+i;
					myarr['setting_id'][i] = $(domtag).attr('id2');
					myarr['can_research'][i] = $(domtag+' #can_research').attr( 'checked' );
					myarr['can_transfer_item'][i] = $(domtag+' #can_transfer_item').attr( 'checked' );
					myarr['can_take_money'][i] = $(domtag+' #can_take_money').attr( 'checked' );
					myarr['can_persuade'][i] = $(domtag+' #can_persuade').attr( 'checked' );
					myarr['can_set'][i] = $(domtag+' #can_set').attr( 'checked' );
					myarr['share_rate'][i] = $(domtag+' #share_rate').val();
				}
				$.post("/core_union/set_setting/",{
					auto_share: $('#setting_auto_share').val(),
					id_list: myarr['setting_id'],
					can_research: myarr['can_research'],
					can_transfer_item: myarr['can_transfer_item'],
					can_take_money: myarr['can_take_money'],
					can_persuade: myarr['can_persuade'],
					can_set: myarr['can_set'],
					share_rate: myarr['share_rate'],
				},function(data) 
				{
						Alert(data["message"]);
						if(data["success"])
							$('#setting_box').fadeOut();
				},'json');
			});
			$('#setting_box_close').click(function(){
				$('#setting_box').fadeOut();
			});
		// Market Box
			$('#doc_market').click(function(){
				$('#union_market_box').fadeIn();
			});
			$('.union_market_each').mouseover(function(){
				$(this).css("background","rgba(200, 200, 200, 0.4)");
			});
			$('.union_market_each').mouseout(function(){
				$(this).css("background","rgba(40, 40, 40, 0.4)");
			});
			$('.union_market_each').click(function(){
				$('#union_market_box').fadeOut();
			});
			$('#view_buy_shop_button').click(function(){
				$.post("/market/search_in_buy/", {},function(data) 
				{
					var content = '<table  class="union_market_table" style="font-size:10px;"><thead><td>ราคา</td><td>ระดับ</td>';
					content += '<td>ไอเท็ม</td><td>จำนวน</td><td>ผู้ตั้ง</td><td>เต็ม</td><td></td></thead><tbody>';
					for(var listobj in data)
					{
						content+='<tr>';
						content+='<td>'+data[listobj]['price']+'</td>';
						content+='<td>'+data[listobj]['level']+'</td>';
						content+='<td><img src="'+data[listobj]['icon_url']+'"width="16px" height="16px"/>'+data[listobj]['item_name']+'</td>';
						content+='<td>'+data[listobj]['quantity']+'</td>';
						content+='<td>'+data[listobj]['buyer']+'</td>';
						content+='<td>'+data[listobj]['must_complete']+'</td>';
						content+='<td>';
						if(data[listobj]['cancle_button'])
						{
							content+='<input type="button" id2="'+data[listobj]['id']+'" value="Cancel" class="cancel_buy"/>';
						}
						else
						{
							content+='<div id="player_buy_id'+data[listobj]['id']+'" class="item_list buy_box_slots" ></div><input type="button" id2="'+data[listobj]['id']+'" value="Sell" class="sell_buy"/>';
						}
						content+='</td>';
						content+='</tr>';
					}
					content+='</tbody></table><div id="view_buy_shop_box_close" class="button">X</div>';
					$('#view_buy_shop_box').html(content);
					$('#view_buy_shop_box').fadeIn();
					$('#view_buy_shop_box_close').click(function(){
						$('#view_buy_shop_box').fadeOut();
					});
					$('.sell_buy').click(function(){
						var myarr = getItemList($('#player_buy_id'+$(this).attr('id2')));
						$.post("/market/player_sell/",{
							buy_id: $(this).attr('id2'),
							item_id: myarr
						}, function(data) 
						{
							Alert(data);
						},'json');
					});
					$('.cancel_buy').click(function(){
						$.post("/market/cancel_buy/",{
							buy_id: $(this).attr('id2')
						}, function(data) 
						{
							Alert(data["message"]);
						},'json');
					});
					SyncItem();
				},'json');
			});
			$('#view_sell_shop_button').click(function(){
				$.post("/market/search_in_sell/",{}, function(data) 
				{
					var content = '<table class="union_market_table" style="font-size:10px;"><thead><td>ราคา</td><td>ระดับ</td>';
					content += '<td style="width:100px;">ไอเท็ม</td><td>ความคงทน</td><td>ขนาด</td><td>ผู้ขาย</td><td></td></thead><tbody>';
					for(var listobj in data)
					{
						content+='<tr>';
						content+='<td>'+data[listobj]['price']+'</td>';
						content+='<td>'+data[listobj]['level']+'</td>';
						content+='<td><img src="'+data[listobj]['icon_url']+'"width="16px" height="16px"/>'+data[listobj]['item_name']+'</td>';
						content+='<td>'+data[listobj]['durability']+'/'+data[listobj]['max_durability']+'</td>';
						content+='<td>'+data[listobj]['storage_cost']+'</td>';
						content+='<td>'+data[listobj]['seller']+'</td>';
						content+='<td>';
						if(data[listobj]['cancle_button'])
						{
							content+='<input type="button" id2="'+data[listobj]['id']+'" value="Cancel" class="cancel_sell"/>';
						}
						else
						{
							content+='<input type="button" id2="'+data[listobj]['id']+'" value="Buy" class="buy_sell"/>';
						}
						content+='</td>';
						content+='</tr>';
					}
					content+='</tbody></table><div id="view_sell_shop_box_close" class="button">X</div>';
					$('#view_sell_shop_box').html(content);
					$('#view_sell_shop_box').fadeIn();
					$('#view_sell_shop_box_close').click(function(){
						$('#view_sell_shop_box').fadeOut();
					});
					$('.buy_sell').click(function(){
						$.post("/market/player_buy/",{
							sell_id: $(this).attr('id2')
						}, function(data) 
						{
							Alert(data["message"]);
						},'json');
					});
					$('.cancel_sell').click(function(){
						$.post("/market/cancel_sell/",{
							sell_id: $(this).attr('id2')
						}, function(data) 
						{
							Alert(data["message"]);
						},'json');
					});
				},'json');
			});
			$('#set_buy_shop_button').click(function(){
				$('#set_buy_shop_box').fadeIn();
				$.post("/market/can_buy/", {},function(data) 
				{
					var mystr='';
					for(var loop in data)
					{
						mystr += '<option value="'+data[loop]["id"]+'">'+data[loop]["name"]+'</option>';
					}
					$('#union_buy_box_slots').html(mystr);
					$('#union_buyshop_box').show();
				},'json');
			});
			$('#set_buy_shop_box_close').click(function(){
				$('#set_buy_shop_box').fadeOut();
			});
			$('#set_sell_shop_box_close').click(function(){
				$('#set_sell_shop_box').fadeOut();
			});
			$('#set_sell_shop_button').click(function(){
				$('#set_sell_shop_box').fadeIn();
			});
			$('#union_sell_box_submit').click(function(){
					var arr = getItemList($('#union_sell_box_slots'));
					$.post("/market/new_sell/", {
						price: $('#union_sell_box_value').val(),
						item_id: arr
						},function(data) 
						{
							Alert(data);
							$('#union_sell_box_value').val('');
					},'json');
			});
			$('#union_buy_box_submit').click(function(){
					$.post("/market/new_buy/", {
						price: $('#union_buy_box_price').val(),
						item_id: $('#union_buy_box_slots').val(),
						level: $('#union_buy_box_lvl').val(),
						quantity: $('#union_buy_box_quantity').val(),
						must_complete: $('#union_buy_box_must_complete').val(),
						},function(data) 
						{
							Alert(data);
							$('#union_buy_box_price').val('');
							$('#union_buy_box_slots').val('');
							$('#union_buy_box_lvl').val('');
							$('#union_buy_box_quantity').val('');
							$('#union_buy_box_must_complete').val('');
					},'json');
			});
		// Research
			$('#doc_research').click(function(event){
				if(nowstate=="union")
					$('#union_research_box').fadeIn();
			});
			$('#union_research_box_close').click(function(event){
				$('#union_research_box').fadeOut();
			});
			$('#union_research_box').draggable({
					handle:'#union_research_box_title'
			});
			$('#union_research_box_submit').click(function(){
				var research_arr = getItemList($('#union_research_box_slots'));
				var research_catas = getItemList($('#union_research_box_catas_slots'));
				$.post("/user/research/",{
						items:research_arr,
						catas: research_catas
					},function(data){
						$('#union_research_box_slots').html('');
						$('#union_research_box_catas_slots').html('');
						if(data["is_success"])
						{
							LoadItem();
							$("#sub_menu2").fadeOut();
							submenu2 = "";
							Alert(data["message"]);
							for(var loop in data["formula"]["items"])
							{
								AlertItem(data["formula"]["items"][loop]);
							}
						}
						else
						{
							Alert(data["message"]);
						}
				},'json');
			});
	// Market
		// Market Box
			$('#market_button').click(function(event){
				$('#market_box').fadeIn("fast");
			});
			$('#bank_button').click(function(event){
				$('#bank_box').fadeIn("fast");
			});
			$('#patent_button').click(function(event){
				$('#patent_box').fadeIn("fast");
			});
			$('#bank_box').draggable({
					handle:'#bank_title'
			});
			$('#patent_box_close').click(function(event){
				$('#patent_box').fadeOut("fast");
			});
			$('#market_box_close').click(function(event){
				$('#market_box').fadeOut("fast");
			});
			$('#viewbuyshop').click(function(event){
				$('#main_shop .tab').removeClass("selected_tab");
				$('#viewbuyshop').addClass("selected_tab");
				$.post("/market/search_in_buy/", {},function(data) 
					{
						var content = '<table  class="market_table"><thead><td>ราคา</td><td>ระดับ</td>';
						content += '<td>ไอเท็ม</td><td>จำนวน</td><td>ผู้ตั้ง</td><td>เต็ม</td><td></td></thead><tbody>';
						for(var listobj in data)
						{
							content+='<tr>';
							content+='<td>'+data[listobj]['price']+'</td>';
							content+='<td>'+data[listobj]['level']+'</td>';
							content+='<td><img src="'+data[listobj]['icon_url']+'"width="16px" height="16px"/>'+data[listobj]['item_name']+'</td>';
							content+='<td>'+data[listobj]['quantity']+'</td>';
							content+='<td>'+data[listobj]['buyer']+'</td>';
							content+='<td>'+data[listobj]['must_complete']+'</td>';
							content+='<td>';
							if(data[listobj]['cancle_button'])
							{
								content+='<input type="button" id2="'+data[listobj]['id']+'" value="Cancel" class="cancel_buy"/>';
							}
							else
							{
								content+='<div id="player_buy_id'+data[listobj]['id']+'" class="item_list buy_box_slots" ></div><input type="button" id2="'+data[listobj]['id']+'" value="Sell" class="sell_buy"/>';
							}
							content+='</td>';
							content+='</tr>';
						}
						content+='</tbody></table>';
						$('.market_component').hide();
						$('#shop_content_viewbuy').show().html(content);
						$('.sell_buy').click(function(){
							var myarr = getItemList($('#player_buy_id'+$(this).attr('id2')));
							$.post("/market/player_sell/",{
								buy_id: $(this).attr('id2'),
								item_id: myarr
							}, function(data) 
							{
								Alert(data["message"]);
							},'json');
						});
						$('.cancel_buy').click(function(){
							$.post("/market/cancel_buy/",{
								buy_id: $(this).attr('id2')
							}, function(data) 
							{
								Alert(data["message"]);
							},'json');
						});
						SyncItem();
					},'json');
			});
			$('#setbuyshop').click(function(event){
				$('.market_component').hide();
				$('#main_shop .tab').removeClass("selected_tab");
				$('#setbuyshop').addClass("selected_tab");
				$.post("/market/can_buy/", {},function(data) 
					{
						var mystr='';
						for(var loop in data)
						{
							mystr += '<option value="'+data[loop]["id"]+'">'+data[loop]["name"]+'</option>';
						}
						$('#buy_box_slots').html(mystr);
						$('#buyshop_box').show();
					},'json');
			});
			$('#viewsellshop').click(function(event){
				$('#main_shop .tab').removeClass("selected_tab");
				$('#viewsellshop').addClass("selected_tab");
				$.post("/market/search_in_sell/",{}, function(data) 
					{
						var content = '<table class="market_table"><thead><td>ราคา</td><td>ระดับ</td>';
						content += '<td>ไอเท็ม</td><td>ความคงทน</td><td>ขนาด</td><td>ผู้ขาย</td><td></td></thead><tbody>';
						for(var listobj in data)
						{
							content+='<tr>';
							content+='<td>'+data[listobj]['price']+'</td>';
							content+='<td>'+data[listobj]['level']+'</td>';
							content+='<td><img src="'+data[listobj]['icon_url']+'"width="16px" height="16px"/>'+data[listobj]['item_name']+'</td>';
							if(data[listobj]['durability']==null)
								content+='<td>?</td>';
							else
								content+='<td>'+data[listobj]['durability']+'/'+data[listobj]['max_durability']+'</td>';
							content+='<td>'+data[listobj]['storage_cost']+'</td>';
							content+='<td>'+data[listobj]['seller']+'</td>';
							content+='<td>';
							if(data[listobj]['cancle_button'])
							{
								content+='<input type="button" id2="'+data[listobj]['id']+'" value="Cancel" class="cancel_sell"/>';
							}
							else
							{
								content+='<input type="button" id2="'+data[listobj]['id']+'" value="Buy" class="buy_sell"/>';
							}
							content+='</td>';
							content+='</tr>';
						}
						content+='</tbody></table>';
						$('#shop_content_viewsell').html(content);
						$('.market_component').hide();
						$('#shop_content_viewsell').show();
						$('.buy_sell').click(function(){
							$.post("/market/player_buy/",{
								sell_id: $(this).attr('id2')
							}, function(data) 
							{
								Alert(data["message"]);
							},'json');
						});
						$('.cancel_sell').click(function(){
							$.post("/market/cancel_sell/",{
								sell_id: $(this).attr('id2')
							}, function(data) 
							{
								Alert(data["message"]);
							},'json');
						});
					},'json');
			});
			$('#setsellshop').click(function(event){
				$('#main_shop .tab').removeClass("selected_tab");
				$('#setsellshop').addClass("selected_tab");
				$('.market_component').hide();
				$('#sellshop_box').show();
			});
			$('#buy_box_submit').click(function(){
					$.post("/market/new_buy/", {
						price: $('#buy_box_price').val(),
						item_id: $('#buy_box_slots').val(),
						level: $('#buy_box_lvl').val(),
						quantity: $('#buy_box_quantity').val(),
						must_complete: $('#buy_box_must_complete').val(),
						},function(data) 
						{
							Alert(data);
							$('#buy_box_price').val('');
							$('#buy_box_slots').val('');
							$('#buy_box_lvl').val('');
							$('#buy_box_quantity').val('');
							$('#buy_box_must_complete').val('');
					},'json');
			});
			$('#sell_box_submit').click(function(){
					var arr = getItemList($('#sell_box_slots'));
					$.post("/market/new_sell/", {
						price: $('#sell_box_value').val(),
						item_id: arr
						},function(data) 
						{
							Alert(data);
							$('#sell_box_value').val('');
					},'json');
			});
			$('#bank_box_submit').click(function(){
					var arr = getItemList($('#bank_box_slots'));
					$.post("/market/sell_bank/", {
						item_id: arr
					},function(data) {
						Alert(data["message"]);
					},'json');
			});
			$('#patent_title_setup').click(function(){
				$('.patent_component').hide();
				$('#patent_title .tab').removeClass("selected_tab");
				$('#patent_title_setup').addClass("selected_tab");
				$.getJSON("/market/can_sell_patent/", {},function(data) 
				{
					var mystr = '';
					for(var loop in data)
					{
						mystr += '<option value="'+data[loop]["patent_id"]+'">'+data[loop]["name"]+'</option>';
					}
					mystr += '';
					$('#patent_box_slots').html(mystr);
					$('#patent_box_setup_content').show();
				});
			});
			$('#patent_title_view').click(function(){
				$('#patent_title .tab').removeClass("selected_tab");
				$('#patent_title_view').addClass("selected_tab");
				$('.patent_component').hide();
				$.getJSON("/market/show_sell_patent/", {},function(data) 
				{
					var mystr = '<table class="market_table"><thead><tr><td>รายการ</td><td>ผู้ขาย</td><td>ราคา</td><td></td></tr></thead><tbody>';
					for(var loop in data)
					{
						mystr += '<td><span class="market_link_patent" id2="'+data[loop]["patent_id"]+'">'+data[loop]["name"]+'</span></td><td>'+data[loop]["seller"]+'</td><td>'+data[loop]["price"]+'</td><td>';
						if(data[loop]["cancle_button"])
						{
							mystr+='<input type="button"  id2="'+data[loop]["sell_id"]+'" class="patent_cancel_sell" value="Cancel"/>';
						}
						else
						{
							mystr+='<input type="button"  id2="'+data[loop]["sell_id"]+'" class="patent_buy" value="Buy"/>';
						}
						mystr += '</td></tr>';
					}
					mystr += '</tbody></table>';
					$('#patent_box_showall').html(mystr);
					$('#patent_box_title_content').show();
					$('.patent_cancel_sell').click(function(){
						$.post("/market/cancel_sell_patent/", {
							sell_patent_id: $(this).attr("id2")
						},function(data) 
						{
							Alert(data["message"]);
						},'json');
					});
					$('.patent_buy').click(function(){
						$.post("/market/buy_patent/", {
							sell_patent_id: $(this).attr("id2")
						},function(data) 
						{
							Alert(data["message"]);
						},'json');
					});
					$('.market_link_patent').click(function(){
						showPatent($(this).attr("id2"));
					});
				});
			});
			$('#patent_box_submit').click(function(){
				$.post("/market/new_sell_patent/", {
						patent_id: $('#patent_box_slots').val(),
						price: $('#patent_box_price').val()
				},function(data) 
				{
					Alert(data);
				},'json');
			});
			$('#bank_box_close').click(function(){
				$('#bank_box').fadeOut("fast");
			});
			$("#forest_button").click(function() {
					Havest();
			});	
			$("#mountain_button").click(function() {
					Havest();
			});	
			$("#river_button").click(function() {
					Havest();
			});
			$("#sea_button").click(function() {
					Havest();
			});
}
function Havest()
{
	$.post("/user/harvest/",{},function(data) 
		{
			if(data["is_success"])
			{
				AlertItem(data["item"]);
			}
			else
			{
				Alert(data["message"]);
			}
			LoadItem();
		},'json');
}
function check_research_lock()
{
	if(nowstate == "player")
	{
		$('#doc_research').addClass("doc_object_disable");
		$('#union_research_box').fadeOut();
	}
	else
	{
		$('#doc_research').removeClass("doc_object_disable");
	}
}