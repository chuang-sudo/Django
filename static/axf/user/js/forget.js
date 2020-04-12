$(function () {

    var $username = $('#username_input');
    $username.change(function () {
        var username = $username.val().trim();
        if(username.length){

            $.getJSON('/axf/checkuser/',{'username':username},function (data) {
                console.log(data);

                var $username_info = $('#username_info');

                if (data['status'] === 200){
                    $username_info.html('用户不存在').css({"color":'red'});
                }else if(data['status']===901){
                    $username_info.html('用户存在').css({"color":'green'});
                }
            });
        }
    });

    var $getVerify = $("#getVerify");
    $getVerify.click(function () {
        var username = $username.val().trim();
        if(username.length){
            $.ajax({
                url:'/axf/verifypassword/',
                data:{
                    csrfmiddlewaretoken: $.cookie("csrftoken"),
                    username:username
                },
                method:'post',
                success:function (data) {
                    if(data['status']===400){
                        var $time = $("#time");
                        var seconds = 60;
                        seconds = seconds < data['msg'] ? seconds:data['msg'];
                        clearInterval(caltime);
                        var caltime = setInterval(function () {
                            $time.html(seconds).css({"color":'green'});
                            seconds = seconds -1;
                            if (seconds <=0){
                                clearInterval(caltime);
                                $time.html('');
                            }
                        },1000)
                    }
                    console.log(data);
                }

            })
        }


    })
});

function check() {

    var $username = $('#username_input');
    if (!$username.val().trim()){
        return false
    }
    var info_color = $('#username_info').css('color');

    if (info_color == 'rgb(255, 0, 0)'){
        return false
    }

    var $password_input = $('#password_input');
    var $password_confirm_input = $('#password_confirm_input');

    var password = $password_input.val().trim();
    var password_confirm_input = $password_confirm_input.val().trim();

    $password_input.val(md5(password));
    $password_confirm_input.val(md5(password_confirm_input));
    password = $password_confirm_input.val().trim() ;
    password_confirm_input = $password_input.val().trim();

    return password ===password_confirm_input

}