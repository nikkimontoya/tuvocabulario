(function($) {
	var wordsList = [];
	var rightAnswersCounter = 0;
	var wordErrors = 0;
	var totalErrors = 0;

	function showWordCard(list_id) {
		var word_id = wordsList[list_id]
		$.ajax({
			url: '/exercises/construct-the-word/get-word-card/' + word_id + '/',
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
			}
		});
	}

	$(document).ready(function() {
		$.ajax({
			url: '/exercises/construct-the-word/get-words-list/',
			method: 'POST',
			data: {
				csrfmiddlewaretoken: $('body').find('input[name=csrfmiddlewaretoken]').val()
			},
			success: function(response) {
				wordsList = response.wordList
				showWordCard(0)
			}
		});
	});

	$('body').on('click', '#get-next-card-btn', function(e) {
		e.preventDefault();

		if(wordErrors == 0) {
			rightAnswersCounter++;
		}

		wordErrors = 0;

		var next_list_id = $(this).data('next_list_id');

		if(next_list_id != -1) {
			showWordCard(next_list_id);
		} else {
			$('#word-card-content').html('<h4>Упражнение завершено. Вы дали ' + rightAnswersCounter
				+ ' правильных ответов из ' + wordsList.length + '</h4><h4>Допущено ' + totalErrors + ' ошибок</h4');
			$(this).addClass('hide');
			$('#return-btn').removeClass('hide');
			$('#word-card').addClass('center-align')
		}
	});

	$('body').on('click', '#letters-container .letter', function(e) {
		e.preventDefault();
		var firstEmptyLetter = $('#empty-letters-container .empty-place').first();
		if (firstEmptyLetter.data('letter') == $(this).text()) {
			firstEmptyLetter.removeClass('empty-place pulse').addClass('filled-place').text(firstEmptyLetter.data('letter'));
			$(this).attr('data-count', $(this).attr('data-count') - 1);
		} else {
			firstEmptyLetter.addClass('pulse');
			wordErrors++;
			totalErrors++;
		}
	});
})(jQuery);