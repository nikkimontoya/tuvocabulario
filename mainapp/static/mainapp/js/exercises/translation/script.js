(function($) {
	var wordsList = [];
	var rightAnswersCounter = 0;

	function showWordCard(list_id) {
		var word_id = wordsList[list_id]
		$.ajax({
			beforeSend: function() {
				$('.preloader-overlay').removeClass('hide');
			},
			url: '/exercises/translation/get-word-card/' + word_id + '/',
			method: 'POST',
			data: {
				csrfmiddlewaretoken: $('#word-card-content').find('input[name=csrfmiddlewaretoken]').val()
			},
			success: function(response) {
				$('#word-card-content').html(response);

				var next_list_id;
				if(typeof(wordsList[list_id + 1]) != 'undefined') {
					next_list_id = list_id + 1
					
				} else {
					next_list_id = -1
				}

				$('#get-next-card-btn').data('next_list_id', next_list_id).removeClass('hide')	
				$('#return-btn').removeClass('hide')
				$('.preloader-overlay').addClass('hide');			
			}
		});
	}

	$(document).ready(function() {
		$.ajax({
			beforeSend: function() {
				$('.preloader-overlay').removeClass('hide');
			},
			url: '/exercises/translation/get-words-list/',
			method: 'POST',
			data: {
				csrfmiddlewaretoken: $('body').find('input[name=csrfmiddlewaretoken]').val()
			},
			success: function(response) {
				wordsList = response.wordList
				showWordCard(0)
				$('.preloader-overlay').addClass('hide');
			}
		});
	});

	$('body').on('click', '#get-next-card-btn', function(e) {
		e.preventDefault();
		var next_list_id = $(this).data('next_list_id');

		if(next_list_id != -1) {
			showWordCard(next_list_id);
		} else {
			$('#word-card-content').html('<h4>Упражнение завершено. Вы дали ' + rightAnswersCounter
				+ ' правильных ответов из ' + wordsList.length + '</h4>');
			$(this).addClass('hide');
			$('#return-btn').removeClass('hide');
			$('#word-card').addClass('center-align')
		}
	});

	$('body').on('click', '#word-card-content .collection-item', function() {
		if(!$(this).hasClass('right-translation')) {
			$(this).addClass('red darken-4 white-text');
		} else {
			rightAnswersCounter++;
		}

		$('#word-card-content .right-translation').addClass('green darken-4 white-text');
		$('#word-card-content .collection-item').addClass('disabled-item');
	});
})(jQuery);