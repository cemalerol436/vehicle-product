



$(document).ready(function(){
//  "click" parameter is to get mouse click event into our codes.
        document.getElementById("addNewProduct").addEventListener("click",()=>{
            const name = document.getElementById("nameField").value
            const bracket = document.getElementById("bracketField").value
            const image = document.getElementById("imageField").value
            $.ajax({
                url: "/add-product",
                data: {
                    name,
                    image,
                    bracket
                },
                method: "post",
                success : function(response){
                    console.log(response);
                    alert("it is saved!")
                }
            });
        })
//vehicle
        document.getElementById("addNewVehicle").addEventListener("click", ()=>{
            const code = document.getElementById("codeField").value
            const model = document.getElementById("modelField").value
            const startyear = document.getElementById("startyearField").value
            const endyear = document.getElementById("endyearField").value
            const brand = document.getElementById("brandField").value
            $.ajax({
                url: "/add-vehicle",
                data: {
                    code,
                    model,
                    startyear,
                    endyear,
                    brand
                },
                method: "post",
                success : function(response){
                    if(response.success) {
                        alert("it is done!")
                    } else {
                        alert("Error")
                    }
                    console.log(response);
                }
            });
            });


        function loadBrands() {
            $.ajax({
                url: "/get-brands",
                async: false,
                success : setBrandOptions
            });

            function setBrandOptions(data) {


                const options = [
                '<option>Choose</option>'
                ];

                data.result.brands.forEach(item=>{

                    options.push('<option value="'+item.brand+'">'+item.brand+'</option>')

                });


                document.getElementById("brands-select").innerHTML = options.join('')

                console.log(data)
            }
        }

        function loadModels(brand) {
           $.ajax({
                url: "/get-models?brand="+brand,
                async: false,
                success : setModelOption
            });

           function setModelOption(data) {
                const options = [];
                data.data.forEach(item=>{
                    options.push('<option value="'+item+'">'+item.model + "  " + "(" + item.modelstart + " - " + item.modelend + ")" +'</option>')
                });
                document.getElementById("models-select").innerHTML = options.join('')
                console.log(data)
           }
        }


        loadBrands();

        document.getElementById("brands-select").addEventListener("change", (event)=>{
            const selectedValue = $(event.target).val();
            console.log(event);
            loadModels(selectedValue)


        })

});
