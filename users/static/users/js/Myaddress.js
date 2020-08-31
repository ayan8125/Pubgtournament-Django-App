var submitaddress = document.getElementById('submitaddress')
var error = document.getElementById('error')



$(document).on('click','#submitaddress',function(e){
    e.preventDefault();
    let hero = document.getElementById('hero')
    let loaders = document.getElementById('loaders')


    counrty = document.getElementById('country').value
    state = document.getElementById('state').value
    addres = document.getElementById('addres').value
    city = document.getElementById('city').value
    picode = document.getElementById('pincode').value

    error.innerHTML = ''
    if(counrty != '' && state != '' && addres != '' && city != '' && picode != ''){
        country = document.getElementById('country').value
        state = document.getElementById('state').value
        addres = document.getElementById('addres').value
        city = document.getElementById('city').value
        pincode = document.getElementById('pincode').value
        loaders.style.display = 'block'
        hero.style.opacity = '0.9'
        hero.style.filter = 'blur(6px)'
        $.ajax({
            type:'POST',
            url:'/user/editaddress/',
            dataType: 'json',
            data:{
                country:country,
                state:state,
                address:addres,
                city:city,
                pincode:pincode,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success:function(data){
                if(data.valid){
                    location.href = '/'
                   }
                loaders.style.display = 'none'
                hero.style.opacity = '1'
                hero.style.filter = 'blur(0px)'

             
            if (data.staterror){
                error.innerHTML = 'Incorrect State!'
            }
            if(data.pincode){
                error.innerHTML = 'Incorrect Pincode!'
            }
            if(data.cityerror){
                error.innerHTML = 'Incorrect City Name!'
            }
        
            }
    });
}
});


function showcountries(){
    var countries = document.getElementById('counrtylists')
    if(countries.classList.contains('showcounrties')){
        countries.classList.remove('showcounrties')
    }
    else{
        countries.classList.add('showcounrties')
    }
}



function selectthis(name){
   var country = document.getElementById('country')
   var counrtylists = document.getElementById('counrtylists')
   counrtylists.classList.remove('showcounrties')
   country.value = name
}



