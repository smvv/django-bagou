BagouWebSocket = function(url, settings, protocols) {
    var ws;
    if (protocols)
        ws = window['MozWebSocket'] ? new MozWebSocket(url, protocols) : window['WebSocket'] ? new WebSocket(url, protocols) : null;
    else
        ws = window['MozWebSocket'] ? new MozWebSocket(url) : window['WebSocket'] ? new WebSocket(url) : null;

    var defaultSettings = {
        open: function(){},
        close: function(){},
        message: function(){},
        options: {},
        events: {}
    };
    // Added extend method to settings Object
    function extend() {
        for(var i=1; i<arguments.length; i++)
            for(var key in arguments[i])
                if(arguments[i].hasOwnProperty(key))
                    arguments[0][key] = arguments[i][key];
        return arguments[0];
    };

    var settings = extend(defaultSettings, settings);

    if (ws) {
        ws.onopen = settings.open;
        ws.onclose = settings.close;
        ws.onmessage = settings.message;
        ws.onmessage = function(e) {
            var m = JSON.parse(e.data);
            var h = settings.events[m.type];
            if (h)
                h.call(this, m);
        };
        ws._send = ws.send;
        ws.send = function(type, data) {
            var m = extend({type: type}, extend({}, settings.open, {type: type}));
            m['data'] = data;
            return this._send(JSON.stringify(m));
        };
        ws.subscribe = function(channel) {
            ws.send('subscribe', {'channel': channel});
        };
        ws.unsubscribe = function(channel) {
            ws.send('unsubscribe', {'channel': channel});
        };
        ws.store = function(key, value) {
            var store = {};
            store[key] = value;
            ws.send('store', store);
        };
        window.onunload = function() {
            ws.onclose();
            ws = null;
        };
    };
    return ws;
};
