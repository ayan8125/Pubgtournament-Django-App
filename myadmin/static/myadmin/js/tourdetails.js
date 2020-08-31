function makeCheck(box,buttonid){
    let icon = box.getElementsByTagName('i')
    let button = document.getElementById('winner'+buttonid)
    let check = icon[0]
    if(check.classList.contains('fas')){
        icon[0].setAttribute('class','')
        button.style.visibility = "hidden"
    }
    else{
        icon[0].setAttribute('class','fas fa-check')
        button.style.visibility = "visible"
    }
    
}

function makewinner(regid,tourid){
    let hero = document.getElementById('wrapper')
    let loaders = document.getElementById('loaders')
    let messages = document.getElementById('messages')
    let actualmessage = document.getElementById('actualmessage')
    loaders.style.display = 'block'
    hero.style.opacity = '0.9'
    hero.style.filter = 'blur(6px)'  
    console.log(regid, tourid)
    const formdata = new FormData()
    formdata.append('regid', regid)
    formdata.append('tourid', tourid)
    formdata.append('csrfmiddlewaretoken', document.getElementsByName('csrfmiddlewaretoken')[0].value)
    var xhr = new XMLHttpRequest();

    // Open the connection.
    xhr.open('POST', '/myadmin/tournaments/makewinner/', true);


    // Set up a handler for when the task for the request is complete.
    xhr.onload = function () {
        loaders.style.display = 'none'
        hero.style.opacity = '1'
        hero.style.filter = 'blur(0px)'
    if (xhr.status === 200) {
        
        loaders.style.display = 'none'
        hero.style.opacity = '1'
        hero.style.filter = 'blur(0px)' 
        messages.style.width = "25rem";
        messages.style.visibility = "visible";
        messages.style.backgroundColor = "forestgreen";
        actualmessage.innerHTML = "Winner was Aloted, Successfully!";

    } else {
        loaders.style.display = 'none'
        hero.style.opacity = '1'
        hero.style.filter = 'blur(0px)'
        messages.style.width = "25rem";
        messages.style.visibility = "visible";
        messages.style.backgroundColor = "firebrick";
        actualmessage.innerHTML = "Sorry , an unexpected error has been occured , try uploading image again!";
    }
    };

    // Send the Data.
    xhr.send(formdata);
}