import { useEffect, useState } from "react";
import axios from "axios";
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip,
  BarChart, Bar, 
  // PieChart, Pie, Cell, Legend
} from "recharts";
import dayjs from "dayjs";



interface ApiResponse {
  fact: string;
  length: number;
}

interface TimeseriesAPIObject {
  timestamp: string;
  latency: number;
  failed_request: boolean;
  length_correct: boolean;
  punctuation: boolean;
  api_response: ApiResponse;
}


const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";
export default function App() {
  const [data, setData] = useState<TimeseriesAPIObject[]>([]);

  useEffect(() => {
    async function fetchData() {
      try {
        const res = await axios.get(API_URL);
        setData(res.data.response);
      } catch (err) {
        console.error("API fetch failed:", err);
      }
    }
    fetchData();
    const interval = setInterval(fetchData, 10000); // refresh every 5s
    return () => clearInterval(interval);
  }, []);

  if (data.length === 0) return <p>Loading data...</p>;

  return (
    <div style={{ padding: 20, fontFamily: "sans-serif" }}>
      <h1>Cat Fact API Dashboard</h1>

      <section>
        <h3>Latency over Time</h3>
        <LineChart width={600} height={300} data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="timestamp"
            ticks={
              data.length > 0
                ? [0, 0.25, 0.5, 0.75, 1].map((r) =>
                    data[Math.floor(r * (data.length - 1))]?.timestamp
                  )
                : []
            }
            tickFormatter={(t) => dayjs(t).format("HH:mm:ss")}
            interval={0}  // show only these exact ticks
          />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="latency" stroke="#8884d8" />
        </LineChart>
      </section>

      <section style={{ marginTop: 40 }}>
        <h3>Feature Counts</h3>
        <BarChart width={600} height={300} data={[
          {
            name: "Success",
            value: data.filter(d => !d.failed_request).length,
          },
          {
            name: "Failed",
            value: data.filter(d => d.failed_request).length,
          },
          {
            name: "Length Correct",
            value: data.filter(d => d.length_correct).length,
          },
          {
            name: "Has Punctuation",
            value: data.filter(d => d.punctuation).length,
          },
        ]}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis allowDecimals={false}/>
          <Tooltip />
          <Bar dataKey="value" fill="#82ca9d" />
        </BarChart>
      </section>
    </div>
  );
}
