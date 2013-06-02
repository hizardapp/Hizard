(function() {
  $(document).ready(function() {
    $('.flexslider').flexslider({
      animation: "fade"
    });

    // hide #back-top first
    $("#back-top").hide();

    // fade in #back-top
    $(function () {
      $(window).scroll(function () {
        // Edit here if you'd like the "Back to top" button to appear before/after
        // scrolling down 100px. Or if you'd like it to show up on smaller/wider screens only
        // adjust the 1250px or remove it all together if you don't want it to depend on size
        if ( ($(this).scrollTop() > 100) && ($(window).width() >= 1250) ) {
          $('#back-top').fadeIn();
        } else {
          $('#back-top').fadeOut();
        }
      });

      // scroll body to 0px on click
      $('#back-top a').click(function () {
        $('body,html').animate({
          scrollTop: 0
        }, 800);
        return false;
      });
    });

    $("#add-interest").submit(function (e) {
      e.preventDefault();
      $.post(e.target.action,
          {email: $("#id_email").val()},
          function(data) {
            $("#result").text(data.message);
        if (data.result === 'error') {
            $("#result").text(data.message);
        } else {
            $("#result").text(data.message);
            $(".interestfields").hide();
        }
      });
    });
  });
})();
