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
