import React, { useEffect, useState } from 'react';
import axios from 'axios';
import WeatherSummaryChart from './WeatherSummaryChart';

const App = () => {
    const [summary, setSummary] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const result = await axios.get("http://localhost:8000/summaries");
                setSummary(result.data);
            } catch (error) {
                console.error("Error fetching data:", error);
            }
        };
        fetchData();
    }, []);

    return (
        <div className="App">
            <h1>Weather Monitoring Dashboard</h1>
            <WeatherSummaryChart data={summary} />
        </div>
    );
};

export default App;
