$(function(){
	function onFormSubmit(event){

		var data = $(event.target).serializeArray();

		var student = {};
		for(var i = 0; i<data.length ; i++){
			student[data[i].name] = data[i].value;
		}

		// send data to server
			var student_create_api = '/api/student';
			$.post(student_create_api, student, function(response){

			// read response from server
			if (response.status = 'OK') {
				var full_name = response.data.Year + ' - ' + response.data.Title;
				$('#student-list').prepend('<li>' + full_name + '</li>')
				$('input[type=text], [type=number]').val('');
			} else {

			}

			});

		return false;
	}

	function loadStudent(){
		var student_list_api = '/api/student';
		$.get(student_list_api, {} , function(response) {
			console.log('#student-list', response)
			response.data.forEach(function(student){
				var full_name = student.Year + ' - '  + student.Title;
				$('#student-list').append('<li>' + full_name + '</li>')
			});
		});
	}

	loadStudent();
	$('form#create-form').submit(onFormSubmit);

	$(document).on('click', 'button#delete', function(){
		$(this).closest('li').remove();
	});

});
