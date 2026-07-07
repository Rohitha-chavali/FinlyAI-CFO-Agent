"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

type DashboardData = {
  company: string;
  timestamp: string;
  kpis: {
    total_revenue: number;
    total_expenses: number;
    net_profit: number;
    profit_margin: number;
  };
  cashflow: {
    inflow: number;
    outflow: number;
    net: number;
  };
  alerts: string[];
};

export default function Dashboard() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadDashboard() {
      try {
        const res = await fetch("https://finlyai-cfo-agent-2.onrender.com/dashboard");
        const json = await res.json();
        setData(json);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }

    loadDashboard();
  }, []);

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-black text-white">
        Loading FinlyAI Dashboard...
      </div>
    );
  }

  if (!data) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-black text-red-400">
        Failed to connect to backend.
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-black text-white p-10">

      {/* Header */}
      <div className="mb-8 flex items-center justify-between">

        <Link
          href="/"
          className="rounded-xl border border-white/20 px-5 py-2 transition hover:bg-white hover:text-black"
        >
          ← Back to Home
        </Link>

        <div className="rounded-full bg-green-500/20 px-4 py-2 text-sm text-green-400">
          ● Backend Connected
        </div>

      </div>

      <h1 className="mb-2 text-5xl font-bold">
        {data.company} Dashboard
      </h1>

      <p className="mb-10 text-gray-400">
        Updated: {new Date(data.timestamp).toLocaleString()}
      </p>

      {/* KPI Cards */}

      <div className="grid gap-6 md:grid-cols-4">

        <Card
          title="Revenue"
          value={`₹${data.kpis.total_revenue.toLocaleString()}`}
        />

        <Card
          title="Expenses"
          value={`₹${data.kpis.total_expenses.toLocaleString()}`}
        />

        <Card
          title="Net Profit"
          value={`₹${data.kpis.net_profit.toLocaleString()}`}
        />

        <Card
          title="Profit Margin"
          value={`${data.kpis.profit_margin}%`}
        />

      </div>

      {/* Cash Flow */}

      <div className="mt-8 grid gap-6 md:grid-cols-3">

        <Card
          title="Cash Inflow"
          value={`₹${data.cashflow.inflow.toLocaleString()}`}
        />

        <Card
          title="Cash Outflow"
          value={`₹${data.cashflow.outflow.toLocaleString()}`}
        />

        <Card
          title="Net Cash"
          value={`₹${data.cashflow.net.toLocaleString()}`}
        />

      </div>

      {/* AI Insights */}

      <div className="mt-10 rounded-3xl border border-white/10 bg-white/5 p-8">

        <h2 className="mb-5 text-2xl font-semibold">
          🤖 AI CFO Insights
        </h2>

        <ul className="space-y-4">
          {data.alerts.map((alert, index) => (
            <li
              key={index}
              className="rounded-xl border border-white/10 bg-black/30 p-4"
            >
              {alert}
            </li>
          ))}
        </ul>

      </div>

    </main>
  );
}

function Card({
  title,
  value,
}: {
  title: string;
  value: string;
}) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 p-6 transition hover:border-blue-500 hover:bg-white/10">

      <h2 className="text-sm text-gray-400">
        {title}
      </h2>

      <p className="mt-3 text-3xl font-bold">
        {value}
      </p>

    </div>
  );
}