$(function () {

     var error_email = true;
     var error_name = true;
     var error_pwd = true;
     var error_verify = true;
     var error_allow = true;
     $('#email').blur(function () {
        var re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;
        var len = $('#email').val().length;
        if (len != 0){
            if(re.test($('#email').val()))
            {
                $.get('/users/email_exist/?email='+$('#email').val(), function (data) {
                    if(data.count != 0){
                        $('#email').next().html('*该邮箱已被注册').show();
                        // $("#submit").attr("disabled",true)
                    }else {
                        $('#email').next().hide();
                        error_email = false;

                    }
                });
            }
            else
            {
                $('#email').next().html('*邮箱格式错误').show();
                // $("#submit").attr("disabled",true)
            }

        }else {
            $('#email').next().html('*邮箱不能为空').show();
            // $("#submit").attr("disabled",true)
        }
    });

     // 检测用户名
    $("#user_name").blur(function () {
        var user_name = $("#user_name").val();
        var len = $("#user_name").val().length;
        if (len != 0) {
            if (user_name.length<2||user_name.length>10){
                $('#user_name').next().html('请输入2-10个字符的用户名').show()
                // $("#submit").attr("disabled",true)
            }else {
                $.get('/users/name_exist/?user_name='+$('#user_name').val(), function (data) {
                    if (data.count != 0){
                        $('#user_name').next().html('*用户名以被注册').show();
                        // $("#submit").attr("disabled",true)
                    } else {
                        $('#user_name').next().hide();
                        error_name = false;
                    }
                })
            }
        }else {
            $('#user_name').next().html('*用户名不能为空').show();
            // $("#submit").attr("disabled",true)
        }


    });

    // 验证用户的密码
    $('#pwd').blur(function () {
        var len = $('#pwd').val().length;
        if (len != 0){
            if (len<6 || len>16) {
                $('#pwd').next().html("*请输入6-16位的字符").show();
                // $("#submit").attr("disabled",true)
            }else {
                $('#pwd').next().hide();
                error_pwd = false;
            }

        }else {
            $('#pwd').next().html("*密码不能为空").show();
            // $("#submit").attr("disabled",true)
        }

    });

    // 获取验证码
    $("#gain_verify").click(function () {
        if (error_email==false) {
            $.get('/users/send_verify/?email=' + $('#email').val(), function (data) {
                if (data.news == 1){
                    // 验证码发送成功
                    let count=60;
                    const countDown = setInterval(() => {
                    if (count == 0) {
                        $("#gain_verify").val('重新发送').removeAttr('disabled');
                        $("#gain_verify").css({ background: '#1c9DC6', color: '#fff',});
                        clearInterval(countDown);
                    }
                    else {
                        $("#gain_verify").attr('disabled', true);
                        $("#gain_verify").css({background: '#d8d8d8',color: '#707070', });
                        $("#gain_verify").val(count + '秒后可重新获取');}count--;},
                        1000);
                }else if (data.news == 0){
                    // 网络出现问题
                }
            })
        } else {
            $('#gain_verify').next().html("请输入邮箱").show();
        }



    });

    // 校验验证码
    $("#verify").blur(function () {
        var len = $('#verify').val().length;
        if (len != 0){
            $.get("/users/check_verify/?verify=" + $("#verify").val(), function (data) {
                if (data.news == 0){
                    $('#gain_verify').siblings(".error_tip1").hide();
                    error_verify = false;
                }else {
                    $('#gain_verify').siblings(".error_tip1").html("*验证码输入错误").show();
                    // $("#submit").attr("disabled",true)
                }
            })
        }else {
            $('#gain_verify').siblings(".error_tip1").html("*验证码不能为空").show();
            // $("#submit").attr("disabled",true)
        }



    });
    // 同意用户使用协议
    $('#allow').click(function() {
		if($(this).is(':checked'))
		{
			$(this).siblings('span').hide();
			error_allow = false;
		}
		else
		{
			$(this).siblings('span').html('请勾选同意').show();
			// $("#submit").attr("disabled",true)
		}
	});
    // 最后的提交
    $("#form1").submit(function () {
        if (error_email == false && error_name == false && error_pwd == false &&
            error_verify == false && error_allow == false) {
            $("#submit").attr("disabled",false);
        } else {
            $("#submit").attr("disabled", true)
        }
    })



















});