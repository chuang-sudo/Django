$(function () {
    $("#not_pay").click(function () {
        window.open('/axf/orderlistnotpay/',target="_self")
    });

    $("#not_receive").click(function () {
        window.open('/axf/orderlistnotreceive/',target="_self")
    })
});