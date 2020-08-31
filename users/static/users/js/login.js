let state = false;
let  nextform = document.getElementById('sigin');



$(document).on('click','#signin',function(e){
    e.preventDefault();
    let hero = document.getElementById('hero')
    let loaders = document.getElementById('loaders')
    loaders.style.display = 'block'
    hero.style.opacity = '0.9'
    hero.style.filter = 'blur(6px)'
    password = document.getElementById('password').value
    email = document.getElementById('email').value
    if(document.getElementById('email').classList.contains('is-invalid')){
        document.getElementById('email').classList.remove('is-invalid')
    }
    let passwords = document.getElementById('invalidid')
    passwords.style.display = 'none';
    if(email != '' && password != ''){
    $.ajax({
            type:'POST',
            url:'/login/',
            dataType: 'json',
            data:{
            password:password,
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
          let email = document.getElementById('email')
          let feedback = document.getElementById('emailinvalid')
          feedback.innerHTML = 'Sorry, No user with this email!'
          email.classList.add('is-invalid')

            
    }
    if (data.wrongpassword){
        document.getElementById('password').value = ''
        document.getElementById('email').value = ''
        let password = document.getElementById('invalidid')
        password.style.display = 'block';
    }
        
            }
    });
}
});









function toggle(){
    if(state){
        document.getElementById("password").setAttribute("type","password");
        state = false;
    }else{
        document.getElementById("password").setAttribute("type","text")
        state = true;
    }
}

function myFunction(show){
    show.classList.toggle("fa-eye-slash");
}









       

        
        
























