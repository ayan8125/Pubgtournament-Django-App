let smsbutton = document.getElementById('smsbutton')
let emailbutton = document.getElementById('emailbutton')


function sendsms(tourid) {
    let hero = document.getElementById('wrapper')
    let loaders = document.getElementById('loaders')
    loaders.style.display = 'block'
    hero.style.opacity = '0.9'
    hero.style.filter = 'blur(6px)'   
    $.ajax({
        type: 'POST',
        url: '/myadmin/admin/sendcredentails/',
        dataType: 'json',
        data: {
            tourid: tourid,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(data) {
            loaders.style.display = 'none'
            hero.style.opacity = '1'
            hero.style.filter = 'blur(0px)' 
            console.log(data)
            if(data.smssend){
                let messages = document.getElementById('messages')
                let actualmessage = document.getElementById('actualmessage')
            
                messages.style.width = "25rem";
                messages.style.visibility = "visible";
                messages.style.backgroundColor = "forestgreen";
                actualmessage.innerHTML = "Rooms Credentials has been send to the users, Successfully!";
            }
           
        }
        

    })
}


function sendemail(tourid) {
    let hero = document.getElementById('wrapper')
    let loaders = document.getElementById('loaders')
    loaders.style.display = 'block'
    hero.style.opacity = '0.9'
    hero.style.filter = 'blur(6px)'  

    $.ajax({
        type: 'POST',
        url: '/myadmin/admin/sendcredentailsemail/',
        dataType: 'json',
        data: {
            tourid: tourid,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(data) {
            loaders.style.display = 'none'
            hero.style.opacity = '1'
            hero.style.filter = 'blur(0px)' 
            if(data.emailssend){
                let messages = document.getElementById('messages')
                let actualmessage = document.getElementById('actualmessage')
            
                messages.style.width = "25rem";
                messages.style.visibility = "visible";
                messages.style.backgroundColor = "forestgreen";
                actualmessage.innerHTML = "Rooms Credentials has been send to the users, Successfully!";
            }
            
        }
        

    })
}


function canceltour(tourid) {
    let hero = document.getElementById('wrapper')
    let loaders = document.getElementById('loaders')
    loaders.style.display = 'block'
    hero.style.opacity = '0.9'
    hero.style.filter = 'blur(6px)' 

    $.ajax({
        type: 'POST',
        url: '/myadmin/admin/canceltour/',
        dataType: 'json',
        data: {
            tourid: tourid,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(data) {
            loaders.style.display = 'none'
            hero.style.opacity = '1'
            hero.style.filter = 'blur(0px)' 
            if(data.canceltour){
                let messages = document.getElementById('messages')
                let actualmessage = document.getElementById('actualmessage')
            
                messages.style.width = "25rem";
                messages.style.visibility = "visible";
                messages.style.backgroundColor = "forestgreen";
                actualmessage.innerHTML = "Rooms Credentials has been send to the users, Successfully!";
            }
        }
        

    })
}



function starttour(tourid) {
    let hero = document.getElementById('wrapper')
    let loaders = document.getElementById('loaders')
    loaders.style.display = 'block'
    hero.style.opacity = '0.9'
    hero.style.filter = 'blur(6px)' 

    $.ajax({
        type: 'POST',
        url: '/myadmin/admin/starttour/',
        dataType: 'json',
        data: {
            tourid: tourid,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(data) {
            loaders.style.display = 'none'
            hero.style.opacity = '1'
            hero.style.filter = 'blur(0px)' 
            if(data.canceltour){
                let messages = document.getElementById('messages')
                let actualmessage = document.getElementById('actualmessage')
            
                messages.style.width = "25rem";
                messages.style.visibility = "visible";
                messages.style.backgroundColor = "forestgreen";
                actualmessage.innerHTML = "Rooms Credentials has been send to the users, Successfully!";
            }
        }
        

    })
}



function completetour(tourid) {
    let hero = document.getElementById('wrapper')
    let loaders = document.getElementById('loaders')
    loaders.style.display = 'block'
    hero.style.opacity = '0.9'
    hero.style.filter = 'blur(6px)' 

    $.ajax({
        type: 'POST',
        url: '/myadmin/admin/completetour/',
        dataType: 'json',
        data: {
            tourid: tourid,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(data) {
            loaders.style.display = 'none'
            hero.style.opacity = '1'
            hero.style.filter = 'blur(0px)' 
            if(data.canceltour){
                let messages = document.getElementById('messages')
                let actualmessage = document.getElementById('actualmessage')
            
                messages.style.width = "25rem";
                messages.style.visibility = "visible";
                messages.style.backgroundColor = "forestgreen";
                actualmessage.innerHTML = "Rooms Credentials has been send to the users, Successfully!";
            }
        }
        

    })
}
