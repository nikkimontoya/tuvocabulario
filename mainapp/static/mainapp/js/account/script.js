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
              $('#translation-card').html(response);
              $('#translation-card').removeClass('hide');
        		}
        	});
        }
  	});

  $('body').on('click', '.add-to-dictionary-link', function(e) {
    e.preventDefault();
    var button = $(this);
    var csrf_token = button.closest('ul').find('input[name=csrfmiddlewaretoken]').val();    
    $.ajax({
      url: button.attr('href'),
      method: 'POST',
      data: {
        csrfmiddlewaretoken: csrf_token
      },
      success: function(response) {
        refreshDictionaryTable();
        M.toast({html: 'Слово было успешно добавлено в ваш словарь'})
      }
    });
  });

  $('body').on('click', '.close-translation', function(e) {
    e.preventDefault();
    $('#translation-card').addClass('hide');
  });
})(jQuery);