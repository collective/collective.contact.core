update_person_title = function(){
	var gender = $(this).val();
	var person_title = $('#form-widgets-person_title').val();
	if (person_title == '' || person_title == 'M.' || person_title == 'Mme') {
		if (gender == 'M') {
			$('#form-widgets-person_title').val("M.");
		} else {
			$('#form-widgets-person_title').val("Mme");
		}
	}
}

$(document).ready(function(){
    $('#formfield-form-widgets-gender input').change(update_person_title);
});
