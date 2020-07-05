$(function () {
    // jquery绑定标签a的click点击时间
    $('.hometitle a').click(function () {
        // 查看当前a标签的标签内容
        recommend_name = $(this).text();
        // 发送ajax请求
        $.ajax({
            // 路径
            'url':'/recommend',
            // 请求方式
            'type':'get',
            // 携带的数据
            'data': {'recommend_name': recommend_name},
            // 返回的数据格式
            'dataType':'json',
            'async':false,
        }).success(function (recommend) {
            // 成功获取返回值
            recommend_posts = recommend.posts;
        });
        return recommend_posts
    })
});