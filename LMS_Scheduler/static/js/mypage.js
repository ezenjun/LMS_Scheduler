function openCity(evt, cityName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(cityName).style.display = "flex";
    evt.currentTarget.className += " active";
}

var acc = document.getElementsByClassName("accordion");
var i;

for (i = 0; i < acc.length; i++) {
  acc[i].addEventListener("click", function() {
    /* Toggle between adding and removing the "active" class,
    to highlight the button that controls the panel */
    this.classList.toggle("active");

    /* Toggle between hiding and showing the active panel */
    var panel = this.nextElementSibling;
    if (panel.style.display === "block") {
      panel.style.display = "none";
    } else {
      panel.style.display = "block";
    }
  });
}


  // Get the element with id="defaultOpen" and click on it
document.getElementById("defaultOpen").click();

  /*var btnContainer = document.getElementById("buttons");
  var btns = btnContainer.getElementsByClassName("btn");
  for (var i = 0; i < btns.length; i++) {
    btns[i].addEventListener("click", function() {
      var current = document.getElementsByClassName("active");
      var activeid
      // If there's no active class
      if (current.length > 0) {
        current[0].className = current[0].className.replace(" active", "");
        activeid = current[0].id
      }
  
      // Add the active class to the current/clicked button
      this.className += " active";
    });
  }*/




  $(document).ready(function(){
    buttonEvt();
  });


  function buttonEvt(){
    $("#1").click(function(){
        $.ajax({
            type: 'POST',
            url: "/account/usertype",
            headers:{
            'X-CSRFToken' : '{{csrf_token}}'
            },
            data: JSON.stringify({'usertype': '1' }),
            dataType: "text",
            success: function (data) {
                console.log('성공');
            },
            error: function (data) {
            console.log('실패');
            console.log(error);
            }
        });
    });

    $("#2").click(function(){
        $.ajax({
            type: 'POST',
            url: "/account/usertype",
            headers:{
            'X-CSRFToken' : '{{csrf_token}}'
            },
            data: JSON.stringify({'usertype': '2' }),
            dataType: "text",
            success: function (data) {
                console.log('성공');
            },
            error: function (data) {
            console.log('실패');
            console.log(error);
            }
        });
    });

    $("#3").click(function(){
        $.ajax({
            type: 'POST',
            url: "/account/usertype",
            headers:{
            'X-CSRFToken' : '{{csrf_token}}'
            },
            data: JSON.stringify({'usertype': '3' }),
            dataType: "text",
            success: function (data) {
                console.log('성공');
            },
            error: function (data) {
            console.log('실패');
            console.log(error);
            }
        });
    });

    $("#4").click(function(){
        $.ajax({
            type: 'POST',
            url: "/account/usertype",
            headers:{
            'X-CSRFToken' : '{{csrf_token}}'
            },
            data: JSON.stringify({'usertype': '4' }),
            dataType: "text",
            success: function (data) {
                console.log('성공');
            },
            error: function (data) {
            console.log('실패');
            console.log(error);
            }
        });
    });

  }



  // var user = document.getElementsByClassName("sortable");
  // var prioritys =[
  //     {% for statistic in mine %}{
  //       id: "{{statistic.user}}",
  //       daily_time: "{{statistic.daily}}",
  //     },   
  //     {% endfor %}
  // ];

  // <li class="ui-state-default">
  //   <span class="ui-icon ui-icon-arrowthick-2-n-s"></span>Item 1
  // </li>