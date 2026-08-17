import { ArrowRight } from "lucide-react";

const METRICS = [
  { label: "Storage", value: 68, color: "bg-accent-blue" },
  { label: "CPU Usage", value: 42, color: "bg-accent-green" },
  { label: "Memory", value: 71, color: "bg-accent-violet" },
  { label: "GPU", value: 23, color: "bg-accent-purple" },
];

export default function SystemStatus() {
  return (
    <div className="panel p-5">
      <h2 className="mb-4 text-base font-semibold text-white">System Status</h2>

      <div className="flex flex-col gap-4">
        {METRICS.map(({ label, value, color }) => (
          <div key={label}>
            <div className="mb-1.5 flex items-center justify-between text-sm">
              <span className="text-slate-300">{label}</span>
              <span className="font-medium text-slate-400">{value}%</span>
            </div>
            <div className="h-1.5 w-full overflow-hidden rounded-full bg-white/[0.06]">
              <div
                className={`h-full rounded-full ${color} transition-all duration-500`}
                style={{ width: `${value}%` }}
              />
            </div>
          </div>
        ))}
      </div>

      <button className="mt-5 flex items-center gap-1.5 text-sm font-medium text-accent-blue hover:text-accent-blue/80">
        View system details
        <ArrowRight size={14} />
      </button>
    </div>
  );
}
