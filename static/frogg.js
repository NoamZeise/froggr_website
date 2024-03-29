$(document).ready(function() {
  $('#like_btn').click(function() {
    var postid;
    postid = $(this).attr('data-postid');
    var action = $(this).attr('data-action');
    $.get("/like-post/",
      {'post_id': postid, 'action': action},
      function(data) {
        if (action == 'like') {
            $('#like_btn').text('Unlike Post');
	    $('#like_btn').removeClass("btn-primary").addClass("btn-secondary");
            $('#like_btn').attr('data-action', 'dislike');
            $('#like_count').text(parseInt($('#like_count').text()) + 1);
        } else {
            $('#like_btn').text('Like Post');
	    $('#like_btn').removeClass("btn-secondary").addClass("btn-primary");
            $('#like_btn').attr('data-action', 'like');
            $('#like_count').text(parseInt($('#like_count').text()) - 1);
        }
      })
  });
});
