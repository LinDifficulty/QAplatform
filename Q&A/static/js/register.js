function bindEmailCaptchaClick(){

    $("#captcha-btn").click(function (event){
        var $this = $(this)
        //阻止默认的事件
        event.preventDefault();

        var email = $("#exampleInputEmail1").val();
        $.ajax({
            url:"/auth/captcha/email?email="+email,
            method:"GET",
            success:function (result){
                var code=result['code'];
                if(code == 200){
                    var countdown = 60;
                    //取消点击时间
                    $this.off("click");
                    var timer = setInterval(function (){
                        $this.text(countdown);
                        countdown-=1;
                        if(countdown<=0){
                            //清掉定时器
                            clearInterval(timer)
                            //重置按钮
                            $this.text("获取验证码");
                            //重新绑定点击事件
                            bindEmailCaptchaClick()
                        }
                    },1000);
                }else{
//                    alert(result['message'])
                }
            },
            fail:function (error){
                console.log(error)
            }
        })
        alert("验证码发送成功!")
    })


}

//待网页完全加载后再执行
$(function () {
    bindEmailCaptchaClick()
});