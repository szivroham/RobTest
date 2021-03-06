var historyFormCount = 1;
var ids=[];

function histoyPage(){
    $("#nav-col-md-9").empty().append(designNavbar);
    $(".setup_buttons").hide();
    $(".col-md-12-set").empty().hide();
    $(".col-md-12-case").empty().hide();
    $(".col-md-12-execution").empty().show();
    $(".col-md-12-object").empty().hide();
    $(".setup").show();
    executionHistLoad("history");
    historyForm("first");
    ids=[];
}

function historyForm(loadingStatus){
    $.get("/HistoryForm",function(data,status){
        if(status){
            $("#nav-design-col-md-9").empty().append(data);
            if(loadingStatus=="first"){
                loadHistoryExe(loadingStatus);
            }
        }
    });
}

function executionHistLoad(mode){
    $.get("/historyExe/"+mode,function(data,status){
        if(status){
            $(".col-md-12-execution").empty().append(data);
        }
    });
}

function loadHistoryExe(exeStatus,executionId){
    if(exeStatus == "first")
        exeId=$($(".historyNav").children().children()[0]).attr('id');
    else
        exeId=executionId;
    $.get("/loadHistoryExe/"+exeId+"/"+exeStatus,function(data,status){
        if(status){
            if(exeStatus == "first" || exeStatus == "new"){
                $(".executionTable").empty().append(data);
                $(".executionInHistory").css("width","100%");
                historyFormCount = 1;
            }
            else{
                $(".executionTable").append(data);
                if(historyFormCount/3 == 1)
                    $(".executionInHistory").css("width","33%");
                if(historyFormCount/3 < 0.45)
                    $(".executionInHistory").css("width","100%");
                if(historyFormCount/3 > 0.6 && historyFormCount/3 < 0.9)
                    $(".executionInHistory").css("width","50%");
            }
        }
    });
}

function selectMoreExe(){
    if (historyFormCount != 3 || ids.indexOf($(event.target).attr('data-dbid')) > -1){
        historyFormCount++;
        id=$(event.target).attr('data-dbid');
        ids.push(id);
        $('#'+id+'.exeInHistory').css("background-color","#eee");
        loadHistoryExe("else",id);
    }
}

function closeHistoryForm(exeId){
    $(".executionInHistory[data-dbid='"+exeId+"']").remove();
    historyFormCount--;
    if(historyFormCount/3 < 0.45)
        $(".executionInHistory").css("width","100%");
    if(historyFormCount/3 > 0.6 && historyFormCount/3 < 0.9)
        $(".executionInHistory").css("width","50%");
    var index = ids.indexOf(exeId);
    if (index > -1) {
        ids.splice(index, 1);
    }
    $('#'+exeId+'.exeInHistory').css("background-color","transparent");
}

function toggleStatus(status){
    if(status=="RUN"){
        $(".success.resultRow").slideToggle();
    }
    if(status=="FAILED"){
        $(".danger.resultRow").slideToggle();
    }
    if(status=="SKIPPED"){
        $(".warning.resultRow").slideToggle();
    }
    if(status=="NOTRUN"){
        $(".active.resultRow").slideToggle();
    }
    if(status=="NOTIMP"){
        $(".info.resultRow").slideToggle();
    }
}

function historyReload(){
    exeid=$("select[data-selectorid='execution']").find(":selected").attr("data-dbid");
    loadHistoryExe("new",exeid);
}

function seeComment(ceId){
    $(".commentPop[data-dbid="+ceId+"]").popover({html:true});
    $(".commentPop[data-dbid="+ceId+"]").popover("toggle");
}

function seeAttached(ceId){
    $(".filePop[data-dbid="+ceId+"]").popover({html:true});
    $(".filePop[data-dbid="+ceId+"]").popover("toggle");
}