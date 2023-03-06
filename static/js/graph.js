const ctx = document.getElementById('myChart');

data = {
    labels: ['Number of Users'],
    datasets: [{
      data: [nbUsers],
      borderWidth: 1,
      backgroundColor: [
        'rgb(255, 99, 132)'
      ]
    }]
  }

new Chart(ctx, {
  type: 'pie',
  data: data,
  options: {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Pie Chart of Users'
      }
    }
  },
});
