

function addChart(){
	$.get("/requestChart",
		function(data,status){
			if(status){
				chartLoad();
			};
		}
	);
	chartLoad();
}

/*function chartLoad() {
		var chart = new CanvasJS.Chart("chartID",
		{
			theme: "theme3",
                        animationEnabled: true,
			title:{
				text: "Template chart",
				fontSize: 30
			},
			toolTip: {
				shared: true
			},			
			axisY: {
				title: "Count"
			},
			data: [ 
			{
				type: "column",	
				name: "Run",
				legendText: "Run",
              	color: "#2ECC71",
				showInLegend: true, 
				dataPoints:[
				{label: "Demo Test", y: 10},
				{label: "Chart Test", y: 11}
				]
			},
			{
				type: "column",	
				name: "Failed",
              	color: "#C0392B",
				legendText: "Failed",
				showInLegend: true,
				dataPoints:[
				{label: "Demo Test", y: 2},
				{label: "Chart Test", y: 1}
				]
			},
			{
				type: "column",	
				name: "Not Run",
				legendText: "Not Run",
              	color: "#7F8C8D",
				showInLegend: true,
				dataPoints:[
				{label: "Demo Test", y: 3},
				{label: "Chart Test", y: 3}
				]
			},
			{
				type: "column",	
				name: "Not Implemented",
				legendText: "Not Implemented",
              	color: "#3498DB",
				showInLegend: true,
				dataPoints:[
				{label: "Demo Test", y: 13},
				{label: "Chart Test", y: 13}
				]
			}
			],
          legend:{
            cursor:"pointer",
            itemclick: function(e){
              if (typeof(e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
              	e.dataSeries.visible = false;
              }
              else {
                e.dataSeries.visible = true;
              }
            	chart.render();
            }
          },
        });

chart.render();
}*/

$(function(){
	
});