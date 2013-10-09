/* Update person_title when gender changes (if person_title hasn't been set manually) */
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

/* Replace spaces with underscores, removes accents and other special characters */
function normalize_string(s) {
	var rules = {
		'a': /[àáâãäå]/g,
		'ae': /[æ]/g,
		'c': /[ç]/g,
		'e': /[èéêë]/g,
		'i': /[ìíîï]/g,
		'n': /[ñ]/g,
		'o': /[òóôõö]/g,
		'oe': /[œ]/g,
		'u': /[ùúûü]/g,
		'y': /[ýÿ]/g,
		'th': /[ðþ]/g,
		'ss': /[ß]/g,
		'_': /[\s\\]+/g
	};
	s = s.toLowerCase();
	for (var r in rules) s = s.replace(rules[r], r);
	return s;
}

/* Update the token which matches the input*/
update_token = function(){
	var name = $(this).val();
	var token = $(this).closest('tr').find('input[id$="-widgets-token"]');
	if (token.val() == '') {
		token_value = normalize_string(name);
		token.val(token_value);
	}
}

/* Manage all stuff for the directory edit form */
manage_directory = function(){
    // hide some columns in directory edit form
	$('input[id$="-widgets-token"]').hide();
	$('#formfield-form-widgets-position_types thead').hide();
	$('#formfield-form-widgets-organization_types thead').hide();
	$('#formfield-form-widgets-organization_levels thead').hide();
	$('.portaltype-directory .datagridwidget-table-view thead').hide();
	// update tokens if necessary
	$('input[id$="-widgets-name"]').blur(update_token);
}

/* Hide use_parent_address field if address field is empty */
manage_hide_use_parent_address = function(){
	if ($("#address").length == 0) {
		$("#formfield-form-widgets-IContactDetails-use_parent_address").hide();
	}
}

$(document).ready(function(){
    $(document).delegate('#formfield-form-widgets-gender input', 'change', update_person_title);
    manage_directory();
    manage_hide_use_parent_address();
});
