function requestSet(){
    $.get("/set_page",
		function(data,status){
			if(status){
				$(".col-md-12-set").empty().append(data);
			};
		}
	);
}

function SetSetup(mode){
	$("#mainHeader").css('margin-bottom','5px');
    $(".setup_buttons").hide();
    $.get("/setForm",
		function(data,status){
			if(status){
				$(".divContainer").empty().append(data);
			};
		}
	);
    if(mode != "false"){
        $(".col-md-12-object").empty().hide();
        $(".buttonSetup").empty().append(setBtn);
        $(".col-md-12-execution").empty().hide();
        requestSet();
    }
}

function saveSet(){
    var sendData=$("input[type=text]").map(function(i,o){return o.name+"="+o.value}).toArray().join("&") + "&"+$("input[type=date]").map(function(i,o){return o.name+"="+o.value}).toArray().join("&")+"&"+$("input:checkbox:checked").map(function(){return "areaBox="+$(this).attr('data-dbid')}).toArray().join("&")+"&ID="+$(".incCases a").map(function(index,node){return node.dataset.dbid;}).toArray().join("&ID=");
	$.post("/save_set", sendData,
		function(data,status){
			if(status){
                if(document.getElementById("fileUploadSet").files.length > 0){
                    updateFilesToSet(data);
                }
				requestSet();
                loadSet(data,"loadSet");
			};
		}
	);
}

function updateSet(setId){
    var sendData=$("input[type=text]").map(function(i,o){return o.name+"="+o.value}).toArray().join("&") + "&"+$("input[type=date]").map(function(i,o){return o.name+"="+o.value}).toArray().join("&")+"&"+$("input:checkbox:checked").map(function(){return "areaBox="+$(this).attr('data-dbid')}).toArray().join("&")+"&ID="+$(".incCases a").map(function(index,node){return node.dataset.dbid;}).toArray().join("&ID=")+"&setId=";
    sendData+=setId;
	$.post("/updateSet", sendData,
		function(data,status){
			if(status){
				requestSet();
                loadSet(data,"loadSet");
			};
		}
	);
}

function loadSet(setId,mode){
	$.get("/load_set/"+setId+"/"+mode,
		function(data,status){
			if(status){
				if(mode == "exeCasesBySet"){return data;}
				else{
					$(".divContainer").empty().append(data);
				}
			};
		}
	);
}

function deleteSet(setId){
	$.get("/deleteSet/"+setId,
		function(data,status){
			if(status){
				SetSetup("false");
				$(".buttonSetup").empty().append(setBtn);
				$(".divContainer").empty().append(SetForm);
			};
		}
	);
}

function newSet(){
    if($(".setForm").attr("data-dbid")=="newSet"){
        $($(".incCases")[0]).attr('ondrop','drop(event)');
        $($(".incCases")[0]).attr('ondragover','allowDrop(event)');
        $("input[type=checkBox]").removeAttr("disabled");
        $("input[type=text][name=name]").removeAttr('readonly');
        $("input[type=text][name=priority]").removeAttr('readonly');
    }
    else{
        SetSetup("false");
    }
	$(".newSet").empty().append(newSetDis);
	$(".saveSet").empty().append(saveSetEn);
    $("body").on('drop',dropRemove);
    //$("body").on('dragstart',drag);
    $("body").on('dragover',allowDrop);
}

function setHideShow(){
    if($(".setHideShow").attr("data-mode")=="show"){
        $($(".panel-set")[0]).hide();
        $(".col-md-12-set")[0].style.height="62px";
        $(".setHideShow").attr("data-mode",'hide');
        $(".setHideShow").empty().append("<i class='fa fa-chevron-down'></i>");
        if($(".caseHideShow").attr("data-mode")=="show"){
            $(".col-md-12-case")[0].style.height="calc(100% - 62px)";
        }
        if($(".exeHideShow").attr("data-mode")=="show"){
            $(".col-md-12-execution")[0].style.height="calc(100% - 62px)";
        }
        
    }
    else{
        if($(".caseHideShow").attr("data-mode")=="show"){
            $(".col-md-12-set")[0].style.height="50%";
            $(".col-md-12-case")[0].style.height="50%";
        }
        if( $(".exeHideShow").attr("data-mode")=="show"){
            $(".col-md-12-set")[0].style.height="50%";
            $(".col-md-12-execution")[0].style.height="50%";
        }
        if($(".caseHideShow")[0]==undefined && $(".exeHideShow")[0]==undefined){
            $(".col-md-12-set")[0].style.height="100%";
        }
        if($(".caseHideShow").attr("data-mode")=="hide" || $(".exeHideShow").attr("data-mode")=="hide"){
            $(".col-md-12-set")[0].style.height="calc(100% - 62px)";
        }
        $($(".panel-set")[0]).show();
        $(".setHideShow").attr("data-mode",'show');
        $(".setHideShow").empty().append("<i class='fa fa-chevron-up'></i>");
    }
}

function setSearch(){
    for (i=0; i < $(".set").length;i++){
        var search=$("input[name=setSearch]").val();
        if($(".set")[i].innerHTML.toLowerCase().indexOf(search.toLowerCase()) >= 0){
            var classFilt= $(".set")[i].id;
            $("[data-dbid=set"+classFilt.toString()+"]").show();
        }
        else{
           var classFilt= $(".set")[i].id;
            $("[data-dbid=set"+classFilt.toString()+"]").hide();
        }
        if (search == ""){
            for (i=0; i < $(".set").length;i++){
                var classFilt= $(".set")[i].id;
                $("[data-dbid=set"+classFilt.toString()+"]").show();
            }
        }
    }
}

function toggleSetFileCont(){
    if($("#newSet").attr('class')=="btn btn-default btn-sm disabled" || $($(".setForm")[0]).attr('data-dbid') != "newSet")
        $(".uploadContent").slideToggle();
}

function addSetToExe(ev){
    if($(".incExeCases") != [] && $(".btn.btn-default.btn-sm.disabled#saveExe") != []){
        draggedElement=ev.target.parentElement;
        if(draggedElement.className == "set"){
			$.get("/load_set/"+draggedElement.dataset.dbid+"/"+"exeCasesBySet",
				function(data,status){
					if(status){
						draggedElement=draggedElement.cloneNode(true);
                        $(".incExeCases")[0].innerHTML+=data;
					};
				}
			);
		}
		else{
			$(".incExeCases").appendChild(draggedElement.cloneNode(true));
		}
    }
    else{
        return;
    }
}

$(function(){
	$("body").on("click","a",function(event) {
		if( $(event.target).attr('class') == "set"  && actualModul == "set"){
			loadSet($(event.target).attr('data-dbid'), "loadSet");
            $(".newSet").empty().append(newSetDis);
	        $(".saveSet").empty().append(saveSetEn);
			//alert(event.target.id + $(event.target).attr('class'));
		}
		if( event.target.id == "saveSet"){
            if($(".setForm").attr('data-dbid')=="newSet"){
				saveSet();
			}
			else{
				updateSet($(".setForm").attr('data-dbid'));
			}
		}
		if( event.target.id == "newSet"){
			newSet();
		}
		if( event.target.id == "cancelSet"){
			SetSetup("false");
			$(".buttonSetup").empty().append(setBtn);
		}
		if( $(event.target).attr('name')=="deleteset" ){
			deleteSet(event.target.id);
            requestSet();
		}
		if( $(event.target).attr('name')=="editSet" ){
			loadSet($(event.target).attr('id'),"editSet");
            $("body").on('drop',dropRemove);
            //$("body").on('dragstart',drag);
            $("body").on('dragover',allowDrop);
		}
	});
});