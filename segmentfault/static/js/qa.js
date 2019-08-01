function start() {
    $(".up-vote").click(function () {
        var node = this;
        var qa_id = $(node).parent().attr('qa-id');
        if ($(node).attr('nature') === 'active'){
            var vote = 'neutral'
        }
        else{
            var vote = 'up'
        }
        $.ajax({
            url:"/qa/vote/",
            data:{"vote":vote,'id':qa_id},
            type:"POST",
            cache:false,
            success:function (data) {
                if (data.status === 3002){
                    window.location.href = '/accounts/login'
                }
                if (data.status === 2000){
                    // 变色操作
                    if (vote === 'up'){
                        var color = '#1afa29'
                    }
                    else{
                        var color = '#bfbfbf'
                    }

                    $(node).children().attr('fill',color);

                    // 改变状态操作，nature状态决定ajax的参数
                    if ($(node).attr('nature') === 'active'){
                        var nature = 'none'
                    }
                    else{
                        var nature = 'active'
                    }
                    $(node).attr('nature',nature)

                    // 改变对应点击按钮的状态
                    var sbnode = $(node).parent().parent().find('.down-vote')
                    if ($(sbnode).attr('nature') === 'active'){
                        $(sbnode).attr('nature','none')
                        $(sbnode).children().attr('fill','#bfbfbf')
                    }
                    // 改变投票数
                    $(node).parent().parent().find('.vote-nums').children().html(data.vote_num)

                }
            }
        })
    });

    $(".down-vote").click(function () {
        var node = this;
        var qa_id = $(node).parent().attr('qa-id');
        if ($(node).attr('nature') === 'active'){
            var vote = 'neutral'
        }
        else{
            var vote = 'down'
        }
        $.ajax({
            url:"/qa/vote/",
            data:{"vote":vote,'id':qa_id},
            type:"POST",
            cache:false,
            success:function (data) {
                if (data.status === 3002){
                    window.location.href = '/accounts/login'
                }
                if (data.status === 2000){
                    if (vote === 'down'){
                        var color = '#515151'
                    }
                    else{
                        var color = '#bfbfbf'
                    }
                    console.log(color)
                    $(node).children().attr('fill',color)
                    if ($(node).attr('nature') === 'active'){
                        var nature = 'none'
                    }
                    else{
                        var nature = 'active'
                    }
                    $(node).attr('nature',nature)

                    var sbnode = $(node).parent().parent().find('.up-vote')
                    if ($(sbnode).attr('nature') === 'active'){
                        $(sbnode).attr('nature','none')
                        $(sbnode).children().attr('fill','#bfbfbf')
                    }
                    $(node).parent().parent().find('.vote-nums').children().html(data.vote_num)


                }
            }
        })
    });

    $(".answer-up-vote").click(function () {
        var node = this;
        var answer_id = $(node).parent().attr('qa-id');
        if ($(node).attr('nature') === 'active'){
            var vote = 'neutral'
        }
        else{
            var vote = 'up'
        }
        $.ajax({
            url:"/qa/answer/vote/",
            data:{"vote":vote,'id':answer_id},
            type:"POST",
            cache:false,
            success:function (data) {
                if (data.status === 3002){
                    window.location.href = '/accounts/login'
                }
                if (data.status === 2000){
                    // 变色操作
                    if (vote === 'up'){
                        var color = '#1afa29'
                    }
                    else{
                        var color = '#bfbfbf'
                    }

                    $(node).children().attr('fill',color);

                    // 改变状态操作，nature状态决定ajax的参数
                    if ($(node).attr('nature') === 'active'){
                        var nature = 'none'
                    }
                    else{
                        var nature = 'active'
                    }
                    $(node).attr('nature',nature)

                    // 改变对应点击按钮的状态
                    var sbnode = $(node).parent().parent().find('.answer-down-vote')
                    if ($(sbnode).attr('nature') === 'active'){
                        $(sbnode).attr('nature','none');
                        $(sbnode).children().attr('fill','#bfbfbf')
                    }
                    // 改变投票数
                    $(node).parent().parent().find('.vote-nums').html(data.vote_num)

                }
            }
        })
    });

    $(".answer-down-vote").click(function () {
        var node = this;
        var answer_id = $(node).parent().attr('qa-id');
        if ($(node).attr('nature') === 'active'){
            var vote = 'neutral'
        }
        else{
            var vote = 'down'
        }
        $.ajax({
            url:"/qa/answer/vote/",
            data:{"vote":vote,'id':answer_id},
            type:"POST",
            cache:false,
            success:function (data) {
                if (data.status === 3002){
                    window.location.href = '/accounts/login'
                }
                if (data.status === 2000){
                    if (vote === 'down'){
                        var color = '#515151'
                    }
                    else{
                        var color = '#bfbfbf'
                    }
                    console.log(color);
                    $(node).children().attr('fill',color);
                    if ($(node).attr('nature') === 'active'){
                        var nature = 'none'
                    }
                    else{
                        var nature = 'active'
                    }
                    $(node).attr('nature',nature);

                    var sbnode = $(node).parent().parent().find('.answer-up-vote');
                    if ($(sbnode).attr('nature') === 'active'){
                        $(sbnode).attr('nature','none');
                        $(sbnode).children().attr('fill','#bfbfbf')
                    }
                    $(node).parent().parent().find('.vote-nums').html(data.vote_num)


                }
            }
        })
    });

    $('.answer-accept').click(function () {
        var node = this;
        if ($('.qa-accept').html() === 'True'){
            return
        }
        console.log($('.qa-accept').html())
        var answer_id = $(node).parent().attr('qa-id');

        $.ajax({
            url:'/qa/accept/',
            data:{'answer_id':answer_id},
            type:"POST",
            cache:false,
            success:function (data) {
                if (data.status === 3002){
                    window.location.href = '/accounts/login'
                }
                if (data.status === 2000){
                    $(node).children().children().attr('fill','#1296db');
                    $('.qa-accept').html('True')
                }
            }
        })

    })

}
start();
// #bfbfbf 灰色
// #1afa29 绿色
// #515151 黑色
