$(function () {
    $('a').click(function () {
        var $a = $(this);
        var orderid = $a.attr('orderid');
        window.open('/axf/orderdetail/?orderid='+orderid,target="_self")
    })
});