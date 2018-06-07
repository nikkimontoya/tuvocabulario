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
    $('.modal').modal();
	});

	$('#search-words-submit').click(function(e) {
  		e.preventDefault();
        var text = $('#search-words-input').val();
        var csrf_token = $(this).closest('form').find('input[name=csrfmiddlewaretoken]').val();

        if (text != '') {
        	$.ajax({
        		url: '/dictionary/',
        		method: 'GET',
        		data: {
        			text: text,
              //csrfmiddlewaretoken: csrf_token
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

  $('body').on('click', '.icon-sound', function(e) {
    $(this).prev('audio')[0].play()
  });

  $('body').on('click', '.delete-icon', function(e) {
    $('#deleting-word-confirm').modal('open').data('id', $(this).closest('tr').data('userwordid'));
  });

  $('body').on('click', '#deleting-word-confirm-btn', function(e) {
    var csrf_token = $("#search-words-form").find('input[name=csrfmiddlewaretoken]').val();
    $.ajax({
        url: '/remove-from-dictionary/',
        method: 'POST',
        data: {
          word_id: $('#deleting-word-confirm').data('id'),
          csrfmiddlewaretoken: csrf_token
        },
        success: function(response) {
          refreshDictionaryTable();
          M.toast({html: 'Слово было успешно удалено из вашего словаря'})
        }
      });
  });
})(jQuery);