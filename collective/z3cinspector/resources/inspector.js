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
    console.info(data);
    $.ajax({
      url: '/@@inspector-search-utility/search_results',
      data: data,
      dataType: 'html',
      cache: false,
      success: function(data, textStatus, XMLHttpRequest) {
        $('#utilityResults').html(data);
      }
    });
  });

});
