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

    const res = await api.post("api/upload/", formData, {
    headers: {
        "Content-Type": "multipart/form-data",
    },
    });
    
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
      <h2>Dashboard</h2>

      <input type="file" onChange={e => setFile(e.target.files[0])} />
      <button onClick={upload}>Upload CSV</button>

      {chartData && <Bar data={chartData} />}

      <h3>Last 5 uploads</h3>
      <ul>
        {datasets.map(d => (
          <li key={d.id}>
            {d.file.split("/").pop()}
            {" "}
            <a href={`http://127.0.0.1:8000${d.pdf_url}`} target="_blank" rel="noreferrer">
              Download PDF
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
}
