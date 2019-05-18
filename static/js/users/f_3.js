$(function () {
    var is_new = false;
    var is_old = false;

    $("#new_pwd").blur(function () {
        var new_pwd = $("#new_pwd").val();
        if (new_pwd.length<6 || new_pwd>16) {

            $("#a").fadeIn("slow", function () {
                $("#a").fadeOut(3000)
            });

        }else {
            is_new = true;
        }

    });


    $("#check_pwd").blur(function () {
        var new_pwd = $("#new_pwd").val();
        var check_pwd = $("#check_pwd").val();

        if (new_pwd!==check_pwd){

            $("#aa").fadeIn("slow", function () {
                $("#aa").fadeOut(3000)
            });

        } else {
            is_old = true;
        }

    });
    alert(is_new, is_old);

    $("#tj").click(function () {
        if (is_new==true && is_old==true){
            var data = {
                pwd: $("#new_pwd").val(),
                csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()
            };
            $.post("/users/post_alert_pwd/", data, function (data) {
                if (data.news==1){
                    window.location.href='/users/alert_ok/'
                }else {
                    $("#aaa").fadeIn("slow", function () {
                        $("#aaa").fadeOut(3000)
                    });
                }
            });


        }
    })

})