(function($) {
	var horDirection = true;

	$('body').on('click', '#crossword-container .collection-item', function(e) {
		e.preventDefault();
		var that = $(this);
		$('#crossword-container .collection-item').removeClass('active');
		that.addClass('active');
        var attr = that.data('indexhor') != undefined ? 'indexhor' : 'indexver';
        horDirection = that.data('indexhor') != undefined;

		$('.crossword-table input').blur().removeClass('word-highlighted crossword-error');
		$('.crossword-table input[data-' + attr + '="' + that.data(attr) + '"]').addClass('word-highlighted').first().focus()
	});

	$('body').on('click', '.check-crossword', function(e) {
		e.preventDefault();

		var wordIndexes = {};

		$('#crossword-container .collection-item').each(function(i) {
			var attr = $(this).data('indexhor') != undefined ? 'indexhor' : 'indexver';
			wordIndexes[attr + $(this).data(attr)] = true;
		});

		$('.crossword-table input').removeClass('word-highlighted').each(function(i) {
			var input = $(this);
			if(input.val().toLowerCase() != input.data('letter').toLowerCase()) {
				input.addClass('crossword-error');
				
				if(input.data('indexhor') != 0) {
					wordIndexes['indexhor' + input.data('indexhor')] = false;
				}

				if(input.data('indexver') != 0) {
					wordIndexes['indexver' + input.data('indexver')] = false;
				}
			}
		});

		total = 0;
		right = 0;

		for (var i in wordIndexes) {
			total++;
			if(wordIndexes[i])
				right++
		}

		if (total == right) {
			text = 'Вы правильно разгадали весь кроссворд. Поздравляем!'
		} else {
			text = 'Вы правильно разгадали ' + right + ' слов из ' + total + '.'
		}

		$('#check-modal .modal-content').text(text);
		$('#check-modal').modal();
		$('#check-modal').modal('open');
	});

	$('body').on('keyup', '.crossword-table input', function(e) {
		var that = $(this);
		// Если действие - не стирание
		if(that.val() != '') {
			if (horDirection) {
				var next = that.closest('td').next().find('input');				
			} else {
				var next = that.closest('tr').next().find('input[data-indexver="' + that.data('indexver') + '"]')
			}


			if(next != undefined) {
				next.focus()
			}
		}
	});

	$('body').on('keydown', '.crossword-table input', function(e) {
		var that = $(this);
		if (e.keyCode == 8 && that.val() == '') {
			e.preventDefault();
			if (horDirection) {
				var prev = that.closest('td').prev().find('input');				
			} else {
				var prev = that.closest('tr').prev().find('input[data-indexver="' + that.data('indexver') + '"]')
			}

			if(prev != undefined) {
				prev.val('');
				prev.focus();
			}
		}
	});

	$('body').on('mousedown', '.crossword-table input', function(e) {
		var that = $(this);
		var indexhor = that.data('indexhor');
		var indexver = that.data('indexver');
		
        if (indexhor == 0 || indexver == 0) {
        	horDirection = that.data('indexhor') != 0;
        } else {
        	if(that.hasClass('first-letter-hor')) {
        		horDirection = true
        	} else if(that.hasClass('first-letter-ver')) {
        		horDirection = false
        	}
        }
		
		var attr = horDirection ? 'indexhor' : 'indexver';

		$('#crossword-container .collection-item').removeClass('active');
		$('#crossword-container .collection-item[data-' + attr + '="' + that.data(attr) + '"]').addClass('active');
		$('.crossword-table input').blur().removeClass('word-highlighted crossword-error');
		$('.crossword-table input[data-' + attr + '="' + that.data(attr) + '"]').addClass('word-highlighted')
	});
})(jQuery);