/* Project specific Javascript goes here. */

function lighter() {
        $('.zi_bell').addClass('zi_bells');
        $('.zi_bell').removeClass('zi_bell');
}

function pstart() {


    if (username !== 'AnonymousUser'){
        // WebSocket连接
        const ws_scheme = "ws"; // 暂时不考虑 https + wss
        const ws_path = ws_scheme + "://" + window.location.host + "/ws/notice/";
        const ws = new ReconnectingWebSocket(ws_path); // 实例化websocket
        // 监听后端发送过来的消息
        ws.onmessage = function (event) {
            const data = JSON.parse(event.data);
            console.log(data.message)
            // 避免其他用户的私信也出现在聊天框中
            // var active_user = $('.active-user').attr('user-name');
            // if (data.sender === active_user ){
            //     $('.pre-scrollable').append(data.message);
            //     scroll_to_top();
            // }
            lighter();
    }



    }
}




pstart();
