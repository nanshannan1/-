$(function () {

    $("#username").blur(function () {
        var name = $("#username").val();
        if (name.length==0){
            alert("用户名不能为空");
            // $(".input_submit").attr("disabled",false)
        } else{
            $.get('/users/name_exist/?user_name='+name, function (data) {
                if (data.count==1){
                    // $(".input_submit").attr("disabled", true)
                } else {
                    // $(".input_submit").attr("disabled",false);
                    alert("用户名不存在");
                }
            })

        }
    });

    $("#pwd").blur(function () {
        var pwd = $("#pwd").val();
        if (pwd.length==0){
            alert("请输入密码")
        }
    })

});