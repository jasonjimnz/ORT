$( document ).ready(function() {
    
	var url = window.location;
	
	$("#btnId").click(function(event){
        event.preventDefault();
        
        // Open Bootstrap Modal
        openModel();
        // get data from Server
        ajaxGet();
	})
	
    // Open Bootstrap Modal
    function openModel(){
    	$("#modalId").modal();
    }
    
    // DO GET
    function ajaxGet(orign, destination){
        $.ajax({
            type : "GET",
            url : url + "/destinations?origin="+ orign+"&destination=" +destination,
            success: function(data){
            	// fill data to Modal Body
                console.log(data);
                fillData(data);
            },
            error : function(e) {
            	fillData(null);
            }
        }); 
    }
    
    function fillData(data){
    	if(data!=null){
            $("#destinationid").text(data);
    	}else{
            $("#destinationid").text("Can Not Get Data from Server!");
    	}
    }

    $('#bntBuscar').on('click', function(event) {
        event.preventDefault(); // To prevent following the link (optional)
        console.log('Cargando los destinos encontrados en funcion del origen y destino, según el proposito activiades y alcance');
        ajaxGet($("#destinationid").val(), $("#destinationid").val());
    })
})