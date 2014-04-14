contactswidget = {};

/* Update person_title when gender changes (if person_title hasn't been set manually) */
contactswidget.update_person_title = function(){
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
contactswidget.normalize_string = function(s) {
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

contactswidget.serialize_form = function(form) {
   viewArr = $(form).serializeArray(),
   view = {};
   for (var i in viewArr) {
     view[viewArr[i].name] = viewArr[i].value;
   }
   return view;
 }

/* Update the token which matches the input*/
contactswidget.update_token = function(){
	var name = $(this).val();
	var token = $(this).closest('tr').find('input[id$="-widgets-token"]');
	if (token.val() == '') {
		token_value = contactswidget.normalize_string(name);
		token.val(token_value);
	}
}

/* Manage all stuff for the directory edit form */
contactswidget.manage_directory = function(){
    // hide some columns in directory edit form
	$('input[id$="-widgets-token"]').hide();
	$('#formfield-form-widgets-position_types thead').hide();
	$('#formfield-form-widgets-organization_types thead').hide();
	$('#formfield-form-widgets-organization_levels thead').hide();
	$('.portaltype-directory .datagridwidget-table-view thead').hide();
	// update tokens if necessary
	$('input[id$="-widgets-name"]').blur(contactswidget.update_token);
}

/* Hide use_parent_address field if address field is empty */
contactswidget.manage_hide_use_parent_address = function(){
	if ($("#address").length == 0) {
		$("#formfield-form-widgets-IContactDetails-use_parent_address").hide();
	}
}

contactswidget.get_selected_contact = function(form, field_id) {
  var view = contactswidget.serialize_form(form);
  var token = view[field_id];
  var input = form.find('#' + field_id.replace(/\./g, '-') + '-input-fields input[value="'+token+'"]');
  var title = input.siblings('.label').find('a').first().text();
  var path = '/' + token.split('/').slice(2).join('/');
  return {token: token, title: title, path: path};
}

contactswidget.setup_relation_dependency = function(master_field, slave_field, relation){
    /* slave field vocabulary is restricted on contacts who have a relation 'relation'
     * with value set in master field
     * master_field is on format : form.widgets.mymasterfield,
     * slave_field is on format : form.widgets.myslavefield,
     */

    $('body').on('change', '#'+master_field.replace(/\./g, '-')+'-input-fields input', function(e){
        var form = $(this).parents('form').first();
        var selected = contactswidget.get_selected_contact(form, master_field);
        var relations = {};
        relations['relations.' + relation + ':record'] = selected.token;
        var slave_field_query = $('#' + slave_field.replace(/\./g, '-') + '-widgets-query')
        slave_field_query.setOptions({extraParams: relations}).flushCache();
    });
}

$(document).ready(function(){
    $(document).delegate('#formfield-form-widgets-gender input', 'change',
                         contactswidget.update_person_title);
    contactswidget.manage_directory();
    contactswidget.manage_hide_use_parent_address();

    $('.contactoverlay').prepOverlay({
      subtype: 'ajax',
      filter: common_content_filter,
      formselector: '#form',
      closeselector: '[name="form.buttons.cancel"]',
      noform: function(el, pbo) {return 'reload';},
    });

    $('.deleteoverlay').prepOverlay({
      subtype: 'ajax',
      filter: common_content_filter,
      formselector: '#delete_confirmation',
      closeselector: '[name="form.button.Cancel"]',
      noform: function(el, pbo) {return 'reload';},
    });

});
