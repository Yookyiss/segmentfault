function scroll_to_top(){
    $('.pre-scrollable').scrollTop($('.pre-scrollable')[0].scrollHeight);
}

function start() {
    scroll_to_top(); //滚动到底
    $('.send-letter').click(function () {
        var recipient_id = $("#recipient").attr('recipient-id');
        var message = $('.reply-input').val();
        $.ajax({
            url: "/msg/post-letter/",
            data: {'recipient':recipient_id, 'message':message},
            type: "POST",
            cache: false,
            success: function (data) {
                if (data.status === 2000) {
                    //评论之后关闭模态框
                    $('.pre-scrollable').append(data.htmlslice)
                    $('.reply-input').val('')
                    scroll_to_top();
                }
                if (data.status === 3002) {
                    window.location.href = '/accounts/login'
                }
                if (data.status === 5000) {
                    alert(data.msg)
                }
            },
            error: function (data) {
                alert('服务器错误')
            }
        })
    })
    // WebSocket连接
    const ws_scheme = "ws"; // 暂时不考虑 https + wss
    const ws_path = ws_scheme + "://" + window.location.host + "/ws/" + currentUser + "/";
    const ws = new ReconnectingWebSocket(ws_path); // 实例化websocket
    // 监听后端发送过来的消息
    ws.onmessage = function (event) {
        const data = JSON.parse(event.data);

        // 避免其他用户的私信也出现在聊天框中
        var active_user = $('.active-user').attr('user-name')
        if (data.sender === active_user ){
            $('.pre-scrollable').append(data.message);
            scroll_to_top();
        }

    }


}




start()
