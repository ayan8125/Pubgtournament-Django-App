var dlist = document.getElementById("dlist");
var dowmarrow = document.getElementById('dowmarrow')
var redem = document.getElementById('redem')
var alernote = document.getElementById('alernote')

// dowmarrow.addEventListener('click', function (e) {
//     if(dlist.classList.contains('showbanks')){
//         var x = window.matchMedia('max-width:375px')
      
//         dlist.classList.remove('showbanks');
//     }
//     else{
//         dlist.classList.add('showbanks')
//     }
// })
function assigninput(li){
    console.log(li)
}


redem.addEventListener('click', function(e){
    e.preventDefault();
    let hero = document.getElementById('maincontent')
    let loaders = document.getElementById('loaders')
    loaders.style.display = 'block'
    hero.style.opacity = '0.9'
    hero.style.filter = 'blur(6px)'


    holdername = document.getElementById('holdername').value
    accountno = document.getElementById('accountno').value
    ifscode = document.getElementById('ifscode').value


    if(holdername != '' && accountno != '' && ifscode != '' ){
    $.ajax({
            type:'POST',
            url:'/posttoredemmoney/',
            dataType: 'json',
            data:{
         
                holdername: holdername,
                accoutno:accountno,
                ifscode:ifscode,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success:function(data){
                loaders.style.display = 'none'
                hero.style.opacity = '1'
                hero.style.filter = 'blur(0px)'
                if(data.valid){
                    location.href = '/'
                }
                if(data.servererror){
                    location.href = '/'
                }
                if(data.errormessage){
                    alernote.style.color = "crimson";
                    alernote.style.fontSize = "1.2rem";
                    alernote.innerHTML = data.errormessage
                }
       
   
        
            }
    });
}

})