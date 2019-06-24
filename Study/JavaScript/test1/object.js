window.onload = function(){
    var pattern = /(\w+)\s(\w+)/;
    var str = "Badjin Javascript";
    var urlPattern = /(\b(?:https?):\/\/[a-z0-9-+&@#\/%?=~_|!:,.;]*)/gim;
    var content = '생활코딩 : http://opentutorials.org/course/1 입니다. 네이버 : http://naver.com 입니다. ';

    var hw1 = document.getElementById('hw1');
    var hw2 = document.getElementById('hw2');

    hw1.addEventListener('click', function(){
      var result = content.replace(urlPattern, function(url){
        return '<a href="'+url+'">'+url+'</a>';
      });
      alert(result);
    });

    hw2.addEventListener('click', function(){
      if (urlPattern.test(content)){
        //document.write(RegExp.$1+"<br />");
        alert(content.match(urlPattern)[1]+"<br />");
      }
    });

};
