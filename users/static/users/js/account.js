let state = false;
let  nextform = document.getElementById('sigin');
let editnamebutton = document.getElementById('editnamebutton')
let closenameform  = document.getElementById('closenameform')
let userimage = document.getElementById('userimage')
let camerafield = document.getElementById('camerafield')
let myimage = document.getElementById('myimage')

var leftarrow = document.getElementById('closebtns')
var sidenavs = document.getElementById('sidenavs')
var hamburger = document.getElementById('hamburger')
var hamburgerbody = document.getElementById('hamburgerbody')


hamburger.addEventListener('click', function(e){
    sidenavs.classList.add('showsidenav')
    hamburgerbody.style.display = 'none'
})


leftarrow.addEventListener('click', function(e){
    sidenavs.classList.remove('showsidenav')
    hamburgerbody.style.display = 'block'
})



camerafield.addEventListener('click',function(e){
    userimage.click();
})

userimage.addEventListener('change', function(e){
    let hero = document.getElementById('userdetails')
    let loaders = document.getElementById('loaders')
    loaders.style.display = 'block'
    hero.style.opacity = '0.9'
    hero.style.filter = 'blur(6px)'        
    let file = this.files[0]
    
    var allowedTypes = ['image/jpeg', 'image/png', 'image/jpg'];
    var fileType = file.type;
    console.log(fileType)
    if(!allowedTypes.includes(fileType)){
        //document.getElementById('uploadStatus').innerHTML = 'Please select a valid file (JPEG/JPG/PNG).';
        console.log('invalid file')
        $("#userimage").val('');
        loaders.style.display = 'none'
        hero.style.opacity = '1'
        hero.style.filter = 'blur(0px)' 
        let messages = document.getElementById('messages')
        let actualmessage = document.getElementById('actualmessage')
        
        messages.style.width = "25rem";
        messages.style.visibility = "visible";
        messages.style.backgroundColor = "firebrick";
        actualmessage.innerHTML = "Invalid image Format, please choose image with valid format like png, jpg.., etc";
        return false;
    }
    else{
        if(file){
                let messages = document.getElementById('messages')
                let actualmessage = document.getElementById('actualmessage')
          
                const formData = new FormData();
                formData.append('myfile', file, file.name);
                formData.append('csrfmiddlewaretoken',$('input[name=csrfmiddlewaretoken]').val() )
                var xhr = new XMLHttpRequest();

                // Open the connection.
                xhr.open('POST', '/user/setprofileimage/', true);


                // Set up a handler for when the task for the request is complete.
                xhr.onload = function () {
                    loaders.style.display = 'none'
                    hero.style.opacity = '1'
                    hero.style.filter = 'blur(0px)'
                if (xhr.status === 200) {
                    messages.style.width = "25rem";
                    messages.style.visibility = "visible";
                    messages.style.backgroundColor = "forestgreen";
                    actualmessage.innerHTML = "Your Profile image has been Updated Successfully!";

                    const reader = new FileReader();
                    console.log(file, this)
                    reader.addEventListener("load",function(e){
                        myimage.setAttribute('src', this.result)
                    })
                    reader.readAsDataURL(file)

                } else {
                    messages.style.width = "25rem";
                    messages.style.visibility = "visible";
                    messages.style.backgroundColor = "firebrick";
                    actualmessage.innerHTML = "Sorry , an unexpected error has been occured , try uploading image again!";
                }
                };

                // Send the Data.
                xhr.send(formData);
        }
        else{
            console.log('file is not selected')
        }
    }
    // console.log(file)
   
})

editnamebutton.addEventListener('click',function(e){
    let maincontent = document.getElementById('maincontent')
    maincontent.style.opacity = "0.5"
    maincontent.style.filter = "blur(5px)"
    let form = document.getElementById('nameform')
    form.style.width = "309px";
    form.style.visibility = 'visible';
})

closenameform.addEventListener('click',function(e){
    let maincontent = document.getElementById('maincontent')
    maincontent.style.opacity = "1"
    maincontent.style.filter = "blur(0)"
    let form = document.getElementById('nameform')
    form.style.width = "0";
    form.style.visibility = 'hidden'; 
})








$(document).on('click','#submitname',function(e){
    e.preventDefault();
    let hero = document.getElementById('nameform')
    let loaders = document.getElementById('loaders')
    loaders.style.display = 'block'
    hero.style.opacity = '0.9'
    hero.style.filter = 'blur(6px)'
    fullname = document.getElementById('fullname').value
    let passwords = document.getElementById('fullnameinvalid')
    passwords.style.display = 'none';
    if(fullname != ''){
    $.ajax({
            type:'POST',
            url:'/user/editname/',
            dataType: 'json',
            data:{
            fullname:fullname,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success:function(data){
                loaders.style.display = 'none'
                hero.style.opacity = '1'
                hero.style.filter = 'blur(0px)'
                if(data.valid){
                    location.reload()
                }
            if (data.notvalid){
          let feedback = document.getElementById('fullnameinvalid')
          feedback.style.display = 'block';
          feedback.innerHTML = 'Invalid Name!'


            
    }
   
        
            }
    });
}
});



let editmailbutton = document.getElementById('editmailbutton')
let closeemailform = document.getElementById('closeemailform')

editmailbutton.addEventListener('click',function(e){
    let maincontent = document.getElementById('maincontent')
    maincontent.style.opacity = "0.5"
    maincontent.style.filter = "blur(5px)"
    let form = document.getElementById('emailform')
    form.style.width = "309px";
    form.style.visibility = 'visible';
})

closeemailform.addEventListener('click',function(e){
    let maincontent = document.getElementById('maincontent')
    maincontent.style.opacity = "1"
    maincontent.style.filter = "blur(0)"
    let form = document.getElementById('emailform')
    form.style.width = "0";
    form.style.visibility = 'hidden'; 
})




$(document).on('click','#submitemail',function(e){
    e.preventDefault();
    let hero = document.getElementById('emailform')
    let loaders = document.getElementById('loaders')
    loaders.style.display = 'block'
    hero.style.opacity = '0.9'
    hero.style.filter = 'blur(6px)'
    email = document.getElementById('email').value
    let emailinvalid = document.getElementById('emailinvalid')
    emailinvalid.style.display = 'none';
    if(email != ''){
    $.ajax({
            type:'POST',
            url:'/user/editmail/',
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
                    let nmailsend = document.getElementById('nmailsend')
                    nmailsend.style.display = 'block';
                    let submitemail = document.getElementById('submitemail')
                    submitemail.style.display = 'none';
                    // location.reload()
                }
                if(data.userexits){
                    let feedback = document.getElementById('emailinvalid')
                    feedback.style.display = 'block';
                    feedback.innerHTML = 'User with this email, already exists!' 
                }
            if (data.notvalid){
          let feedback = document.getElementById('emailinvalid')
          feedback.style.display = 'block';
          feedback.innerHTML = 'Invalid Email!'


            
    }
   
        
            }
    });
}
});






let editpasswordbutton = document.getElementById('editpasswordbutton')
let closepasswordform = document.getElementById('closepasswordform')

editpasswordbutton.addEventListener('click',function(e){
    let maincontent = document.getElementById('maincontent')
    maincontent.style.opacity = "0.5"
    maincontent.style.filter = "blur(5px)"
    let form = document.getElementById('passwordform')
    form.style.width = "309px";
    form.style.visibility = 'visible';
})

closepasswordform.addEventListener('click',function(e){
    let maincontent = document.getElementById('maincontent')
    maincontent.style.opacity = "1"
    maincontent.style.filter = "blur(0)"
    let form = document.getElementById('passwordform')
    form.style.width = "0";
    form.style.visibility = 'hidden'; 
})




$(document).on('click','#submitpassword',function(e){
    e.preventDefault();
    let hero = document.getElementById('passwordform')
    let loaders = document.getElementById('loaders')
    loaders.style.display = 'block'
    hero.style.opacity = '0.9'
    hero.style.filter = 'blur(6px)'

    currentpassword = document.getElementById('currentpassword').value
    newpassword = document.getElementById('newpassword').value
    confirmnewpassword = document.getElementById('confirmnewpassword').value

    let newpasswordvalid = document.getElementById('newpassinvalid')
    newpasswordvalid.style.display = 'none';
    let currenpassinvalid = document.getElementById('currenpassinvalid')
    currenpassinvalid.style.display = 'none';
    if(currentpassword != '' && newpassword != '' && confirmnewpassword != ''){
    $.ajax({
            type:'POST',
            url:'/user/editpassword/',
            dataType: 'json',
            data:{
            currentpassword:currentpassword,
            newpassword:newpassword,
            confirmnewpassword:confirmnewpassword,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success:function(data){
                loaders.style.display = 'none'
                hero.style.opacity = '1'
                hero.style.filter = 'blur(0px)'
                if(data.valid){
                    location.reload()
                }
                if(data.nomatch){
                    let feedback = document.getElementById('newpassinvalid')
                    feedback.style.display = 'block';
                    feedback.innerHTML = 'New Password are not matching' 
                }
            if (data.notvalid){
          let feedback = document.getElementById('currenpassinvalid')
          feedback.style.display = 'block';
          feedback.innerHTML = 'Incorrect, Current Password!'


            
    }
   
        
            }
    });
}
});





let editnumberdbutton = document.getElementById('editnumberdbutton')
let closenumberform = document.getElementById('closenumberform')

editnumberdbutton.addEventListener('click',function(e){
    let maincontent = document.getElementById('maincontent')
    maincontent.style.opacity = "0.5"
    maincontent.style.filter = "blur(5px)"
    let form = document.getElementById('numberform')
    form.style.width = "309px";
    form.style.visibility = 'visible';
})

closenumberform.addEventListener('click',function(e){
    let maincontent = document.getElementById('maincontent')
    maincontent.style.opacity = "1"
    maincontent.style.filter = "blur(0)"
    let form = document.getElementById('numberform')
    form.style.width = "0";
    form.style.visibility = 'hidden'; 
})




$(document).on('click','#submitnumber',function(e){
    e.preventDefault();
    let hero = document.getElementById('numberform')
    let loaders = document.getElementById('loaders')
    loaders.style.display = 'block'
    hero.style.opacity = '0.9'
    hero.style.filter = 'blur(6px)'

    number = document.getElementById('number').value
    

    let newpasswordvalid = document.getElementById('numberinvalid')
    newpasswordvalid.style.display = 'none';
    if(number != '' ){
    $.ajax({
            type:'POST',
            url:'/user/editnumber/',
            dataType: 'json',
            data:{
                number:number,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success:function(data){
                loaders.style.display = 'none'
                hero.style.opacity = '1'
                hero.style.filter = 'blur(0px)'
                if(data.nochange){
                    location.reload()
                }
                if(data.changesuccess){
                    location.reload()
                }
                if(data.otpsend){
                    let numbersform = document.getElementById('numbersform')
                    numbersform.style.display = 'none'
                    let otpforms = document.getElementById('otpforms')
                    otpforms.style.display="block"
                }
                if(data.userexists){
                    let feedback = document.getElementById('numberinvalid')
                    feedback.style.display = 'block';
                    feedback.innerHTML = 'User with this number, already exists' 
                }
            if (data.notvalid){
          let feedback = document.getElementById('numberinvalid')
          feedback.style.display = 'block';
          feedback.innerHTML = 'Invalid, number!'


            
    }
   
        
            }
    });
}
});





$(document).on('click','#submitotp',function(e){
    e.preventDefault();
    let hero = document.getElementById('otpforms')
    let loaders = document.getElementById('loaders')
    loaders.style.display = 'block'
    hero.style.opacity = '0.9'
    hero.style.filter = 'blur(6px)'

    otp = document.getElementById('otp').value
    number = document.getElementById('number').value

    let otpinvalid = document.getElementById('otpinvalid')
    otpinvalid.style.display = 'none';
    if(otp != '' ){
    $.ajax({
            type:'POST',
            url:'/user/checkotp/',
            dataType: 'json',
            data:{
                otp:otp,
                number:number,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success:function(data){
                loaders.style.display = 'none'
                hero.style.opacity = '1'
                hero.style.filter = 'blur(0px)'
                if(data.valid){
                 location.reload()
                }
             
            if (data.notvalid){
          let feedback = document.getElementById('otpinvalid')
          feedback.style.display = 'block';
          feedback.innerHTML = 'Incorrect, Otp!'


            
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









       

        
        
























