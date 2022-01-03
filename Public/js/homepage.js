

//  Homepage
$(document).ready(function(){

	$.ajax({  
		url: "/get-brands",
		async: false,
		success : function(response){
			loadHeaderData(response)
		}
	});

	function loadHeaderData(data) {


        const options = [];

        data.data.forEach(item=>{

            options.push('<option value="'+item+'">'+item+'</option>')

        });


        document.getElementById("brands-select").innerHTML = options.join('')

		console.log(data)
	}

	
});
//  Homepage
$(document).ready(function(){

	$.ajax({
		url: "/get-models?brand=AUDI aa",
		async: false,
		success : function(response){
			loadHeaderData(response)
		}
	});

	function loadHeaderData(data) {


        const options = [];

        data.data.forEach(item=>{

            options.push('<option value="'+item+'">'+item.model + "  " + "(" + item.modelstart + " - " + item.modelend + ")" +'</option>')

        });


        document.getElementById("models-select").innerHTML = options.join('')

		console.log(data)
	}


});


