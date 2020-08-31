
var mainnav = document.getElementById('mainnav');
var hero = document.getElementById('hero')
var navlink = mainnav.getElementsByClassName('navlink')

var logoutmodal = document.getElementById('logoutmodal') 
var closemodals = document.getElementById('closemodals')
var closemodal = document.getElementById('closemodal')
var logoutag = document.getElementById('logoutag')
var listsofbook1 = document.getElementById('listsofbook1')
var mainnotibody1 = document.getElementById('mainnotibody1')
var backarrow =  document.getElementById('backarrow')
var leftarrow = document.getElementById('closebtns')
var sidenavs = document.getElementById('sidenavs')
var hamburger = document.getElementById('hamburger')
var usernotification = document.getElementById('usernotification')


hamburger.addEventListener('click', function(e){
    sidenavs.classList.add('showsidenav')
   
})


leftarrow.addEventListener('click', function(e){
    sidenavs.classList.remove('showsidenav')
   
})


listsofbook1.addEventListener('click', function(e){
   
    var x = window.matchMedia("(max-width: 340px)")
    if(x.matches){
        mainnotibody1.style.width = '18rem';
    }
    else{
        mainnotibody1.style.width = '20rem';
    }
    listsofbook1.style.display = 'none';
    mainnotibody1.style.height = '30rem';
    mainnotibody1.style.display = 'block';
})

backarrow.addEventListener('click', function(e){
    listsofbook1.style.display = 'block';
    mainnotibody1.style.width = '0';
    mainnotibody1.style.height = '0';
    mainnotibody1.style.display = 'none'; 
    hamburgerbody.style.display = 'block'
})
// window.onscroll = function (e) {
//   var scrollfromtop = window.scrollY; // Value of scroll Y in px
//   if(scrollfromtop > 20){
//     mainnav.classList.add('fix-search')
//     hero.style.marginTop="7rem"
//     for(var i=0; i<navlink.length; i++){

//       navlink[i].style.color ="orange"
//     }
//   }
//   else{
//     mainnav.classList.remove('fix-search')
//     hero.style.marginTop="0rem"
//     for(var i=0; i<navlink.length; i++){

//       navlink[i].style.color ="white"
//     }
//   }
// };

logoutag.addEventListener('click', function(e){
    let hero = document.getElementById('hero')
    hero.style.filter = 'blur(5px)'
    logoutmodal.style.visibility = "visible";
    logoutmodal.style.width = "15rem";
    
})


closemodal.addEventListener('click', function(e){
    
    let hero = document.getElementById('hero')
    hero.style.filter = 'blur(0px)'
    logoutmodal.style.width = "0rem";
 
    logoutmodal.style.visibility = "hidden";
    
})

closemodals.addEventListener('click', function(e){
    let hero = document.getElementById('hero')
    hero.style.filter = 'blur(0px)'
    logoutmodal.style.width = "0rem";
  
    logoutmodal.style.visibility = "hidden";
    
})


function countdown(day,thour,tmin,tsec,evetyear,eventmonth,evendate,hour,minute,second,milliseconds){
    var now = new Date();
    var eventdate = new Date(evetyear,eventmonth,evendate,hour,minute,second);

    var current = now.getTime();
    var eventtime = eventdate.getTime();

    var remtime = eventtime - current;


    var s = Math.floor(remtime/1000);
    var m = Math.floor(s/60);
    var h= Math.floor(m/60);
    var d = Math.floor(h/24);

    h %= 24
    m %= 60
    s %= 60

    console.log(d,h,m,s)

    h = (h < 10 && h >= 0) ? "0"+h: h;
    m = (m < 10 && m >= 0) ? "0"+m: m;
    s = (s < 10 && s >= 0) ? "0"+s: s;
    d = (d < 10 && d >= 0)? "0"+d:d;

    h = (h < 0 ) ? "00":h;
    m = (m < 0) ? "00":m;
    s = (s < 0) ?"00":s;
    d = (d < 0) ? "00":d;

    document.getElementById(day).innerHTML = d;
    document.getElementById(thour).innerHTML = h;
    document.getElementById(tmin).innerHTML = m;
    document.getElementById(tsec).innerHTML = s;
    
}

getusernotification()

function getusernotification(){
    let xhr = new XMLHttpRequest();

    xhr.open('GET', '/usernotification/');
    xhr.send();

    xhr.onload = function() {
        if (xhr.status != 200) { // analyze HTTP status of the response
          alert(`Error ${xhr.status}: ${xhr.statusText}`); // e.g. 404: Not Found
        } else { // show the result
            usernotification.innerHTML = xhr.responseText
          console.log(xhr.responseText)
        }
      };
}