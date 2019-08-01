// 初始化函数
function start() {
    // 发布动态
    $(".circle-post-btn").click(function () {
        $.ajax({
            url: '/circle/new/',
            data: $("#circle-form").serialize(),
            type: 'POST',
            cache: false,
            success: function (data) {
                if (data.status === 3002) {
                    window.location.href = '/accounts/login'
                }
                $('.append-single-hr').after(data);
                $('#message-text').val("");

                reload_bind()
            },
            error: function (data) {
                alert('发布失败');
            },
        });
    });
    // 点赞
    $(".like-symbol").click(function () {
        var circle_id = $(this).parent().attr("circle-id")
        var nums = $(this).attr('class');
        node = $(this);
        $.ajax({
            url: "/circle/like/",
            data: {'uuid': circle_id},
            type: "POST",
            cache: false,
            success: function (data) {
                if (data.status === 3002) {
                    window.location.href = '/accounts/login'
                }
                else {
                    if (nums.includes('move-hand')) {
                        node.removeClass("move-hand")
                        node.removeClass("zi_love")
                        node.addClass("zi_loves")
                    } else {
                        node.removeClass("zi_loves")
                        node.addClass("move-hand")
                        node.addClass("zi_love")
                    }
                    console.log(data.like_num)
                    node.siblings('.like-num').text(data.like_num);
                }


            },
            error: function (data) {
                alert('fail')
            }
        })
    })

    // 删除动态操作
    $('.my-delete-circle').click(function () {
        var r = confirm("确定删除动态？！")
        if (r === false) {
            return false
        }
        var circle_id = $(this).parent().attr('circle-id');
        var node = $(this).parent()
        $.ajax({
            url: "/circle/delete/",
            data: {'uuid': circle_id},
            type: "POST",
            cache: false,
            success: function (data) {
                if (data.status === 3002) {
                    window.location.href = '/accounts/login'
                }
                if (data.status === 2000) {
                    node.remove()
                }

            },
            error: function (data) {
                alert('fail')
            }
        })
    });

    //打开回复
    $('.reply').click(function () {
        var node = $(this);
        var circle_id = $(this).parent().attr('circle-id')
        $.ajax({
            url: "/circle/getreply/",
            data: {'uuid': circle_id},
            type: "POST",
            cache: false,
            success: function (data) {
                if (data.status === 3002) {
                    window.location.href = '/accounts/login'
                }
                if (data.status === 2000) {
                    $('#reply-list').html("");
                    $('#reply-list').append(data.html_text)
                    reload_bind()
                }

            },
            error: function (data) {
                alert('fail')
            }
        })
    });

    //发送回复
    $(".post-reply").click(function () {
        var text = $(".post-reply-message").val();
        var circle_id = $(this).attr("uuid");
        $.ajax({
            url: "/circle/reply/",
            data: {'uuid': circle_id, 'text': text},
            type: "POST",
            cache: false,
            success: function (data) {
                if (data.status === 2000) {
                    //评论之后关闭模态框
                    $('#exampleModalLong').modal("hide")
                }

            },
            error: function (data) {
                alert('fail')
            }
        })


    });
}
// 重新绑定函数
function reload_bind(){
    $('.post-reply').unbind();
    $('.my-delete-circle').unbind();
    $(".like-symbol").unbind();
    $('.circle-post-btn').unbind();
    $('.reply').unbind()
    start()
}
start()

