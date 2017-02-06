

$( document ).ready(function() {
    insertFirstDocInput();
    attachJsonXmlEvent();
    
    attachGetLogsEvents();
    attachTokenEvents();
});

function attachTokenEvents(){
	$("#createNewToken").click(function(){
		data={
			streamId:$("#streamIdLogs").val(),
			accessToken:$("#accessTokenLogs").val(),
			status:$("#statusToken").val()
		}
		url="/createToken?"+$.param(data);
		var win=window.open(url, '_blank');
		win.focus();
	});
	$("#validateNewToken").click(function(){
		data={
			streamId:$("#streamIdLogs").val(),
			accessToken:$("#accessTokenLogs").val()			
		}
		url="/validateToken?"+$.param(data);
		var win=window.open(url, '_blank');
		win.focus();
	});
}

function attachGetLogsEvents(){
	$("#getLogs").click(function(){
		data={
			streamId:$("#streamIdLogs").val(),
			accessToken:$("#accessTokenLogs").val()
		}
		url="http://localhost:8888/log?"+$.param(data);
		var win=window.open(url, '_blank');
		win.focus();
	});
}

var count=1;
function insertFirstDocInput(){
	$("#documentBox").append(formTemplate.replace(/~count~/g,count));	
	$("#addDocumentEvent").click(function(){
		count++;
		$("#documentBox").append(formTemplate.replace(/~count~/g,count));			
	});
}
var formTemplate='<div id="doc~count~">\
			<h5>Document ~count~</h5>\
			Doc ID: <input type="text" name="docId"/>\
  			<br/>\
  			Project ID: <input type="text" name="projectId"/>\
  			<br/>\
  			Search Set ID: <input type="text" name="searchSetId"/>\
  			<br/>\
  			Published Date: <input type="text" name="publishedDate"/>\
  			<br/>\
  			Author: <input type="text" name="author"/>\
  			<br/>\
  			Author ID: <input type="text" name="authorId"/>\
  			<br/>\
  			Title: <input type="text" name="title"/>\
  			<br/>\
  			Content: <input type="text" name="content"/>\
  			<br/>\
  			Gender: <input type="text" name="gender"/>\
  			<br/>\
  			Place: <input type="text" name="place"/>\
  			<br/>\
  			State: <input type="text" name="state"/>\
  			<br/>\
  			Parent Doc ID: <input type="text" name="parentDocId"/>\
  			<br/>\
  			Url: <input type="text" name="url"/>\
  			<br/>\
		</div>\
		<br/>';
		
function attachJsonXmlEvent(){
	$("#pushAsJson").click(function(){		
		pushAsJson(createMessageObject());
	});
	$("#pushAsXml").click(function(){		
		pushAsXml(createMessageObject());
	});
	
	
	$("#testPush100").click(function(){		
		var headerObj={
			streamId: $("#streamId").val(),
			accessToken: $("#accessToken").val()			
		}
		url="/push100?"+$.param(headerObj);
		alert(url);
		var win=window.open(url, '_blank');
		win.focus();
	});
	$("#testPush1000").click(function(){
		var headerObj={
				streamId: $("#streamId").val(),
				accessToken: $("#accessToken").val()			
			}
			url="/push1000?"+$.param(headerObj);
			alert(url);
			var win=window.open(url, '_blank');
			win.focus();
	});
}
function createMessageObject(){
	var headerObj={
		streamId: $("#streamId").val(),
		accessToken: $("#accessToken").val()			
	}
	var bodyObj={
			docs:[]
	}
	for(var i=0;i<count;i++){
		var doc={
			docId:$("#doc"+(i+1)+" input[name='docId']").val(),
			projectId:$("#doc"+(i+1)+" input[name='projectId']").val(),
			searchSetId:$("#doc"+(i+1)+" input[name='searchSetId']").val(),
			publishedDate:$("#doc"+(i+1)+" input[name='publishedDate']").val(),
			author:$("#doc"+(i+1)+" input[name='author']").val(),
			authorId:$("#doc"+(i+1)+" input[name='authorId']").val(),
			title:$("#doc"+(i+1)+" input[name='title']").val(),
			content:$("#doc"+(i+1)+" input[name='content']").val(),
			gender:$("#doc"+(i+1)+" input[name='gender']").val(),
			place:$("#doc"+(i+1)+" input[name='place']").val(),
			state:$("#doc"+(i+1)+" input[name='state']").val(),
			parentDocId:$("#doc"+(i+1)+" input[name='parentDocId']").val(),
			url:$("#doc"+(i+1)+" input[name='url']").val()
		}
		bodyObj.docs.push(doc);
	}
	var messages={
		Header:headerObj,
		Body:bodyObj
	}
	var messageFull={
		Message:messages
	}
	//alert(JSON.stringify(messageFull));
	return messageFull;
}
function pushAsJson(data){
	
	$.ajax({
		url: "/push",
		type: "POST",
		crossDomain: true,
		contentType: "application/json",		
		data: JSON.stringify(data),
		dataType: "text",
		success: function(result) {
		    alert('success');
		}
	});
}
function pushAsXml(data){
	$.ajax({
		url: "/push",
		type: "POST",
		contentType: "text/xml",		
		data: data,
		success: function(result) {
		    alert('success');
		}
	});
}