  var buildQueryString = function() {
    var queries = [$('#search-field').val()];
    var typicalagerange = $('#typicalagerange-field').val();
    if (typicalagerange) {
      queries.push('more:pagemap:creativework-typicalagerange:' + typicalagerange);
    }
    var grade = $('#grade-field').val();
    if (grade) {
      queries.push('more:pagemap:creativework-grade:' + grade);
    }
    var extra = $('#extra-field').val();
    if (extra) {
      queries.push(extra);
    }
    return queries.join('+');
  };
  $('#search-button').click(function() {
    console.log(google.search.cse.element.getAllElements());
    var element = google.search.cse.element.getElement('lrmi-search');
    var query = buildQueryString();
    console.log(query)
    element.execute(query);

  });

  $(document).on("click", "a.moreLikeThis", function(){
    var propertyName = 'more:pagemap:creativework-' + $(this).attr('data-propertyname') + ':';
    console.log(propertyName)
    var propertyValue = $(this).attr('data-propertyvalue').toLowerCase().replace(/\s/g, '_');
    console.log(propertyValue)
    $('#extra-field').val(propertyName + propertyValue + ' OR ' + propertyName.replace('creativework', 'scholarlyarticle') + propertyValue);
    $('#search-button').click();


    return false;
  });

  $('#clear-extra').click(function() {
    $('#extra-field').val('');
    $('#search-button').click();
  })

  $('.kd-segmentedcontrol a').click(function() {
    $(this).addClass('selected');
    $(this).siblings().removeClass('selected');
    var cx = $(this).attr('data-cx');
    window.location = window.location.origin + '/?cx=' + cx;

  });

console.log(cx);

$('[data-cx="' + cx +'"]').addClass('selected');
$('[data-cx="' + cx +'"]').siblings().removeClass('selected');

