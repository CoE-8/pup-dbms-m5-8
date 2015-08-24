$(function(){
	function onFormSubmit(event){

		var data = $(event.target).serializeArray();

		var student = {};

		for(var i = 0; i<data.length ; i++){
			student[data[i].name] = data[i].value;
		}

		// send data to server
			var thesis_create_api = '/api/thesis';
			$.post(thesis_create_api, student, function(response){

			// read response from server
			if (response.status = 'OK') {
				var thesisDetail = '<strong>YEAR:</strong> ' + response.data.Year + '<br><strong>TITLE: </strong>' + response.data.Title + '<br><strong>CREATED BY: </strong>' + response.data.username;
				$('#student-list').prepend('<li>' + thesisDetail + '<br><a href=\"/thesis/delete/'+response.data.id+'\"><button id=\"delete\" class=\"btn btn-danger\" type=\"submit\">DELETE</button></a> <a href=\"/thesis/edit/'+response.data.id+'\"><button id=\"edit\" class=\"btn btn-success\" type=\"submit\">EDIT</button></a><hr></li>')
				$('input[type=text], [type=number]').val('');
				$('textarea[type=text]').val('');
				$('select[name=Year]').val('Year');
				$('select[name=Section]').val('Section');
			} else {

			}

			});

		return false;
	}

	function loadThesis(){
		var thesis_list_api = '/api/thesis';
		$.get(thesis_list_api, {} , function(response) {
			console.log('#student-list', response)
			response.data.forEach(function(thesis){
				var thesisDetail = '<strong>YEAR: </strong>' + thesis.Year + '<br><strong>TITLE: </strong>'  + thesis.Title + '<br><strong>CREATED BY: </strong>' + thesis.username;;
				$('#student-list').append('<li>' + thesisDetail + '<br><a href=\"/thesis/delete/'+thesis.id+'\"><button id=\"delete\" class=\"btn btn-danger\" type=\"submit\">DELETE</button></a> <a href=\"/thesis/edit/'+thesis.id+'\"><button id=\"edit\" class=\"btn btn-success\" type=\"submit\">EDIT</button></a><hr></li>')
			});
		});
	}

	loadThesis();
	$('form#create-form').submit(onFormSubmit);

});
