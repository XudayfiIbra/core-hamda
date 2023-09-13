console.log("helloooo halimaaaah ");

const dashboardslug = document.getElementById("dashboard-slug").textContent.trim();
const user = document.getElementById("user").textContent.trim();
const submitBtn = document.getElementById("submit-btn");

const dataInput = document.getElementById("data-input");
const dataBox = document.getElementById("data-box");
const socket = new WebSocket('ws://' + window.location.host + '/ws/test-stat/');

console.log(socket);

socket.onmessage = function (e) {
  if (socket.readyState === WebSocket.OPEN) {
    console.log('server: ' + e.data);
    const { sender, message } = JSON.parse(e.data);
    dataBox.innerHTML += `<p>${sender}: ${message}</p>`;
    updateChart();
  }
};

submitBtn.addEventListener("click", () => {
  const dataValue = dataInput.value;
  socket.send(JSON.stringify({
    'message': dataValue,
    'sender': user,
  }))
});

const fetchChartData = async () => {
  const response = await fetch(window.location.href + 'chart/');
  console.log(response);
  const data = await response.json();
  console.log(data);
  return data;
};

let chart;

const drawChart = async () => {
  const data = await fetchChartData();
  const { chartData, chartLabels } = data;

  const ctx = document.getElementById('chartCanvas').getContext('2d');
  chart = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: chartLabels,
      datasets: [
        {
          label: '% of contribution',
          data: chartData,
          borderWidth: 1,
        },
      ],
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  });
};

const updateChart = async () => {
  if (chart) {
    chart.destroy();
  }
  await drawChart();
};

drawChart();