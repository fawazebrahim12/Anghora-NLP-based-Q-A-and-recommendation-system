<!DOCTYPE html>
<html>
<head>
<title>Anghora</title>
<link rel="shortcut icon" type="image/png" href="/favicon.png"/>
<?php 
session_start();
if(isset($_SESSION["username"])){
header("Location: index.php");
exit(); }
?>
<style type="text/css">
a:link { color: #1a0dab; text-decoration: none; font-family: arial,sans-serif}
a:visited { color: #609; text-decoration: none}
a:hover { color: #3366CC; text-decoration: underline; font-family: arial,sans-serif}
a:active { color:#609; text-decoration: none}
#right {float: right; margin-right: 75px}
.button {
  display: inline-block;
  padding: 7px 17px;
  font-size: 20px;
  cursor: pointer;
  text-align: center;	
  text-decoration: none;
  outline: none;
  color: #fff;
  background-color: #4CAF50;
  border: none;
  border-radius: 4px;
  box-shadow: 0 3px #999;
  position: relative;
  top: -123px;
  left: 370px;
}

.button:hover {background-color: #3e8e41}

.button:active {
  background-color: #3e8e41;
  box-shadow: 0 5px #666;
  transform: translateY(3px);
}

</style>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js"></script>
<script>

$(document).ready(function(){
$("#spin").hide();
$('#query').keypress(function(event) {
if (event.keyCode == 13) {
$("#spin").show();
	var notEmpty = $('#query').val();
	if(notEmpty){
	$( "div" ).empty();
	$("div").removeAttr("style");

	$q = $("#query").val();
	$('div').css({'width':'600px',
	'box-shadow':'0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)', 'background-color':'white',
	'margin-left':'100px'
	});
	$("#right").css({'width':'500px','background-color':'transparent'});
        $.getJSON("http://localhost:5000/",{"q":$q,"id":'-1'}, function(result){
            $("#spin").hide();
            $.each(result, function(i, field){
			if(i=="correction")
			{if(field){
			var $div = $('<div id="correctionText">');
				$("#correction").append($div);
				$("#correctionText").append('Showing results for <span style="font-style: italic;">'+ field + '</span><br />').css({'color':'grey','font-size':'20px'});
				$q = field;; 
				$('#correction').css({'padding':'20px','margin-bottom':'10px'});       
			}
			}
			if(i=="distMatrix")
			{
			if(field){
				var $div = $('<div id="distMatrixtxt">');
				$("#distMatrix").append($div);
				$("#distMatrixtxt").append('Origin : ' + field.origin + '<br />Destination : ' + field.destination + '<br />Distance : ' + field.distance + '<br />Duration : ' + field.duration).css({'color':'#0000000','font-size':'20px'});
				$('#distMatrix').css({'padding':'20px','margin-bottom':'10px'});  
			}
			}
			if(i=="wolf_result")
			{
			if(field){
				var $div = $('<div id="wolftxt">');
				$("#wolfram").append($div);
				$("#wolftxt").append('Wolfram Answers <br />').css({'color':'grey','font-size':'20px','line-height':'2.5'});
				$.each(field, function(key, value){
					$("#wolfram").append('<span style="font-size: 20px;color:#ff4411">' + key + '</span><br />' + value + '<br /><br />');
					});
				$('#wolfram').css({'padding':'20px','margin-bottom':'10px'});  
			}
			}
			if(i=="web_result")
			{if(field){
			var $div = $('<div id="webtxt">');
				$("#web").append($div);
				$("#webtxt").append('Web Results <br /><br />').css({'color':'grey','font-size':'20px'});
				$.each(field, function(key, value){
					$("#web").append('<a href='+ value.Url + ' ><span style="font-size: 18px;">' + value.Title + '</span></a>'+ '<br /><span style="font-size: 14px; color:#006621; line-height:16px">' + value.Url + '</span><br /><span style="color:#545454;font-family:arial,sans-serif;line-height:16px">' + value.Description + '</span><br /> <br />');
					});
				$('#web').css({'padding':'20px','margin-bottom':'10px'});       
			}
			}
			if(i=="rs_result")
			{
			if(field){
				var $container = $("#rs");
				var $div = $('<div id="rstxt">');
				$("#rs").append($div);
				$("#rstxt").append('Related searches <br />').css({'color':'grey','font-size':'20px','line-height':'2.5'});
				$.each(field, function(key, value){
					var item = '<div id="valtxt ' + $container.children().length + 1 + '"><a href="#">' + value.Title + '</a></div>';
					var $item = $(item).click(function() {
            $("#query").val(value.Title);
			$('#query').trigger({type: 'keypress', which: 13, keyCode: 13});
        });
					$container.append($item).css('line-height','1.5');
					
					});
				$('#rs').css('padding','20px');  
			}
			}
			
			if(i=="ai_result")
			{
			if(field){
			var $div = $('<div id="ai">');
			$("#right").append($div);
			$("#ai").css('background-color','white');
				var $div = $('<div id="aitxt">');
				$("#ai").append($div);
				$("#aitxt").append(field).css({'color':'#0000000','font-size':'20px',"font-style":"italic"});
				$('#ai').css({'padding':'20px','margin-bottom':'10px'});  
			}
			}
			if(i=="kg_result")
			{if(field){
			var $div = $('<div id="kg">');
			$("#right").append($div);
			$("#kg").css('background-color','white');
				$.each(field, function(key, value){
					var img = $('<img id="image_portrait" width="186px" height="185px" style="float: right">');
					if(value.image){
					img.attr("src", value.image);
					img.appendTo('#kg');
					}
					$("#kg").append( '<span style="font-size: 30px;">' + value.name + '</span><br /><span style="font-size: 13px; color:#777; line-height:2">' + value.description +'</span><br /><br /><span style="padding-right:10px;">' + value.detailedDescription + '<br /><br />');

					});
					
				$('#kg').css({'padding':'20px','margin-bottom':'10px'});       
			}
			}
			if(i=="alchemy_result")
			{
			if(field){
				var $div = $('<div id="alchemytxt">');
				$("#alchemy").append($div);
				$("#alchemytxt").append("Category : " + field).css({'color':'#0000000','font-size':'20px',"font-style":"italic"});
				$('#alchemy').css({'padding':'20px','margin-bottom':'10px'});  
			}
			}
            });
			
        });
		}
    }});
	
});
</script>
</head>
<body style="background-color:white; background-image:linear-gradient(red,#f06d06);  background-repeat: no-repeat;">
<p style = "color:white; font-size:25px" align = "center">Ask Something like:</p>
<MARQUEE onmouseover="this.stop();"
      onmouseout="this.start();" DIRECTION=UP SCROLLAMOUNT=4 BGCOLOR="" height ="125px" align="center"><p ALIGN=CENTER> <FONT SIZE=5 COLOR="white">
Who was the president of USA in 1920?<br /><br />
What is the calorie of an orange?<br /><br />
What is the atomic number of Boron?<br /><br />
When was Titanic movie released?<br /><br />
What is the distance between Mumbai and Pune?<br /><br />
Will it rain tommorow in Goa?<br /><br />
What are the stocks for Twitter?<br /><br />
How much is 1000USD in Indian rupees?
</FONT> </p></MARQUEE> 
 <p  style = "text-align:center;font-size:50px; color:white;margin-bottom:30px;"> ANGHORA </p>

<input type="text" id="query"  style=" width:400px; position:relative;
	padding:8px 15px;
                margin-left:33%; margin-bottom:40px;
                border:2px solid #f6f6f6;
	font-family: Tahoma, sans-serif;" placeholder="Ask Anything!!!">
				 <button class="button"><a href="login.php">Login</a></button>
				 
<img src="ajax.gif" id="spin" style="position: relative; top: 125px; left: -415px"/>
<div id='correction'></div>
<!-- <div id='recommend' ></div> -->
<!-- <div id='ai' ></div> -->
<div id='right' ></div>
<!-- <div id='kg' ></div> -->
<div id='alchemy' ></div>
<div id='distMatrix'></div>
<div id='wolfram'></div>
<div id='web'></div>
<div id='rs'></div>


</body>
</html>