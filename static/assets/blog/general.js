$(function(){
	$("a[href=#toc]").click(function(e){
		e.preventDefault();
		$(".toc").slideToggle();
	})
})

