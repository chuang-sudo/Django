$(function () {
/****************************折叠按钮************************/
    //全部类型标签的点击事件
    var is_down = true;
    var is_sort_down = true;


    $("#alltypebtn").click(function () {
        $("#typediv").toggle();
        // 判断is_down的状态
        if(!is_sort_down){
            $("#sortdiv").toggle();
            is_sort_down = change_sort_status(is_sort_down);
        }
        is_down = change_type_status(is_down);
    });


    $("#typediv").click(function () {
        $(this).toggle();
        is_down = change_type_status(is_down);
    });


    $("#showsortbtn").click(function () {
        $("#sortdiv").toggle();
        if(!is_down){
            $("#typediv").toggle();
            is_down = change_type_status(is_down);
        }
        is_sort_down = change_sort_status(is_sort_down);
    });


    $("#sortdiv").click(function () {
        $(this).toggle();
        is_sort_down = change_sort_status(is_sort_down);
    });

/*************************(+,-)进购物车******************************/
    //给商品的加号添加点击事件
    $(".addShopping").click(function () {
        //prop 只能获得系统的属性 无法获得自定属性的值
        var g_id = $(this).attr('g_id');
        // console.log(g_id);
        //记录当前点击的按钮元素
        var $current_btn = $(this);

        //发送请求给后端
        $.ajax({
            url:"/axf/addtocart/",

            data:{
                g_id: g_id,
                opreate_type:"add",
                //通过DJANGO的csrf校验
                csrfmiddlewaretoken: $.cookie("csrftoken")
            },

            method:"post",

            success:function (data) {
                console.log(data);
                if (data['status']==200) {
                    var num = data['num'];
                    console.log(num);
                    //拿到加号前边的那个span标签 更新商品的数量
                    $current_btn.prev().html(num);
                }
                else if (data['status']==302){
                    //如果没登陆 需要跳转到登录页面
                    window.open(url='/axf/login/', target="_self");
                }

            }
        })
    });


    // 给商品的减号添加点击事件
    $(".subShopping").click(function () {
        //prop 只能获得系统的属性 无法获得自定属性的值
        var g_id = $(this).attr('g_id');
        var $current_btn = $(this);
        //商品数量是0 点操作不允许
        if ($(this).next().html() == 0) {
            return;
        }
        $.ajax({
            url:"/axf/addtocart/",
            data:{
                g_id: g_id,
                opreate_type:"sub",
                csrfmiddlewaretoken: $.cookie("csrftoken")
            },
            method:"post",
            success:function (data) {
                console.log(data);
                if (data['status']==200) {
                    var num = data['num'];
                    //更新商品的数量
                    $current_btn.next().html(num);
                }
                else if (data['status']==302){
                    //如果没登陆 需要跳转到登录页面
                    window.open(url='/axf/login/', target="_self");
                }

            }
        })
    });
});

function change_type_status(is_down) {
    if (is_down){
            $("#alltypebtn").find("span").removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-up");
            is_down = false;
        } else {
            $("#alltypebtn").find("span").removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");
            is_down = true;
        }
    return is_down;
}

function change_sort_status(is_down) {
    if (is_down){
            $("#showsortbtn").find("span").removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-up");
            is_down = false;
        } else {
            $("#showsortbtn").find("span").removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");
            is_down = true;
        }
    return is_down;
}