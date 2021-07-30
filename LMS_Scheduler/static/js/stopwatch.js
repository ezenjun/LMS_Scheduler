var time = 0;
var starFlag = true;
$(document).ready(function(){
  buttonEvt();
});

function init(){
  document.getElementById("time").innerHTML = "00시간 00분 00초";
}

function buttonEvt(){
  var hour = 0;
  var min = 0;
  var sec = 0;
  var timer;

  // start btn
  $("#startbtn").click(function(){

    if(starFlag){
      $(".fa").css("color","#333")
      this.style.color = "green";
      starFlag = false;

      if(time == 0){
        init();
      }

      timer = setInterval(function(){
        time++;

        min = Math.floor(time/60);
        hour = Math.floor(min/60);
        sec = time%60;
        min = min%60;

        var th = hour;
        var tm = min;
        var ts = sec;
        if(th<10){
        th = "0" + hour;
        }
        if(tm < 10){
        tm = "0" + min;
        }
        if(ts < 10){
        ts = "0" + sec;
        }

        document.getElementById("time").innerHTML = th + "시간 " + tm + "분 " + ts + "초";
      }, 1000);
    }
  });

  // pause btn
  $("#pausebtn").click(function(){
    if(time != 0){
      $(".fa").css("color","#333")
      this.style.color = "yellow";
      clearInterval(timer);
      starFlag = true;
    }
  });

  // stop btn
  $("#stopbtn").click(function(){
    if(time != 0){
      $(".fa").css("color","#333")
      this.style.color = "red";
      clearInterval(timer);
      starFlag = true;
      $.ajax({
        type: 'POST',
        url: "/lms/test",
        headers:{
          'X-CSRFToken' : '{{csrf_token}}'
        },
        data: JSON.stringify({'time': time }),
        dataType: "text",
        success: function (data) {
          console.log('성공');
        },
        error: function (data) {
          console.log('실패');
          console.log(request);
          console.log(error);
        }
      });
      
      time = 0;
      init();
    }
  });
}
