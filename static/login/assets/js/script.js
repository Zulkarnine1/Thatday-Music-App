$("#butonas").click(()=>{

    let pass1 = $("#formum2")[0].value
    let pass2 = $("#formum3")[0].value

    if(pass1===pass2){
    $("#form").submit()
    }else{
    alert("The passwords don't match, please try again.")
    }
    console.log({pass1,pass2})

})

$("#img3").change(function(){

		$("#fileImg3").attr("src",window.URL.createObjectURL(this.files[0]))

	})