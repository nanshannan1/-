$(function () {
    var is_email = false;
    var is_code = false;

    $("#email").blur(function () {
        var email = $("#email").val();
        var re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;
        if (email.length==0){
             $("#b").fadeIn("slow", function () {
                $("#b").fadeOut(3000)
            });
             is_email = true;
        } else {

            if (re.test(email)){
            //
            } else {
                $("#b").fadeIn("slow", function () {
                    $("#b").fadeOut(3000)
                });
                is_email = true;
            }


        }
    });

    $("#cc").click(function () {

        if (is_email==false){
            var email = $("#email").val();
            alert(email);
            $.get('/users/send_verify/?email='+email, function (data) {
                if (data.news==1) {
                    $("#c1").fadeIn("slow", function () {
                        $("#c1").fadeOut(3000)
                    });

                }else {
                    $("#c2").fadeIn("slow", function () {
                        $("#c2").fadeOut(3000)
                    });
                }
            })
        }
    });

    $("#code").blur(function () {
        var code = $("#code").val();
        if (code.length==0){
            $("#c3").fadeIn("slow", function () {
                $("#c3").fadeOut(3000)
            });

        } else {
            $.get("/users/check_verify/?verify="+code, function (data) {
                if (data.news==1) {
                    $("#c3").fadeIn("slow", function () {
                        $("#c3").fadeOut(3000)
                    });
                }else {
                    is_code = true;
                }
            })
        }
    });

    $("#tj").click(function () {
        if (is_email==false && is_code==true){
            window.location.href='/users/get_alert_pwd/'
        }
    });




});