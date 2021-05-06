
function cities(input){
	if(input=="Francia")
	{
		var city = new XMLHttpRequest();
		city.onreadystatechange = function(){
			if(this.readyState == 4 && this.status == 200)
			{
				//document.getElementById("cities").innerHTML = this.responseText;
				var txt = this.responseText;
				txt = txt.split('\n');
				//alert(txt);
				var x = document.getElementById("mySelect");
				while(x.firstChild){ //primero vacío 
					x.removeChild(x.firstChild);
				}
				for(var i=0;i<txt.length;i++)
				{
					if(txt[i]){
						var option = document.createElement("option");
						option.text = txt[i];
						x.add(option);
					}
				}
			}
		};
		city.open("GET", "cities/Francia.txt", true);
		city.send();
	}
	if(input=="Dinamarca")
	{
		var city = new XMLHttpRequest();
		city.onreadystatechange = function(){
			if(this.readyState == 4 && this.status == 200)
			{
				//document.getElementById("cities").innerHTML = this.responseText;
				var txt = this.responseText;
				txt = txt.split('\n');
				//alert(txt);
				var x = document.getElementById("mySelect");
				while(x.firstChild){
					x.removeChild(x.firstChild);
				}
				for(var i=0;i<txt.length;i++)
				{
					if(txt[i]){
						var option = document.createElement("option");
						option.text = txt[i];
						x.add(option);
					}
				}
			}
		};
		city.open("GET", "cities/Dinamarca.txt", true);
		city.send();
	}
	if(input=="Holanda")
	{
		var city = new XMLHttpRequest();
		city.onreadystatechange = function(){
			if(this.readyState == 4 && this.status == 200)
			{
				//document.getElementById("cities").innerHTML = this.responseText;
				var txt = this.responseText;
				txt = txt.split('\n');
				//alert(txt);
				var x = document.getElementById("mySelect");
				while(x.firstChild){
					x.removeChild(x.firstChild);
				}
				for(var i=0;i<txt.length;i++)
				{
					if(txt[i]){
						var option = document.createElement("option");
						option.text = txt[i];
						x.add(option);
					}
				}
			}
		};
		city.open("GET", "cities/Holanda.txt", true);
		city.send();
	}
	if(input=="Italia")
	{
		var city = new XMLHttpRequest();
		city.onreadystatechange = function(){
			if(this.readyState == 4 && this.status == 200)
			{
				//document.getElementById("cities").innerHTML = this.responseText;
				var txt = this.responseText;
				txt = txt.split('\n');
				//alert(txt);
				var x = document.getElementById("mySelect");
				while(x.firstChild){
					x.removeChild(x.firstChild);
				}
				for(var i=0;i<txt.length;i++)
				{
					if(txt[i]){
						var option = document.createElement("option");
						option.text = txt[i];
						x.add(option);
					}
				}
			}
		};
		city.open("GET", "cities/Italia.txt", true);
		city.send();
	}
}

function functionDatos(input) {
	//alert('Esta funcion no esta implementada')
	var passw = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}$/;
	
	if(input.value.match(passw)) 
	{ 
		//alert('a')
		var seg = "";
		if(input.value.length < 7)
			seg = "aceptable";
		else if(input.value.length >= 7 && input.value.length <= 12)
			seg = "media";
		else if(input.value.length > 12)
			seg = "alta";
		alert('Contrase\u00F1a v\u00E1lida, nivel de seguridad: ' + seg);
		return true;
	}
	else
	{ 
		var minuscula = /[a-z]/g;
		var mayuscula = /[A-Z]/g;
		var num = /[0-9]/g;
		var letra = "";
		var Letra = "";
		var numero = "";
		var caracteres = "";
  		if(!input.value.match(minuscula)) 
  			//alert('Debe contener una letra minuscula' + letra)
  			letra = " una letra min\u00FAscula,";
  		if(!input.value.match(mayuscula))
  			//alert('Debe contener una letra mayuscula')
  			Letra = " una letra may\u00FAscula,";
  		if(!input.value.match(num))
  			//alert('Debe contener al menos un numero')
  			numero = " un n\u00FAmero,";
  		if(input.value.length < 6)
  			//alert('Debe contener al menos 6 caracteres')
  			caracteres = " 6 caracteres.";
  		alert('Le falta al menos:' + letra + Letra + numero + caracteres);
		//alert('La contrasena debe contener al menos 6 caracteres, un numero, una letra mayuscula y una minuscula')
		return false;
	}
}



function comparar(input) {
	/*var op = document.getElementById("country");
    for (var i = 0; i < op.options.length; i++)
    {
    	if ( op.options[i].value.toUpperCase() == input.toUpperCase()) 
        	return true;
    }
    alert('Pais erroneo');
    return false; */
    var e1 = document.getElementById("country").options.namedItem("europa1").value;
	var e2 = document.getElementById("country").options.namedItem("europa2").value;
	var e3 = document.getElementById("country").options.namedItem("europa3").value;
	var e4 = document.getElementById("country").options.namedItem("europa4").value;
	//document.getElementById("demo").innerHTML = e2;
	var op = [];
	op.push(e1);
	op.push(e2);
	op.push(e3);
	op.push(e4);
	//document.getElementById("demo").innerHTML = op[2];
	for (var i = 0; i < op.length; i++)
    {
    	if ( op[i].toUpperCase() == input.toUpperCase()) 
        	return true;
    }
    alert('Pais erroneo');
    return false; 
	
		//console.log(optionVals);
  		//document.getElementById("demo").innerHTML = x;
    
    
     //&& op.options[i].namedItem().value == "europa"
}



function Temperatura() {
	var elx = parseInt(document.getElementById("a").value);
	var ely = parseInt(document.getElementById("b").value);
	var elz = document.getElementById("c");

	elz.value = elx - ely;
	//document.getElementById("c").innerHTML.value = elx.value + ely.value;
	if(elz.value > 26 || 
		elz.value < 22)
			{
				elz.style.color = 'red';
				alert('Valor de la temperatura fuera de rango, debe estar entre 22 y 26 grados')
				
			}
		else
			elz.style.color = '#2F4F4F';
		
}

function seguridad(){
	var elx = document.getElementById("pwd");
	var passw = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{6,}$/;
	
	if(elx.value.match(passw)) 
		elx.style.color = 'green';
	else
		elx.style.color = 'red';
}

function maps(){
	//var valido = /[^\d]+,[^\d]*$/;
	//var valido = /\d{2}\.\d{6}/gim; 
	//var valido = /^\d+,\d+$/; //este solo acepta enteros,enteros
	var valido = /^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$/;
	var a = document.getElementById('url');
	var elx = document.getElementById("gps1");
	var url = "http://maps.google.com/maps?q=";
	if(elx.value.match(valido))
	{
		alert('Coordenadas v\u00E1lidas, creando enlace...')
		a.href = url + elx.value;
		if(a.style.display === "none")
			a.style.display = "block";
	}
	else
	{
		alert('Coordenadas inv\u00E1lidas')
		if(a.style.display === "block")
			a.style.display = "none";
	}
}