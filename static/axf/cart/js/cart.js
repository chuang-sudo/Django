$(function () {



    $(".addShopping").click(function () {

        var $add = $(this);
        var c_id = $add.attr('ga');

        $.ajax({
            url: '/axf/changecartstate/',

            data: {
                o_type: 'add',
                c_id: c_id,
                csrfmiddlewaretoken: $.cookie("csrftoken")
            },

            method: 'post',

            success: function (data) {
                console.log(data);
                if (data['status'] === 200) {
                    if (data['is_all_select']) {
                        $(".all_select").html("√")
                    } else {
                        $(".all_select").html("")
                    }

                    $add.prev('span').html(data['num']);

                    $(".sum_money").html(data['sum_price'])
                }
            }
        })
    });

    $(".subShopping").click(function () {
        var $sub = $(this);
        var c_id = $sub.attr("ga");
        var num = Number($sub.next('span').html().trim());
        console.log(num);
        if (num > 0) {
            $.ajax({
                url: '/axf/changecartstate/',
                data: {
                    o_type: 'sub',
                    c_id: c_id,
                    csrfmiddlewaretoken: $.cookie("csrftoken")
                },
                method: 'post',
                success: function (data) {
                    console.log(data);
                    if (data['is_all_select']) {
                        $(".all_select").html("√")
                    } else {
                        $(".all_select").html("")
                    }
                    if(data['num']>0){
                        $sub.next('span').html(data['num'])
                    }else {
                        $sub.parent().parent('li').remove()
                    }

                    $(".sum_money").html(data['sum_price'])

                }
            })
        }


    });

    //点击商品选中按钮
    $(".is_select").click(function () {
        var $c_btn = $(this);
        var c_id = $c_btn.attr("ga");
        $.ajax({
            url: '/axf/changecartstate/',
            data: {
                o_type: 'change',
                c_id: c_id,
                csrfmiddlewaretoken: $.cookie("csrftoken")
            },
            method: "post",
            success: function (data) {
                console.log(data);

                if (data['status'] === 200) {
                    //改变总价
                    // $("#sum_money").html(data['money']);
                    //改当前商品的状态
                    if (data['is_select']) {
                        $c_btn.html("√");
                    } else {
                        $c_btn.html("");
                    }

                    if (data['is_all_select']) {
                        $(".all_select").html("√")
                    } else {
                        $(".all_select").html("")
                    }

                    $(".sum_money").html(data['sum_price'])

                } else {

                }
            }
        })
    });

    //点击全选按钮
    $(".all_select").click(function () {
        var $all_select = $(this);

        var select_list = [];
        var unselect_list = [];

        $(".is_select").each(function () {
            var $is_select = $(this);
            var cartid = $is_select.attr('ga');

            if ($is_select.html().trim()) {
                select_list.push(cartid)
            } else {
                unselect_list.push(cartid)
            }
        });

        if (unselect_list.length > 0) {//有未勾选的
            $.ajax({
                url: '/axf/allselect/',
                data: {
                    cart_list: unselect_list.join("#"),
                    csrfmiddlewaretoken: $.cookie("csrftoken")
                },
                method: "post",
                success: function (data) {
                    console.log(data);
                    if (data['status'] === 200) {

                        if (data['is_all_select']) {
                            $(".all_select").html("√")
                        } else {
                            $(".all_select").html()
                        }

                        $(".is_select").each(function () {
                            $(this).html("√")
                        });

                        $(".sum_money").html(data['sum_price'])
                    }
                }
            })
        } else if (select_list.length > 0) {//全部勾选 and 存在数据
            $.ajax({
                url: '/axf/allselect/',
                data: {
                    cart_list: select_list.join("#"),
                    csrfmiddlewaretoken: $.cookie("csrftoken")
                },
                method: "post",
                success: function (data) {
                    console.log(data);
                    if (data['status'] === 200) {

                        if (data['is_all_select']) {
                            $(".all_select").html("√")
                        } else {
                            $(".all_select").html("")
                        }

                        $(".is_select").each(function () {
                            $(this).html("")
                        });

                        $(".sum_money").html(data['sum_price'])
                    } else {

                    }
                }
            })
        }


    });

    $("#ok").click(function () {
        //判断商品是否选中
        var select_list =[];
        $(".is_select").each(function () {
            var $is_select = $(this);
            var cartid = $is_select.attr('ga');

            if ($is_select.html().trim()) {
                select_list.push(cartid)
            }
        });
        if(select_list.length === 0){
            return
        }

        $.ajax({
            url:"/axf/makeorder/",
            data:{
                cart_ids:select_list.join('#'),
                csrfmiddlewaretoken: $.cookie("csrftoken")
            },
            method:"post",
            success:function (data) {
                if(data['status']===200){
                    console.log(data);
                     $(".is_select").each(function () {
                            var $is_select = $(this);

                            if ($is_select.html().trim()) {
                                $is_select.parent().parent('li').remove()
                            }
                     });
                    window.open('/axf/orderdetail/?orderid='+data['orderid'],target='_self')
                }
            }
        })
    })
});