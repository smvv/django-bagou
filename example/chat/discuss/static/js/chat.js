function isReady(callback) {
  var readyStateCheckInterval = setInterval(function() {
      if (document.readyState === "complete") {
          if (callback) callback();
          clearInterval(readyStateCheckInterval);
      }
  }, 10);
}

function loadChat() {
  var focused = true;
  var counter = 0;
  var favicon=new Favico({
    type : 'rectangle',
    animation: 'slide',
  });
  favicon.badge(counter);
  try {
    var ws = BagouWebSocket(WEBSOCKET_URL, {
      open: function() {
        setStatus(ws.readyState);
      },
      close: function() {
        setStatus(ws.readyState);
      },
      events: {
        message: function(msg){
          message('<span class="time">[10-23-20 12:30:33]</span>  <span class="username">' + msg.data.name + '</span> ' + msg.data.text);
          window.scrollTo(0,document.body.scrollHeight);
        }
      }
    });
  } catch(exception) {
    message('<p>Error: ' + exception);
  };

  function message(msg){
    var alerts = document.getElementById('alerts');
    alerts.innerHTML += '<p class="message">' + msg + '</p>';
    if (!focused)
      counter += 1;
      favicon.badge(counter);
  };
  function send(){
    var field = document.getElementById('field');
    ws.emit('message', {'content': field.value});
  };
  function setStatus(status) {
    var statusBar = document.getElementsByClassName('status')[0];
    var statusText = '';
    if (status == 0)
      statusText = 'Connecting';
    else if (status == 1)
      statusText = 'Connected';
    else if (status == 2)
      statusText = 'Disconnecting';
    else if (status == 3)
      statusText = 'Disconnected';
    else
      statusText = 'Unknown';
    statusBar.innerHTML = 'Connection status: ' + statusText;
  };
  // ROOM
  document.getElementById('submit').onclick = function(){
    send();
    document.getElementById('field').value = '';
  };
  document.getElementById('disconnect').onclick = function(){
    ws.close();
    message('Disconnected.');
  };
  document.getElementById('field').onkeypress = function(e) {
    if (e.keyCode == 13) {
      send();
      this.value = '';
    };
  };
  // LOGIN
  function join() {
    var username = document.getElementById('username').value;
    var room = document.getElementById('room').value;
    if (!username || !room)
      return;

    ws.store('username', username, function() {
      ws.subscribe(room);
      ws.auth();
    });

    document.getElementsByClassName('room-name')[0].innerHTML = room;
    document.getElementsByClassName('status')[0].innerHTML += ' | Username: ' + username;

    document.getElementsByClassName('home')[0].style.display = 'none';
    document.getElementsByClassName('room')[0].style.display = '';
    document.getElementById('field').focus();
  };
  document.getElementById('join').onclick = function(){
      join();
  };
  document.getElementById('username').onkeypress = function(e){
    if (e.keyCode == 13)
      join();
  }
  document.getElementById('room').onkeypress = function(e){
    if (e.keyCode == 13)
      join();
  }
  // Other
  window.onfocus = function() {
    focused = true;
    counter = 0;
    favicon.badge(counter);
  }
  window.onblur = function() {
    focused = false;
  }
};
