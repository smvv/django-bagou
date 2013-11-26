$(document).ready(function() {
  try {
    var ws = $.websocket(WEBSOCKET_URL, {
      open: function(){
        message('<p class="event">Socket Status: ' + ws.readyState + ' (open)');
      },
      close: function(){
        message('<p class="event">Socket Status: '+ ws.readyState+' (Closed)');
      },
      events: {
        message: function(msg){
          message('<p class="message">Received (type:' + msg.type + '): ' + msg.data.name + ': ' + msg.data.text);
        }
      }
    })
  } catch(exception) {
    message('<p>Error: ' + exception);
  };

  message('<p class="event">Socket Status: ' + ws.readyState);

  function message(msg){
    $('#alerts').append(msg + '</p>');
  };

  // Send on enter keypress
  $('#text').keypress(function(event) {
      if (event.keyCode == '13') {
        send();
      }
  });

  // I am using this one
  function send(){
    var field1 = $('#field1').val();
    ws.send('message', field1);
  }

  $('#Submit').click(function(){
    message('Waiting for response from server');
    send();
  });

  $('#disconnect').click(function(){
     ws.close();
  });
});
