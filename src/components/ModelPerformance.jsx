import { useState } from "react";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";
import { ChevronDown } from "lucide-react";

const DATA = [
  { day: "Mon", accuracy: 65 },
  { day: "Tue", accuracy: 78 },
  { day: "Wed", accuracy: 76 },
  { day: "Thu", accuracy: 87 },
  { day: "Fri", accuracy: 80 },
  { day: "Sat", accuracy: 83 },
  { day: "Sun", accuracy: 86 },
];

const METRICS = [
  { label: "Accuracy", value: "87%", delta: "↑ 8%", active: true },
  { label: "Precision", value: "83%", delta: "↑ 6%" },
  { label: "Recall", value: "81%", delta: "↑ 7%" },
  { label: "F1 Score", value: "82%", delta: "↑ 7%" },
];

function CustomTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  return (
    <div className="rounded-lg border border-white/10 bg-base-800 px-3.5 py-2.5 shadow-xl">
      <p className="text-xs font-medium text-slate-400">{label}</p>
      <p className="text-sm font-semibold text-white">Accuracy: {payload[0].value}%</p>
    </div>
  );
}

export default function ModelPerformance() {
  const [range, setRange] = useState("This Week");

  return (
    <div className="panel flex flex-col p-5">
      <div className="mb-2 flex items-center justify-between">
        <h2 className="text-base font-semibold text-white">Model Performance</h2>
        <button className="flex items-center gap-1.5 rounded-lg border border-white/[0.08] bg-white/[0.02] px-3 py-1.5 text-xs font-medium text-slate-300 hover:bg-white/[0.05]">
          {range}
          <ChevronDown size={13} />
        </button>
      </div>

      <div className="h-64 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={DATA} margin={{ top: 16, right: 8, left: -18, bottom: 0 }}>
            <defs>
              <linearGradient id="accuracyFill" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#5B8DEF" stopOpacity={0.35} />
                <stop offset="100%" stopColor="#5B8DEF" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid vertical={false} stroke="rgba(255,255,255,0.05)" />
            <XAxis
              dataKey="day"
              axisLine={false}
              tickLine={false}
              tick={{ fill: "#64748B", fontSize: 12 }}
              dy={8}
            />
            <YAxis
              domain={[0, 100]}
              ticks={[0, 25, 50, 75, 100]}
              tickFormatter={(v) => `${v}%`}
              axisLine={false}
              tickLine={false}
              tick={{ fill: "#64748B", fontSize: 12 }}
            />
            <Tooltip content={<CustomTooltip />} cursor={{ stroke: "rgba(255,255,255,0.1)" }} />
            <Area
              type="monotone"
              dataKey="accuracy"
              stroke="#5B8DEF"
              strokeWidth={2.5}
              fill="url(#accuracyFill)"
              dot={{ r: 3, fill: "#5B8DEF", strokeWidth: 0 }}
              activeDot={{ r: 5, fill: "#5B8DEF", stroke: "#0B0F1A", strokeWidth: 3 }}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      <div className="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-4">
        {METRICS.map(({ label, value, delta, active }) => (
          <div
            key={label}
            className={`rounded-xl border px-4 py-3 ${
              active
                ? "border-accent-blue/40 bg-accent-blue/[0.08]"
                : "border-white/[0.06] bg-white/[0.02]"
            }`}
          >
            <p className="text-xs font-medium text-slate-400">{label}</p>
            <div className="mt-1 flex items-baseline gap-1.5">
              <span className="text-xl font-bold text-white">{value}</span>
              <span className="text-xs font-medium text-emerald-400">{delta}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
