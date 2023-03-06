const ctx = document.getElementById('myChart');

data = {
    labels: ['Number of Users', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
    datasets: [{
      data: [nbUsers, 19, 3, 5, 2, 3],
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
