$(function() {

  /* UTILITIES */

  $("#utilityInterface").autocomplete(
    '/@@inspector-search-utility/search_interface', {
      width: 400
    });

  var ac_utility_name = $('#utilityName').autocomplete(
    '/@@inspector-search-utility/search_name', {
      width: 400,
      extraParams: {
        iface: function() {
          return $("#utilityInterface").val();
        }
      }
    });

  $("#utilityInterface").change(function() {
    ac_utility_name.flushCache();
  });

  $('#utilitySearch').click(function() {
    var data = {};
    $('.utility-field').each(function() {
      data[$(this).attr('name')] = $(this).val();
    });
    $('#utilityResults').html('');
    showSpinner($(this).parents('fieldset:first'));
    $.ajax({
      url: '/@@inspector-search-utility/search_results',
      data: data,
      dataType: 'html',
      cache: false,
      success: function(data, textStatus, XMLHttpRequest) {
        $('#utilityResults').html(data);
        hideSpinner();
      },
      error: function(XMLHttpRequest, textStatus, errorThrown) {
        alert('Failed: '.concat(textStatus));
        hideSpinner();
      }
    });
  });

  /* general */

  $('.open').live('click', function() {
    $.ajax({
      url: '/@@inspector-open',
      data: {
        path: $(this).parents('td:first').find('input[name=path]').val(),
        line: $(this).parents('td:first').find('input[name=line]').val()
      }
    });
  });

  $('#configSave').click(function() {
    var data = {};
    $('#configuration-form .config-field').each(function() {
      if($(this).attr('type') == 'checkbox') {
        data[$(this).attr('name').concat(':boolean')] = $(this).attr('checked') ? '1' : '';
      } else {
        data[$(this).attr('name')] = $(this).val();
      }
    });
    $.ajax({
      url: '/@@inspector-save-config',
      type: 'POST',
      data: data
    });
  });

  var showSpinner = function(fieldset) {
    $('<img src="/++resource++collective.z3cinspector-spinner.gif" class="spinner" />').appendTo(fieldset);
  };

  var hideSpinner = function() {
    $('.spinner').remove();
  };

});
