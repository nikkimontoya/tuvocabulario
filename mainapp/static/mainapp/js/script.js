(
  function($) {
  	$('#vocabulary-submit').click(function(e) {
  		  e.preventDefault();
        var text = $('#vocabulary-input').val();
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
        			$('#result-heading').text(response.Heading);
              $('#result-translation').text(response.Translation.Translation);
        		}
        	});
        }
  	});
  }
)(jQuery)