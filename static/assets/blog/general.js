$(function(){

	// show table of contents on #toc link click
	$("a[href=#toc]").click(function(e){
		e.preventDefault();
		$(".toc").slideToggle();
	});

	// show popup window on socila link click
	$(".social a").click(function(e){
		e.preventDefault();
		window.open ($(this).attr("href"), $(this).attr("title"), "location=0,status=0,scrollbars=0,width=640,height=480");
	});

	// remove hyphenation from text on copy event
	$(".content").on("copy", function(e){
		if (e.originalEvent && e.originalEvent.clipboardData) {
			e.preventDefault();

			var selected_text = window.getSelection().toString();

			// replace soft hyphens here
			selected_text = selected_text.replace(/[\u00AD\u002D\u2011]+/g, "");

			e.originalEvent.clipboardData.setData("Text", selected_text);
		}
	})

	// keyboard navigation
	$(window).on("keyup", function(e){
		if (e.altKey) {
			var newloc = null;

			console.log(e);

			if (e.which == 37) {
				newloc = $("link[rel*=prev]").attr("href");
			} else if (e.which == 39) {
				newloc = $("link[rel*=next]").attr("href");
			} else if (e.which == 38) {
				newloc = $("link[rel*=up]").attr("href");
			} 

			if (newloc) {
				document.location.href = newloc;
			}
		}
	})
})

