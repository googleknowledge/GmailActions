$(document).ready(function(){

  // Set up email content editor.
  var editor = CodeMirror.fromTextArea(document.getElementById("code"), {
    mode: {name: "htmlmixed"},
    tabMode: "indent",
    lineNumbers: true
  });
  editor.on('focus', function() {
    if (editor.getValue() === 'Paste email markup here') {
        editor.setValue('');
    }
  });
  editor.on('blur', function() {
      if (editor.getValue() === '') {
          editor.setValue('Paste email markup here');
      }
  });

  // Attach button listeners.
  $("#send-email").click(function() {
    $.post('/', {'content': editor.getValue()}, function(data) {
      $('#flash').text(data);
    });
  });
  $('#load-sample').change(function() {
    if (!$(this).val()) {
      return;
    }
    var now  = new Date();
    var tz = now.getTimezoneOffset() / -60;
    tz = tz < 10 ? '0' + tz : tz;
    var googleNowDate = now.toISOString().replace(/\.[0-9]*Z/, '%2B');
    // The current date is used to contruct Google Now cards in the backend.
    var url = $(this).val() + '?googleNowDate=' + googleNowDate + tz + ':00';
    $.get(url, function(data) {
      editor.setValue(data);
    })
  });

  // Set up listening to messages from the backend.
  var onOpened = function() {
    var token = channel.token_ || channel.fd;
    $('#client-log p').text('Listening for calls to the server ').append($('<span class="token">token=' + token + '</span>'));
  };
  var onMessage = function(msg) {
    console.log(msg)
    $('#client-log').append('<p>' + msg.data + '</p>')
  };
  var channel = new goog.appengine.Channel(token);
  var socket = channel.open();
  socket.onopen = onOpened;
  socket.onmessage = onMessage;
});


