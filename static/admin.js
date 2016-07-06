var rowId;
function userSetup(){
    document.getElementById("col-md-9").style.width = '70%';
    $(".setup_buttons").hide();
    $(".col-md-12-set").empty();
    $(".col-md-12-case").empty();
    $(".col-md-12-execution").empty();
    $(".setup").show();
    requestAdmin();
}

function requestAdmin(){
    $("#mainHeader").css('margin-bottom','0px');
    $(".setup").css('padding-left','0px');
    $.get("/getUsers",
         function(data,status){
            if(status){
                $(".col-md-9").empty().append(data);
            } 
    });
    $.get("/getAdminNav",
         function(data,status){
            $(".col-md-12-set").empty().append(data);
    });
}

function selectRow(){
    if(rowId == ""){
        rowId=$(event.target).attr('id');
        $("[data-row='editRow']#"+$(event.target).attr('id')).attr('class','info');
        $(event.target).css("color","black");
    }
    else{
        if(rowId != $(event.target).attr('id')){
            $("[data-row='editRow']#"+rowId).removeAttr('class');
            $("#"+rowId+".rowLink").css("color","#eee");
            $("[data-row='editRow']#"+$(event.target).attr('id')).attr('class','info');
            $(event.target).css("color","black");
            rowId=$(event.target).attr('id');
        }
        else{
            $("[data-row='editRow']#"+rowId).removeAttr('class');
            $("#"+rowId+".rowLink").css("color","#eee");
            rowId="";
        }
    }
}

function activateUser(){
    if(rowId != ""){
        var sendData="userId="+rowId+"&status=active";
        $.post("/userActive",sendData,function(data,status){
            if(status){
                $(".userStatus[data-dbid="+rowId+"]").empty().append(data);
                $(".userStatus[data-dbid="+rowId+"]").css("color","#5cb85c");
            }
        });
    }
}

function deactivateUser(){
    if(rowId != ""){
        var sendData="userId="+rowId+"&status=inactive";
        $.post("/userActive",sendData,function(data,status){
            if(status){
                $(".userStatus[data-dbid="+rowId+"]").empty().append(data);
                $(".userStatus[data-dbid="+rowId+"]").css("color","#d9534f");
            }
        });
    }
}

function saveNewPw(){
    var id = $(event.target).attr('id');
    var sendData="oldPw="+$("input[name=oldPw][id="+id+"]").val()+"&newPw="+$("input[name=newPw][id="+id+"]").val();
    sendData+="&id="+id;
    $.post("/savePassword",sendData,
          function(data,status){
            if(data=="false"){
                alert("error");
            }
            else{
                alert("success");
                $("input[name=oldPw][id="+id+"]").val('');
                $("input[name=newPw][id="+id+"]").val('');
                $("#"+id+".slideMoving").slideUp();
            }
    });
}

function saveUser(){
	if($("input[type='text'][data-newuser='userName']").val()=="" || $("input[type='password'][data-newuser='userPassword']").val()==""){
        $(".userErrorMessage").tooltip({title: "Missing value!"});
        $(".userErrorMessage").tooltip('show');
    }
    else{
        $(".userErrorMessage").tooltip('hide');
        var sendData="userName="+$("input[type='text'][data-newuser='userName']").val()+"&password="+$("input[type='password'][data-newuser='userPassword']").val()+"&roleId=";
        sendData=sendData+$(".newRoleSelector").find(':selected').attr('data-roleid')+"&projectId="+$(".projectSelector").find(':selected').attr('data-dbid');
        $.post("/saveUser",sendData,function(data,status){
            if(status){
                requestAdmin();
            }
        });
    }
}

function addUser(){
    $(".newUserForm").slideToggle();
}

function confirmUserDeletion(){
    id=event.target.id;
	$("#"+id+".userDeletion").popover({content: "<p style='color:black;'>Are you sure to delete this user?</p><button type='button' class='btn btn-danger btn-xs' data-dbid='"+id+"' onclick='deleteUser()' style='width:50%;'>Delete</button><button type='button' class='btn btn-default btn-xs' onclick='cancelUser("+id+")' style='width:50%;'>Cancel</button>",html:true});
    $("#"+id+".userDeletion").popover('show');
}
function cancelUser(id){
    $("#"+id+".userDeletion").popover('hide');
}
function deleteUser(){
    var sendData="userId="+$(event.target).attr('data-dbid');
    $.post("/deleteUser",sendData,function(data,status){
       if(status){
           $("#"+id+".userDeletion").popover('hide');
           requestAdmin();
       } 
    });
}

function roleChange(){
    var userId=$(event.target).attr("data-selectorid");
    var sendData="userId="+userId+"&roleId="+$(".roleSelector[data-selectorid="+userId+"]").find(":selected").attr('data-roleid');
    $.post("/updateUserRole", sendData,
		function(data,status){
			     if(data=="error"){
                     alert("error");
                 }
			}
	);
}


$(function(){
        if($(event.target).attr('name')=="edit"){
			ID=event.target.id;
			$("#"+ID+".slideMoving").slideToggle();
		}
})