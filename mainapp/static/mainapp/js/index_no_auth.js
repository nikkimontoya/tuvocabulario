(function($) {
	$(document).ready(function() {
      $('.tabs').tabs();      

      $('.modal').modal({
        onOpenEnd: function() {
          $('.tabs').tabs('_handleWindowResize');
        }
      });
    });

    $("#reg-form-submit").click(function() {
    	var password = $("#reg-form-password").val();
    	var csrf_token = $(this).closest('form').find('input[name=csrfmiddlewaretoken]').val();

    	if(password == $("#reg-form-confirm-password").val()) {
	    	$.ajax({
	    		method: 'POST',
	    		url: '/user/register/',
	    		data: {
	    			email: $("#reg-form-email").val(),
	    			password: password,
	    			csrfmiddlewaretoken: csrf_token
	    		},
	    		success: function(response) {
		    		if(response.status == 0) {
	    				$("#reg-form-email").addClass("invalid");
	    				$("#reg-form-password").addClass("invalid");
	    			} else if (response.status == 1) {
	    				window.location = '/user/' + response.user_id
	    			}
	    		}
	    	});
        }
    });

    $("#auth-form-submit").click(function() {
    	var csrf_token = $(this).closest('form').find('input[name=csrfmiddlewaretoken]').val();

    	$.ajax({
    		method: 'POST',
    		url: '/user/auth/',
    		data: {
    			email: $("#auth-form-email").val(),
    			password: $("#auth-form-password").val(),
    			csrfmiddlewaretoken: csrf_token
    		},
    		success: function(response) {
    			if(response.status == 0) {
    				$("#auth-form-email").addClass("invalid");
    				$("#auth-form-password").addClass("invalid");
    			} else if (response.status == 1) {
    				window.location = '/user/' + response.user_id
    			}
    		}
    	});
    });
})(jQuery)