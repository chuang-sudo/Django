$(function () {

    var $username = $('#username_input');
    $username.change(function () {
        var username = $username.val().trim();
        if(username.length){

            $.getJSON('/axf/checkuser/',{'username':username},function (data) {
                console.log(data);

                var $username_info = $('#username_info');

                if (data['status'] === 200){
                    $username_info.html('用户名可用').css({"color":'green'});
                }else if(data['status'] === 901){
                    $username_info.html('用户已存在').css({'color':'red'});
                }
            });
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