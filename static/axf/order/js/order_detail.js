$(function () {
    $("#alipay").click(function () {
        var total_price = $("#total_price").html() ;
        $.ajax({
            url:'/axf/check_alipay/',
            data :{
                total_price:total_price,
                csrfmiddlewaretoken: $.cookie("csrftoken")
            },
            method:'post',
            success:function (data) {
                console.log(data);
                if(data['status']===200){
                    window.open('/axf/alipay/?total_price='+data['total_price'])
                }
            }

        })
    })
});