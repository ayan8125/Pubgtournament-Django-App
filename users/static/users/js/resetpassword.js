



var leftarrow = document.getElementById('closebtns')
var sidenavs = document.getElementById('sidenavs')
var hamburger = document.getElementById('hamburger')
var hamburgerbody = document.getElementById('hamburgerbody')
var reset = document.getElementById('reset')




hamburger.addEventListener('click', function(e){
    sidenavs.classList.add('showsidenav')
    hamburgerbody.style.display = 'none'
})


leftarrow.addEventListener('click', function(e){
    sidenavs.classList.remove('showsidenav')
    hamburgerbody.style.display = 'block'
})

reset.addEventListener('click', function(e){
    e.preventDefault();
    let hero = document.getElementById('maincontent')
    let loaders = document.getElementById('loaders')
    loaders.style.display = 'block'
    hero.style.opacity = '0.9'
    hero.style.filter = 'blur(6px)'

    email = document.getElementById('email').value
    var errormessage = document.getElementById('errormessage')
    errormessage.style.display = 'none';
    if(email != ''){
    $.ajax({
            type:'POST',
            url:'/postoresetpassword/',
            dataType: 'json',
            data:{
            email:email,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success:function(data){
                loaders.style.display = 'none'
                hero.style.opacity = '1'
                hero.style.filter = 'blur(0px)'
                if(data.valid){
                    location.href = '/'
                }
            if (data.nouser){
                console.log('came')
                var errormessage = document.getElementById('errormessage')
                errormessage.style.display = 'block';
            errormessage.innerHTML = 'Sorry, No user with this email!'
      
            }
            

  
            }
    });
}

})


















