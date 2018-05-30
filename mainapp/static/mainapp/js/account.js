(function($) {
	$(document).ready(function(){
		$(".dropdown-trigger").dropdown({ coverTrigger: false });
	});

	$('#search-words-submit').click(function(e) {
  		e.preventDefault();
        var text = $('#search-words-input').val();
        var csrf_token = $(this).closest('form').find('input[name=csrfmiddlewaretoken]').val();

        if (text != '') {
        	$.ajax({
        		url: '/dictionary/',
        		method: 'POST',
        		data: {
        			text: text,
              csrfmiddlewaretoken: csrf_token
        		},
        		success: function(response) {
        			$('#result-heading').text(response.original);
              		$('#result-translation').text(response.translation);
        		}
        	});
        }
  	});
})(jQuery);