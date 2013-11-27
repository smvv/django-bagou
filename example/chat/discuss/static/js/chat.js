function isReady(callback) {
  var readyStateCheckInterval = setInterval(function() {
      if (document.readyState === "interactive") {
          if (callback) callback();
          clearInterval(readyStateCheckInterval);
      }
  }, 10);
}

isReady(function() {
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
    ws.send('message', field.value);
  };
  function setStatus(status) {
    var statusBar = document.getElementsByClassName('status')[0];
    statusBar.innerHTML = '| Socket status: ' + status;
  };
  // ROOM
  document.getElementById('submit').onclick = function(){
    message('Waiting for response from server');
    send();
    document.getElementById('field').value = '';
  };
  document.getElementById('disconnect').onclick = function(){
    ws.send('message', "I'm disconnected.");
    ws.close();
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
    ws.subscribe(room);
    ws.store('username', username);

    document.getElementsByClassName('room-name')[0].innerHTML = room;
    document.getElementsByClassName('status')[0].innerHTML += '<br />| Username: ' + username;

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
});
