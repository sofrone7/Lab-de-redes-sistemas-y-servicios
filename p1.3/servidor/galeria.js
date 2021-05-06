$(document).ready(function(){
	$('.next').on('click',function(){
		//$('.active').css('opacity', '0.5');
		var imgActiva = $('.active');
		var iNext = imgActiva.next();
		if(iNext.length == 0){
			var imgNext = $('img[alt="Barcelona"]');
		}
		else
			var imgNext = imgActiva.next();
		//var captionText = $('#caption');
		if(imgNext.length){
			imgActiva.removeClass('active').css('z-index',-10);
			imgNext.addClass('active').css('z-index',10);
			var newActiva = $('.active');
			$(".caption-container").text(newActiva.attr('alt'));
			//$('.active').css('opacity', '1');
		}
	});

	$('.prev').on('click',function(){
		//$('.active').css('opacity', '0.5');
		var imgActiva = $('.active');
		var iPrev = imgActiva.prev();
		if(iPrev.length == 0){
			var imgPrev = $('img[alt="Alicante"]');
		}
		else
			var imgPrev = imgActiva.prev();
		if(imgPrev.length){
			imgActiva.removeClass('active').css('z-index',-10);
			imgPrev.addClass('active').css('z-index',10);
			var newActiva = $('.active');
			$(".caption-container").text(newActiva.attr('alt'));
			//$('.active').css('opacity', '1');
		}
	});

	$('.demoCursor').mouseover( function() {
	    var newActiva = $(this);
			$(".caption-container2").text(newActiva.attr('alt'));
	});

	$('.demoCursor').mouseleave( function() {
			$(".caption-container2").text('');
	});

	$('.demoCursor').on('click',function(){
		var imgActiva = $('.active');
		//$('.demoCursor').each(function(){
		if($(this).attr('alt') == "Barcelona")
		{
			//alert($(this).attr('alt'));
			var imgElem = $('img[alt="Barcelona"]');
			imgActiva.removeClass('active').css('z-index',-10);
			imgElem.addClass('active').css('z-index',10);
			var newActiva = $('.active');
			$(".caption-container").text(newActiva.attr('alt'));
		}
		if($(this).attr('alt') == "Burgos")
		{
			//alert($(this).attr('alt'));
			var imgElem = $('img[alt="Burgos"]');
			imgActiva.removeClass('active').css('z-index',-10);
			imgElem.addClass('active').css('z-index',10);
			var newActiva = $('.active');
			$(".caption-container").text(newActiva.attr('alt'));
		}
		if($(this).attr('alt') == "Madrid")
		{
			//alert($(this).attr('alt'));
			var imgElem = $('img[alt="Madrid"]');
			imgActiva.removeClass('active').css('z-index',-10);
			imgElem.addClass('active').css('z-index',10);
			var newActiva = $('.active');
			$(".caption-container").text(newActiva.attr('alt'));
		}
		if($(this).attr('alt') == "Alcala")
		{
			//alert($(this).attr('alt'));
			var imgElem = $('img[alt="Alcala"]');
			imgActiva.removeClass('active').css('z-index',-10);
			imgElem.addClass('active').css('z-index',10);
			var newActiva = $('.active');
			$(".caption-container").text(newActiva.attr('alt'));
		}
		if($(this).attr('alt') == "Cordoba")
		{
			//alert($(this).attr('alt'));
			var imgElem = $('img[alt="Cordoba"]');
			imgActiva.removeClass('active').css('z-index',-10);
			imgElem.addClass('active').css('z-index',10);
			var newActiva = $('.active');
			$(".caption-container").text(newActiva.attr('alt'));
		}
		if($(this).attr('alt') == "Alicante")
		{
			//alert($(this).attr('alt'));
			var imgElem = $('img[alt="Alicante"]');
			imgActiva.removeClass('active').css('z-index',-10);
			imgElem.addClass('active').css('z-index',10);
			var newActiva = $('.active');
			$(".caption-container").text(newActiva.attr('alt'));
		}
		//var imgActiva = $('.active');
		//var img = $(this).attr('alt');
		//var img = $(this);
		//var imgElem = $('img[alt="Barcelona"]');
		//var imgElem = $('img[alt = img]');
		//imgActiva.removeClass('active').css('z-index',-10);
		//img.addClass('active').css('z-index',10);
		//var newActiva = $('.active');
		//$(".caption-container").text(newActiva.attr('alt'));
		
	});
});
