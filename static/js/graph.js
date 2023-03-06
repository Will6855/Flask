const ctx = document.getElementById('myChart');

data = {
    labels: ['Number of Users'],
    datasets: [{
      data: [nbUsers],
      borderWidth: 1
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
        text: 'Chart.js Pie Chart'
      }
    }
  },
});
