function isReady(callback) {
  var readyStateCheckInterval = setInterval(function() {
      if (document.readyState === "complete") {
          if (callback) callback();
          clearInterval(readyStateCheckInterval);
      }
  }, 10);
}

function loadChat() {
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
  };
  function send(){
    var field = document.getElementById('field');
    ws.emit('message', field.value);
  };
  function setStatus(status) {
    var statusBar = document.getElementsByClassName('status')[0];
    statusBar.innerHTML = 'Socket status: ' + status;
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
    ws.store('username', username, function() {
      ws.subscribe(room);
      ws.auth();
    });

    document.getElementsByClassName('room-name')[0].innerHTML = room;
    document.getElementsByClassName('status')[0].innerHTML += ' | Username: ' + username;

    document.getElementsByClassName('home')[0].style.display = 'none';
    document.getElementsByClassName('room')[0].style.display = '';
  };
  document.getElementById('join').onclick = function(){
    join();
  };
  document.getElementById('room').onkeypress = function(e){
    if (e.keyCode == 13) {
      join();
    }
  }
};
