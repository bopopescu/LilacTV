var Body = {
  // target: var document.querySelector('body');
  setColor:function (color){
    // document.querySelector('body').style.color = color;
    $('body').css('color', color);
  },
  setBackground:function (color){
    // document.querySelector('body').style.backgroundColor = color;
    $('body').css('backgroundColor', color);
  }
};

var Links = {
  setColor:function (color){
    // var alist = document.querySelectorAll('a');
    // for (var i = 0 ; i < alist.length ; i++){
    //   alist[i].style.color = color;
    // }
    $('a').css('color',color);
  }
};

function NightDayHandler(self){
  if(self.value === 'night'){
    Body.setBackground('black');
    Body.setColor('white');
    Links.setColor('red');
    self.value = 'day';

  } else{
    Body.setBackground('white');
    Body.setColor('black');
    Links.setColor('blue');
    self.value = 'night';
  }
}
