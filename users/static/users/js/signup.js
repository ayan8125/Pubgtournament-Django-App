let state = false;
let state2 = false;
let password = document.getElementById("password");
let confirmpassword = document.getElementById("confirmpassword");
let passwordStrength = document.getElementById("password-strength");
let lowUpperCase = document.querySelector(".low-upper-case i");
let number = document.querySelector(".one-number i");
let specialChar = document.querySelector(".one-special-char i");
let eightChar = document.querySelector(".eight-character i");
let passwordmatch = document.querySelector(".password-match i");
let  nextform = document.getElementById('nextform');
let  nextotpsubmit = document.getElementById('nextotpsubmit');
let  nextcreatesubmit = document.getElementById('nextcreatesubmit');



    
$(document).on('click','#nextform',function(e){
    e.preventDefault();
    name = document.getElementById('name').value
    email = document.getElementById('email').value
    pnumber = document.getElementById('number').value
    if(document.getElementById('name').classList.contains('is-invalid')){
        document.getElementById('name').classList.remove('is-invalid')
    }
    if(document.getElementById('email').classList.contains('is-invalid')){
        document.getElementById('email').classList.remove('is-invalid')
    }
    
    if(document.getElementById('number').classList.contains('is-invalid')){
        document.getElementById('number').classList.remove('is-invalid')
    }
    

    
    
    if(name != '' && email != '' && pnumber != ''){
        let hero = document.getElementById('hero')
        let loaders = document.getElementById('loaders')
        loaders.style.display = 'block'
        hero.style.opacity = '0.9'
        hero.style.filter = 'blur(6px)'
    $.ajax({
            type:'POST',
            url:'/signup/',
            dataType: 'json',
            data:{
            name:name,
            email : email,
            phnumber:pnumber,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success:function(data){
                loaders.style.display = 'none'
                hero.style.opacity = '1'
                hero.style.filter = 'blur(0px)'
                console.log(data);
            if (data.emailexists){
                let email = document.getElementById('email')
                let feedback = document.getElementById('emailinvalid')
                feedback.innerHTML = 'User with this  Email, already exists'
                email.classList.add('is-invalid')

    }
    if (data.numberexists){
        let pnumber = document.getElementById('number')
        let feedback = document.getElementById('numberinvalid')
        feedback.innerHTML = 'User with this  number, already exists'
        pnumber.classList.add('is-invalid')

}
if (data.notvalidemail){
    let email = document.getElementById('email')
    let feedback = document.getElementById('emailinvalid')
    feedback.innerHTML = 'Enter a valid Email '
    email.classList.add('is-invalid')

}
if (data.notnumber){
    let pnumber = document.getElementById('number')
    let feedback = document.getElementById('numberinvalid')
    feedback.innerHTML = 'Enter a valid Number'
    pnumber.classList.add('is-invalid')

}
    if (data.notvalidname){
        let name = document.getElementById('name')
        let feedback = document.getElementById('nameinvalid')
        feedback.innerHTML = 'Enter a valid Name'
        name.classList.add('is-invalid')
    }
    if (data.notvalidlastname){
        notlastname();
    }
    if(data.otpsend){
    let validateform1 = document.getElementById('validateForm1')
    let validateform2 = document.getElementById('validateForm2')
    validateform1.style.width = "0"
    
    validateform2.style.display = "block"
    validateform2.style.width = "324px"
    validateform1.style.display = "none"
    }
        
            }
    });
}
});
    
    



$(document).on('click','#nextotpsubmit',function(e){
    e.preventDefault();
    otp = document.getElementById('otp').value
    email = document.getElementById('email').value
    if(document.getElementById('otp').classList.contains('is-invalid')){
        document.getElementById('otp').classList.remove('is-invalid')
    }
    if(otp != ''){
        let hero = document.getElementById('hero')
        let loaders = document.getElementById('loaders')
        loaders.style.display = 'block'
        hero.style.opacity = '0.9'
        hero.style.filter = 'blur(6px)'
    $.ajax({
            type:'POST',
            url:'/otp/',
            dataType: 'json',
            data:{
            otp:otp,
            email:email,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success:function(data){
                loaders.style.display = 'none'
                hero.style.opacity = '1'
                hero.style.filter = 'blur(0px)'
                console.log(data);
            if (data.otpwrong){
          let otp = document.getElementById('otp')
          let feedback = document.getElementById('otpinvalid')
          feedback.innerHTML = 'Wrong OTP'
          otp.classList.add('is-invalid')

            
    }
    if (data.success){
    let validateform2 = document.getElementById('validateForm2')
    let validateform3 = document.getElementById('validateForm3')
    validateform2.style.width = "0"
    validateform2.style.display = "none"
    validateform3.style.display = "block"
    validateform3.style.width = "324px"
    }
        
            }
    });
}
});




$(document).on('click', '#nextcreatesubmit', function(e){

    e.preventDefault();
    email = document.getElementById('email').value
    pass = document.getElementById('password').value
    if(pass != ''){
        let hero = document.getElementById('hero')
        let loaders = document.getElementById('loaders')
        loaders.style.display = 'block'
        hero.style.opacity = '0.9'
        hero.style.filter = 'blur(6px)'
    $.ajax({
          type:'POST',
          url:'/setPassword/',
          dataType: 'json',
          data:{
            email:email,
            password : pass,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
          },
          success:function(data){
            loaders.style.display = 'none'
            hero.style.opacity = '1'
            hero.style.filter = 'blur(0px)'
              console.log(data);
            if (data.emailsend){
              location.reload()
            }
        
         
          }
    });
}


})




password.addEventListener("keyup", function(){
    let pass = document.getElementById("password").value;
    checkStrength(pass);
});

confirmpassword.addEventListener("keyup", function(){
        //If password is greater than 7
        if(confirmpassword.value != '') {
            if (password.value == confirmpassword.value) {
                passwordmatch.classList.remove('fa-circle');
                passwordmatch.classList.add('fa-check');
            } else {
                passwordmatch.classList.add('fa-circle');
                passwordmatch.classList.remove('fa-check');   
            }
        
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

function checkStrength(password) {
    let strength = 0;

    //If password contains both lower and uppercase characters
    if (password.match(/([a-z].*[A-Z])|([A-Z].*[a-z])/)) {
        strength += 1;
        lowUpperCase.classList.remove('fa-circle');
        lowUpperCase.classList.add('fa-check');
    } else {
        lowUpperCase.classList.add('fa-circle');
        lowUpperCase.classList.remove('fa-check');
    }
    //If it has numbers and characters
    if (password.match(/([0-9])/)) {
        strength += 1;
        number.classList.remove('fa-circle');
        number.classList.add('fa-check');
    } else {
        number.classList.add('fa-circle');
        number.classList.remove('fa-check');
    }
    //If it has one special character
    if (password.match(/([!,%,&,@,#,$,^,*,?,_,~])/)) {
        strength += 1;
        specialChar.classList.remove('fa-circle');
        specialChar.classList.add('fa-check');
    } else {
        specialChar.classList.add('fa-circle');
        specialChar.classList.remove('fa-check');
    }
    //If password is greater than 7
    if (password.length > 7) {
        strength += 1;
        eightChar.classList.remove('fa-circle');
        eightChar.classList.add('fa-check');
    } else {
        eightChar.classList.add('fa-circle');
        eightChar.classList.remove('fa-check');   
    }



    // If value is less than 2
    if (strength < 2) {
        passwordStrength.classList.remove('progress-bar-warning');
        passwordStrength.classList.remove('progress-bar-success');
        passwordStrength.classList.add('progress-bar-danger');
        passwordStrength.style = 'width: 10%';
    } else if (strength == 3) {
        passwordStrength.classList.remove('progress-bar-success');
        passwordStrength.classList.remove('progress-bar-danger');
        passwordStrength.classList.add('progress-bar-warning');
        passwordStrength.style = 'width: 60%';
    } else if (strength == 4) {
        passwordStrength.classList.remove('progress-bar-warning');
        passwordStrength.classList.remove('progress-bar-danger');
        passwordStrength.classList.add('progress-bar-success');
        passwordStrength.style = 'width: 100%';
    }
}












function submit_form(){
    console.log('Came here');
$(document).on('submit','#loginform',function(e){
   e.preventDefault();
   emails = document.getElementById('email').value
   pass = document.getElementById('password').value
   console.log(emails,pass)
   $.ajax({
         type:'POST',
         url:'{% url "login"  %}',
         dataType: 'json',
         data:{
           email:emails,
           password : pass,
           csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
         },
         success:function(data){
             console.log(data);
           if (data.nouser){
            document.getElementById('alerts').style.display = 'block';
            document.getElementById('note_pass1').innerHTML = 'No user with this Credentials'
           }
           if (data.wrongpassword){
              document.getElementById('alerts').style.display = 'block';
              document.getElementById('note_pass1').innerHTML = 'Incorrect Password'
           }
           if (data.valid){
            location.href='{% url "home" %}';
           }
        
         }
   });
});

}




       

        
        

function mytoggle(icon)
{   
    let confirmpassword = document.getElementById('confirmpassword')
    icon.classList.toggle('fa-eye-slash')
    if(confirmpassword.type == 'password'){
        confirmpassword.type = 'text'
    }
    if(state2){
        confirmpassword.setAttribute("type","password");
        state2 = false;
    }else{
        confirmpassword.setAttribute("type","text")
        state2 = true;
    }
    
}























