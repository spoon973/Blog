$(function () {
    $oPic = $('.pics');
    $oUl = $oPic.find('ul')[0];
    $oUl.innerHTML += $oUl.innerHTML;

    var iLeft = 0;
    iSpeed = 0;
    var iNowspeed = 0;

    $('.category_skip').click(function () {
        category_name = $(this).html();
        $.ajax({
            'url': '/index_category',
            'type': 'get',
            'data': {'category_name': category_name},
            'dataType': 'json',
        });
        setTimeout(function () {
            window.location.reload();
        },100);
    });
    // 设置鼠标移入时静止状态
    $oPic.mouseover(function() {
        // 先获取鼠标移入前iSpeed的状态值
        iNowspeed = iSpeed;
        iSpeed = 0;
    });

    // 设置鼠标移出时的继续状态
    $oPic.mouseout(function() {
        iSpeed = iNowspeed;
    });

    // 创建定时器,使用匿名函数
    var timer = setInterval(function() {
        iLeft += iSpeed;
        // 当ul向左滚动到第6个li时，瞬间将整个ul拉回到初始位置
        if (iLeft < -1100 ) {
            iLeft = 0;
        }else if(iLeft > 0) {
            iLeft = -1100;
        }
        $oUl.style.left = iLeft + 'px';
    },15);
});