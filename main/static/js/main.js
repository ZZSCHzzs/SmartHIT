$(document).ready(function() {
    var navbar = $(".navbar");
    var headerOffset = navbar.offset().top;
    var headerHeight = navbar.outerHeight();

    $(window).scroll(function() {
        var scrollPosition = $(this).scrollTop();

        // 检查页面滚动位置是否超过导航栏原始位置
        if (scrollPosition >= headerOffset) {
            navbar.addClass("fixed-top");
            $(".index_root").css("padding-top", 80); // 为body添加与导航栏高度相同的padding-top，避免内容跳动
        } else {
            navbar.removeClass("fixed-top");
            $(".index_root").css("padding-top", 0); // 如果导航栏不固定，移除body的padding-top
        }
    });
});
