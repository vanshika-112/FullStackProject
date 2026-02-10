import { useEffect, useState } from "react";
import api from "../services/api";
import { Bar } from "react-chartjs-2";

import {
  Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend
);

export default function Dashboard() {
  const [file, setFile] = useState(null);
  const [datasets, setDatasets] = useState([]);
  const [chartData, setChartData] = useState(null);
  const [summary, setSummary] = useState(null);

  const fetchLastFive = async () => {
    const res = await api.get("datasets/last-five/");
    setDatasets(res.data);
  };

  useEffect(() => {
    fetchLastFive();
  }, []);

  const upload = async () => {
    const formData = new FormData();
    formData.append("file", file);

    const res = await api.post("upload/", formData);
    setSummary(res.data);

    fetchLastFive();

    const dist = res.data.equipment_distribution;
    setChartData({
      labels: Object.keys(dist),
      datasets: [
        {
          label: "Equipment Distribution",
          data: Object.values(dist),
        },
      ],
    });
  };

  return (
    <div>
      <h2 align="center">Dashboard</h2>
      <p align="center">Upload your file here : &emsp;   
        <input type="file" onChange={e => setFile(e.target.files[0])} />
        <br />
        <br />
        <button onClick={upload}>Upload CSV</button>
      </p>
      {chartData && <Bar data={chartData} />}

      {summary && (
        <><div style={{ marginTop: "20px" }}>
          <h3 align="center">Dataset Summary</h3>
          <div align="center">
            <p><strong>Total Records:</strong> {summary.total_count}</p>
          </div>
          <div style={{ display: 'flex', justifyContent: 'center' , gap: '20px'}}>
            <div>
              <h4 align="center">Averages</h4>
              <ul>
                {Object.entries(summary.averages || {}).map(([key, value]) => (
                  <li key={key}>{key}: {value}</li>
                ))}
              </ul>
            </div>
            <div>
              <h4 align="center">Equipment Distribution</h4>
              <ul>
                {Object.entries(summary.equipment_distribution || {}).map(([key, value]) => (
                  <li key={key}>{key}: {value}</li>
                ))}
              </ul>
            </div>
          </div>
          </div>
          <div align="center">
            <button
            style={{ marginTop: "15px" }}
            onClick={() => window.open(summary.pdf_url,
              "_blank")}>
              Download PDF
            </button>
          </div>
          </>
      )}
      <div align="center">
        <h3>Last 5 uploads</h3>
        <div style={{ display: 'flex', justifyContent: 'center' }}>
          <ul>
            {datasets.map(d => (
              <li key={d.id}>
                {d.file.split("/").pop()}
                {" "}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
