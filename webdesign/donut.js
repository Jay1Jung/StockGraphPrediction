function updateDonutChart() {
    // Data: Name and percentage
    const sectors = [
        { name: "Energy", value: -0.41 },
        { name: "Health Care", value: -0.02 },
        { name: "Communication Services", value: 2.13 },
        { name: "Information Technology", value: 1.44 },
        { name: "Materials", value: 0.65},
        { name: "Consumer Discretionary", value: 0.61},
        { name: "Industrials", value: -3.1},
        { name: "Financials", value: -2.22},
        { name: "Consumer staples", value: -1.44},
        { name: "Utilities", value: -1.28},
        { name: "Real Estate", value: -5}
  
    ];
  
    const sectorsWithColors = sectors.map((sector) => ({
      ...sector,
      color: sector.value > 1
          ? "#4caf50" // Positive: Green
          : sector.value < 1 && sector.value > 0
          ? "#ffeb3b" // Negative: Red
          : "#f44336", // Neutral: Yellow
  }));
  const total = sectorsWithColors.reduce((sum, sector) => sum + Math.abs(sector.value), 0);
  
  let gradientStops = [];
  let currentAngle = 0;
  
  // Loop through each sector to calculate proportional size
  sectorsWithColors.forEach((sector) => {
      const percentage = (Math.abs(sector.value) / total) * 100; // Percentage of total
      const angle = (percentage / 100) * 360; // Convert percentage to angle
      const nextAngle = currentAngle + angle;
  
      // Add gradient stop for this sector
     gradientStops.push(`${sector.color} ${currentAngle}deg ${nextAngle}deg`);
  
      // Update current angle for the next sector
      currentAngle = nextAngle;
  });
  
  // Apply the `conic-gradient` to the chart background
  const donutChart = document.querySelector('.donut-chart');
  donutChart.style.background = `conic-gradient(${gradientStops.join(', ')})`;
  }
  
  // Initialize the chart
  updateDonutChart();