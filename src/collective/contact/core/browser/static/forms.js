contactswidget = {};

/* Update person_title when gender changes (if person_title hasn't been set manually) */
contactswidget.update_person_title = function(){
	var gender = $(this).val();
	var person_title = $('#form-widgets-person_title').val();
	if (person_title === '' || person_title == 'M.' || person_title == 'Mme') {
		if (gender == 'M') {
			$('#form-widgets-person_title').val("M.");
		} else {
			$('#form-widgets-person_title').val("Mme");
		}
	}
};

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
};

contactswidget.serialize_form = function(form) {
   var viewArr = $(form).serializeArray();
   var view = {};
   for (var i in viewArr) {
     view[viewArr[i].name] = viewArr[i].value;
   }
   return view;
 };

/* Update the token which matches the input*/
contactswidget.update_token = function(){
	var name = $(this).val();
	var token = $(this).closest('tr').find('input[id$="-widgets-token"]');
	if (token.val() === '') {
		token_value = contactswidget.normalize_string(name);
		token.val(token_value);
	}
};

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
};

/* Hide use_parent_address field if parent address is empty and if
   use_parent_address is not checked */
contactswidget.manage_hide_use_parent_address = function(){
  if ($("#form-widgets-IContactDetails-parent_address").text().trim().length === 0) {
    if($('#form-widgets-IContactDetails-use_parent_address-0').length > 0
      && $('#form-widgets-IContactDetails-use_parent_address-0:checked').length == 0) {
      if($('#formfield-form-widgets-position').length === 0){
        /* except on held position form because, there,
         * actual parent address can change during edition
         */
        $("#formfield-form-widgets-IContactDetails-use_parent_address").hide();
      }
    }
  }
};

contactswidget.get_selected_contact = function(form, field_id) {
  var view = contactswidget.serialize_form(form);
  var token = view[field_id];
  if(token === undefined){
      return undefined;
  }
  var input = form.find('#' + field_id.replace(/\./g, '-') + '-input-fields input[value="'+token+'"]');
  var title = input.siblings('.label').find('a').first().text();
  var path = '/' + token.split('/').slice(2).join('/');
  return {token: token, title: title, path: path};
};

contactswidget.setup_relation_dependency = function(master_field, slave_field, relation){
    /* slave field vocabulary is restricted on contacts who have a relation 'relation'
     * with value set in master field
     * master_field is on format : form.widgets.mymasterfield,
     * slave_field is on format : form.widgets.myslavefield,
     */
    function apply_relation_dependency(input, master_field, slave_field, relation) {
        var form = input.parents('form').first();
        var selected = contactswidget.get_selected_contact(form, master_field);
        /* set new relation search parameter on slave field */
        var relations = {};
        if(selected !== undefined){
            relations['relations.' + relation + ':record'] = selected.token;
        }
        var slave_field_query = $('#' + slave_field.replace(/\./g, '-') + '-widgets-query');
        slave_field_query.setOptions({extraParams: relations}).flushCache();

        /* change create link so that master field selection is selected by default */
        var add_link = $('#formfield-' + slave_field.replace(/\./g, '-')).find('.addnew');
        if(add_link.length == 1){
            var orig_href = add_link.attr('href');
            var key;
            if(orig_href.indexOf('@add-contact') > -1) {
                key = '@add-contact';
            }
            if(orig_href.indexOf('@add-held-position') > -1) {
                key = '@add-held-position';
            }
            if(key) {
                var base_add_url = orig_href.substr(0, orig_href.indexOf(key) + key.length);
                var new_url = base_add_url + '?oform.widgets.organization=' + selected.token;
                new_url += '&oform.widgets.position=' + selected.token;
                if(add_link.orig_text === undefined){
                    add_link.orig_text = add_link.text();
                }
                add_link.attr('href', new_url);
                add_link.data('pbo').src = new_url;
                var text_wo_company = add_link.orig_text.replace(/ *\([^)]*\) */g, "");
                if (selected.token === '--NOVALUE--') {
                    add_link.text(text_wo_company);
                } else {
                    add_link.text(text_wo_company + ' (' + selected.title + ')');
                }

            }
        }
    }

    var selector = '#' + master_field.replace(/\./g, '-') + '-input-fields input';

    $('body').on('change', selector, function(){
        apply_relation_dependency($(this), master_field, slave_field, relation);
    });

    $(document).ready(function(){
        $('body').find(selector).each(function(){
            apply_relation_dependency($(this), master_field, slave_field, relation);
        });
    });
};

$(document).ready(function(){
    $(document).on('change', '#formfield-form-widgets-gender input',
                         contactswidget.update_person_title);
    /* contactswidget.manage_directory();  Do not hide token column in edit mode */
    contactswidget.manage_hide_use_parent_address();

    jQuery(document).bind('loadInsideOverlay',
            function(e, pbajax, responseText, errorText, api){
        contactswidget.manage_hide_use_parent_address();
    });

    $('.contactoverlay').prepOverlay({
      subtype: 'ajax',
      filter: common_content_filter,
      formselector: '#form',
      closeselector: '[name="form.buttons.cancel"]',
      noform: function(el, pbo) {return 'reload';}
    });

    $('.deleteoverlay').prepOverlay({
      subtype: 'ajax',
      filter: common_content_filter,
      formselector: '#delete_confirmation',
      closeselector: '[name="form.button.Cancel"]',
      noform: function(el, pbo) {return 'reload';}
    });

});
