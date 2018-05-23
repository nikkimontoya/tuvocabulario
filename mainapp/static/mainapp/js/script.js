(
  function($) {
  	var token = "ZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SmxlSEFpT2pFMU1qY3hOamN4TURJc0lrMXZaR1ZzSWpwN0lrTm9ZWEpoWTNSbGNuTlFaWEpFWVhraU9qVXdNREF3TENKVmMyVnlTV1FpT2pFME1UVXNJbFZ1YVhGMVpVbGtJam9pWlRjMVpEWTJNbU10WmpreFppMDBOVE5sTFdFeFkyTXROakEzWTJSbE5qSmhNRFl5SW4xOS5jbjlvejBfdnJZNGRGbzRQc2ZQSGZ2NDRoc0NTU0NjeGwxbGxkVWdtR0hZ";
	$(document).ready($.ajax({
		url: 'https://developers.lingvolive.com/api/v1.1/authenticate',
		method: 'POST',
		headers: {
			"Authorization": "Basic ZTc1ZDY2MmMtZjkxZi00NTNlLWExY2MtNjA3Y2RlNjJhMDYyOjQzOGZlNzcxNTAxODQzODI4OTA3OWI4MjQ2ZmExZTI1",
		},
		data: {},
		success: function(response) {
			token = response;
		}
	}));
  	$('#vocabulary-submit').click(function(e) {
  		e.preventDefault();
        var text = $('#vocabulary-input').val();

        if (text != '') {
        	$.ajax({
        		url: 'https://developers.lingvolive.com/api/v1/Translation',
        		method: 'GET',
        		headers: {
        			"Authorization": "Bearer " + token
        		},
        		data: {
        			text: text,
        			srcLang: 1034,
        			dstLang: 1049
        		},
        		beforeSend: function (jqXHR, settings) {
        jqXHR.setRequestHeader('Authorization', "Bearer " + token);
    },
        		success: function(response) {
        			$('#result').text(response);
        		}
        	});
        }
  	});
  }
)(jQuery)