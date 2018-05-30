(function($) {
  function refreshDictionaryTable() {
    var container = $('#dictionary-table');
    $.ajax({
      url: '/get-dictionary-table/',
      method: 'POST',
      data: {
        csrfmiddlewaretoken: container.find('input[name=csrfmiddlewaretoken]').val()
      },
      success: function(response) {
        container.html(response);
      }
    });
  }

	$(document).ready(function(){
		$(".dropdown-trigger").dropdown({ coverTrigger: false });
    refreshDictionaryTable();
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
              $('#add-to-dictionary').attr('href', '/add-to-dictionary/' + response.wordId + '/');
              $('#translation-card').removeClass('hide');
        		}
        	});
        }
  	});

  $('#add-to-dictionary').click(function(e) {
    var button = $(this);
    var csrf_token = button.closest('.card-action').find('input[name=csrfmiddlewaretoken]').val();
    e.preventDefault();
    $.ajax({
      url: button.attr('href'),
      method: 'POST',
      data: {
        csrfmiddlewaretoken: csrf_token
      },
      success: function(response) {
        refreshDictionaryTable();
      }
    });
  });
})(jQuery);