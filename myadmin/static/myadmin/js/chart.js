var ctx = document.getElementById('myPieChart');
var myPieChart = new Chart(ctx, {
    type: 'pie',
    data : {
        datasets: [{
            data: [60, 40],
            backgroundColor:['crimson', 'gray']
        }],
        
    
        // These labels appear in the legend and in the tooltips when hovering different arcs
        labels: [
            'Occupied Places',
            'Availabel Places',
           
        ]
    },

});