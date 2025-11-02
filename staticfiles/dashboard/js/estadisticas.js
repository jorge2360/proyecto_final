document.addEventListener("DOMContentLoaded", function () {
  // Obtener los datos desde el bloque JSON del template
  const chartDataElement = document.getElementById("chartData");
  if (!chartDataElement) return;

  const chartData = JSON.parse(chartDataElement.textContent);

  const ctx = document.getElementById("chartPedidos");
  if (!ctx) return;

  new Chart(ctx, {
    type: "line",
    data: {
      labels: chartData.labels,
      datasets: [
        {
          label: "Pedidos por mes",
          data: chartData.values,
          borderColor: "#6c63ff",
          backgroundColor: "rgba(108,99,255,0.2)",
          borderWidth: 2,
          tension: 0.3,
          fill: true,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
      },
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  });
});
