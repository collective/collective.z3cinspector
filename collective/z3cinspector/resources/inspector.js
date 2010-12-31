$(function() {

  /* TABS */

  $('ul.tabs').tabs('ul.panes > li');
  $(document).bind('keydown', 'ctrl+u', function() {
    $('#tabUtilities').click();
  });
  $(document).bind('keydown', 'ctrl+a', function() {
    $('#tabAdapters').click();
  });
  $(document).bind('keydown', 'ctrl+c', function() {
    $('#tabConfiguration').click();
  });

  /* UTILITIES */

  $("#utilityInterface").autocomplete(
    '/@@inspector-search-utility/search_interface', {
      width: 500
    });

  var ac_utility_name = $('#utilityName').autocomplete(
    '/@@inspector-search-utility/search_name', {
      width: 500,
      extraParams: {
        iface: function() {
          return $("#utilityInterface").val();
        }
      }
    });

  $("#utilityInterface").change(function() {
    ac_utility_name.flushCache();
  });

  $('#utilityForm').submit(function(e) {
    e.preventDefault();
    var data = {};
    $('.utility-field').each(function() {
      data[$(this).attr('name')] = $(this).val();
    });
    $('#utilityResults').html('');
    showSpinner($(this).parents('li:first'));
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


  /* ADAPTERS */

  $("#adapterInterface").autocomplete(
    '/@@inspector-search-adapter/search_interface', {
      width: 500
    });

  var ac_adapter_name = $('#adapterName').autocomplete(
    '/@@inspector-search-adapter/search_name', {
      width: 500,
      extraParams: {
        iface: function() {
          return $("#adapterInterface").val();
        }
      }
    });

  var ac_adapter_descs = new Array();
  $('.adapter-desc-field').each(function(index, value) {
    ac_adapter_descs.push($(this).autocomplete(
      '/@@inspector-search-adapter/search_for', {
        width: 500,
        extraParams: {
          iface: function() {
            return $("#adapterInterface").val();
          },
          name: function() {
            return $('#adapterName').val();
          },
          level: index
        }
      }));
  });

  $("#adapterInterface").change(function() {
    ac_adapter_name.flushCache();
    $(ac_adapter_descs).each(function(){this.flushCache();});
  });

  $('#adapterName').change(function() {
    $(ac_adapter_descs).each(function(){this.flushCache();});
  });

  $('#adapterForm').submit(function(e) {
    e.preventDefault();
    var data = {};
    $('.adapter-field').each(function() {
      data[$(this).attr('name')] = $(this).val();
    });
    $('#adapterResults').html('');
    showSpinner($(this).parents('li:first'));
    $.ajax({
      url: '/@@inspector-search-adapter/search_results',
      data: data,
      dataType: 'html',
      cache: false,
      success: function(data, textStatus, XMLHttpRequest) {
        $('#adapterResults').html(data);
        hideSpinner();
      },
      error: function(XMLHttpRequest, textStatus, errorThrown) {
        alert('Failed: '.concat(textStatus));
        hideSpinner();
      }
    });
  });


  /* config */

  $('#configOpenCommandTemplate').change(function() {
    if($(this).val()) {
      $('#configOpenCommand').val($(this).val());
    }
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

  var showSpinner = function(tab) {
    $('<img src="/++resource++collective.z3cinspector-spinner.gif" class="spinner" />').appendTo(tab);
  };

  var hideSpinner = function() {
    $('.spinner').remove();
  };

});
