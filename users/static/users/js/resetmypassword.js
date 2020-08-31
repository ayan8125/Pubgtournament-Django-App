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
let resetbutton = document.getElementById("resetbutton")
let setpasswordform = document.getElementById("setpasswordform")
let strength = 0; 
let hero = document.getElementById("hero")
let loaders = document.getElementById("loaders")

resetbutton.addEventListener('click', function(e) {
    if(strength==5){
        setpasswordform.submit()
        hero.style.filter = "blur(5px)"
        loaders.style.display = "block"
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
                if(strength==4){
                    resetbutton.style.opacity = 1
                    strength += 1
                }
                else{
                    resetbutton.style.opacity = 0.2
                    strength -= 1
                }
            } else {
                passwordmatch.classList.add('fa-circle');
                passwordmatch.classList.remove('fa-check');  
                resetbutton.style.opacity = 0.2
          
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
    strength = 0;
    resetbutton.style.opacity = 0.2
    //If password contains both lower and uppercase characters
    if (password.match(/([a-z].*[A-Z])|([A-Z].*[a-z])/)) {
        strength += 1;
        lowUpperCase.classList.remove('fa-circle');
        lowUpperCase.classList.add('fa-check');
    } else {
        strength -= 1;
        lowUpperCase.classList.add('fa-circle');
        lowUpperCase.classList.remove('fa-check');
    }
    //If it has numbers and characters
    if (password.match(/([0-9])/)) {
        strength += 1;
        number.classList.remove('fa-circle');
        number.classList.add('fa-check');
    } else {
        strength -= 1;
        number.classList.add('fa-circle');
        number.classList.remove('fa-check');
    }
    //If it has one special character
    if (password.match(/([!,%,&,@,#,$,^,*,?,_,~])/)) {
        strength += 1;
        specialChar.classList.remove('fa-circle');
        specialChar.classList.add('fa-check');
    } else {
        strength -= 1;
        specialChar.classList.add('fa-circle');
        specialChar.classList.remove('fa-check');
    }
    //If password is greater than 7
    if (password.length > 7) {
        strength += 1;
        eightChar.classList.remove('fa-circle');
        eightChar.classList.add('fa-check');
    } else {
        strength -= 1;
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
        passwordStrength.style = 'width: 80%';

    }
    if(strength==4 && password.value == confirmpassword.value){
        resetbutton.style.opacity = 1
        strength += 1
    }
    
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























