(function($) {
	var wordsList = [];
	var rightAnswersCounter = 0;

	function showWordCard(list_id) {
		var word_id = wordsList[list_id]
		$.ajax({
			beforeSend: function() {
				$('.preloader-overlay').removeClass('hide');
			},
			url: '/exercises/audio/get-word-card/' + word_id + '/',
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

				$('#get-next-card-btn').data('next_list_id', next_list_id).addClass('hide')
				$('#check-word-btn').removeClass('hide')
				$('#return-btn').removeClass('hide')
				$('.preloader-overlay').addClass('hide');
				$('.result-content').addClass('hide').find('.result-wrong').addClass('hide')	
			}
		});
	}

	$(document).ready(function() {
		$.ajax({
			beforeSend: function() {
				$('.preloader-overlay').removeClass('hide');
			},
			url: '/exercises/audio/get-words-list/',
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

	$('body').on('click', '#check-word-btn', function(e) {
		e.preventDefault();
		var inputContainer = $('.input-container');
		var resultContainer = $('.result-content');
		var input = inputContainer.find('input');
		var rightAnswer = input.data('word').toLowerCase();
		var userAnswer = input.val().toLowerCase();

		resultContainer.find('.result-right').text(rightAnswer);
		inputContainer.addClass('hide');

		if(userAnswer != rightAnswer) {			
			resultContainer.find('.result-wrong').find('del').text(userAnswer).end().removeClass('hide');
		} else {
			rightAnswersCounter++;
		}

		resultContainer.removeClass('hide')

		$(this).addClass('hide');
		$('#get-next-card-btn').removeClass('hide');
	});

	$('body').on('click', '.icon-sound', function(e) {
	    $(this).prev('audio')[0].play()
	});
})(jQuery);