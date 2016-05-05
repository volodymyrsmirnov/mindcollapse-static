$(document).on "ready", ()->

# show table of contents on #toc link click
  $("a[href=#toc]").on "click", (event)->
    event.preventDefault()
    $(".toc").slideToggle()
    return

  # show popup window on social link click
  $(".social a").on "click", (event)->
    event.preventDefault()
    window.open $(this).attr("href"), $(this).attr("title"), "location=0,status=0,scrollbars=0,width=640,height=480"
    return

  # remove hyphenation from text on copy
  $(".content").on "copy", (event)->
    if event.originalEvent and event.originalEvent.clipboardData
      event.preventDefault()

      selected_text = window.getSelection().toString()
      selected_text = selected_text.replace /[\u00AD\u002D\u2011]+/g, ""

      event.originalEvent.clipboardData.setData "Text",
                                                """#{ selected_text }

                Подробнее на #{ document.location.href }"""

  # keyboard navigation
  $(window).on "keyup", (event)->
    if event.altKey
      new_location = undefined

      switch event.which
        when 37 then new_location = $("link[rel*=prev]").attr("href");
        when 39 then new_location = $("link[rel*=next]").attr("href");

      if new_location?
        document.location.href = new_location

  # open post full size images in new tab on click if window width < 900px;
  # made for mobile image responsible problem solution
  $(".content img").on "click", ()->
    if $(window).width() <= 900
      window.open($(@).attr("src"), "_blank");