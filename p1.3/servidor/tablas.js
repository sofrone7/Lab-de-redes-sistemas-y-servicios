
$(document).ready(function(){

	$("table td").css({
		'border': '2px solid white',
		'text-align': 'left',
		'width': '400px',
		'padding': '20px'
	});
	
	
	$("table").css({
		'margin-left': 'auto',
		'margin-right': 'auto',
		'background-color': '#BDB76B',
		'border-collapse': 'collapse',
		'width': '70%'
	});
	$("th").css('background-color', 'gray');
	$('td').hover( function() {
	    $(this).parent().children().css("background-color", "#DDD");
	    $(this).css("background-color", "#FAFAD2")
	});
	$('tr').mouseleave( function() {
	    $(this).children('td').css("background-color", "#BDB76B");
	});

	$.getJSON("json/tablas.json", function(data){
		var estacion ='';
		$.each(data, function(key, value){
			estacion += '<tr>';
			estacion += '<td>'+value.ciudad+'</td>';
			estacion += '<td>'+value.temperatura+'</td>';
			estacion += '<td>'+value.humedad+'</td>';
			estacion += '<td>'+value.ruido+'</td>';
			estacion += '<td>'+value.luz+'</td>';
			estacion += '<td>'+value.iluminacion+'</td>';
			estacion += '</tr>';
		});
		$('#table3').append(estacion);
	});

	$('#T1').on('click',function(){
		$('.btActive').css('background-color', 'white');
		$(this).css('background-color', '#DDD');
		var btActive = $('.btActive');
		var btT1 = $(this);
		btActive.removeClass('btActive');
		btT1.addClass('btActive');
		var tableActiva = $('.active');
		var table1 = $('#table1');
		tableActiva.removeClass('active').css('z-index', -10);
		table1.addClass('active').css('z-index', 10);
	});

	$('#T2').on('click',function(){
		$('.btActive').css('background-color', 'white');
		$(this).css('background-color', '#DDD');
		var btActive = $('.btActive');
		var btT2 = $(this);
		btActive.removeClass('btActive');
		btT2.addClass('btActive');
		var tableActiva = $('.active');
		var table2 = $('#table2');
		tableActiva.removeClass('active').css('z-index', -10);
		table2.addClass('active').css('z-index', 10);
	});

	$('#T2').on('click',function(){
		$("table td").css({
		'border': '2px solid white',
		'text-align': 'left',
		'width': '400px',
		'padding': '20px'
		});
		$("table").css({
			'margin-left': 'auto',
			'margin-right': 'auto',
			'background-color': '#BDB76B',
			'border-collapse': 'collapse',
			'width': '70%'
		});
		$("th").css('background-color', 'gray');
		$('td').hover( function() {
		    $(this).parent().children().css("background-color", "#DDD");
		    $(this).css("background-color", "#FAFAD2")
		});
		$('tr').mouseleave( function() {
		    $(this).children('td').css("background-color", "#BDB76B");
		});
	});

	$('#T3').on('click',function(){
		$("table td").css({
		'border': '2px solid white',
		'text-align': 'left',
		'width': '400px',
		'padding': '20px'
		});
		$("table").css({
			'margin-left': 'auto',
			'margin-right': 'auto',
			'background-color': '#BDB76B',
			'border-collapse': 'collapse',
			'width': '70%'
		});
		$("th").css('background-color', 'gray');
		$('td').hover( function() {
		    $(this).parent().children().css("background-color", "#DDD");
		    $(this).css("background-color", "#FAFAD2")
		});
		$('tr').mouseleave( function() {
		    $(this).children('td').css("background-color", "#BDB76B");
		});
	});

	$('#T3').on('click',function(){
		$('.btActive').css('background-color', 'white');
		$(this).css('background-color', '#DDD');
		var btActive = $('.btActive');
		var btT3 = $(this);
		btActive.removeClass('btActive');
		btT3.addClass('btActive');
		var tableActiva = $('.active');
		var table3 = $('#table3');
		tableActiva.removeClass('active').css('z-index', -10);
		table3.addClass('active').css('z-index', 10);
	});

	$('#T4').on('click',function(){
		$('.btActive').css('background-color', 'white');
		$(this).css('background-color', '#DDD');
		var btActive = $('.btActive');
		var btT4 = $(this);
		btActive.removeClass('btActive');
		btT4.addClass('btActive');
		var tableActiva = $('.active');
		var table4 = $('#table4');
		tableActiva.removeClass('active').css('z-index', -10);
		table4.addClass('active').css('z-index', 10);
	});
});


