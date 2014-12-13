function search() {
  $.post('/', {'keyword' : $('#keyword').val()}, function(data) {
    result = data['result']

    $('#_').html('<ul>')

    for (i = 0; i < result.length; ++i) {
      title = result[i]['title']
      type = result[i]['type']
      answer = result[i]['answer']
      ret = '<li><h5><small><strong>[' + type + ']</strong></small>&nbsp;' + title + '</h5></li>' + '<p class="answer">' + answer + '</p>'
      $('#_').append(ret)
    }

    if (result.length == 0)
      $('#_').append('<li><h5>未搜索到相关答案</h5></li>')

    $('#_').append('</ul>')

  }).fail(function() {
    $('#_').html('查询失败')
  })
}

$("#search").click(search)
$("#keyword").keypress(function(event) {
  if (event.keyCode == 13)
    search()
})

$(function() {
  $("#keyword").focus();
});
