import React from 'react';
import { Line } from 'react-chartjs-2';

const WeatherSummaryChart = ({ data }) => {
    const dates = data.map(item => item.date);
    const avgTemps = data.map(item => item.average_temp);
    const maxTemps = data.map(item => item.max_temp);
    const minTemps = data.map(item => item.min_temp);

    const chartData = {
        labels: dates,
        datasets: [
            {
                label: 'Average Temperature (°C)',
                data: avgTemps,
                borderColor: 'rgba(75,192,192,1)',
                fill: false,
            },
            {
                label: 'Max Temperature (°C)',
                data: maxTemps,
                borderColor: 'rgba(255,99,132,1)',
                fill: false,
            },
            {
                label: 'Min Temperature (°C)',
                data: minTemps,
                borderColor: 'rgba(54, 162, 235, 1)',
                fill: false,
            },
        ],
    };

    return (
        <div>
            <h2>Daily Temperature Summary</h2>
            <Line data={chartData} />
        </div>
    );
};

export default WeatherSummaryChart;
