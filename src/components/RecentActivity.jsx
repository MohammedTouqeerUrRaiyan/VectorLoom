import { Code2, Database, FlaskConical, CheckCircle2, FileText, ArrowRight } from "lucide-react";

const ACTIVITY = [
  {
    icon: Code2,
    dot: "bg-accent-green",
    title: 'Model "VectorLoom-v1" trained successfully',
    time: "2 hours ago",
  },
  {
    icon: Database,
    dot: "bg-accent-blue",
    title: 'Dataset "airline-dynamics.csv" uploaded',
    time: "5 hours ago",
  },
  {
    icon: FlaskConical,
    dot: "bg-accent-purple",
    title: 'Experiment "Hyperparam Tuning" completed',
    time: "1 day ago",
  },
  {
    icon: CheckCircle2,
    dot: "bg-accent-green",
    title: 'All tests passed for "predict.py"',
    time: "1 day ago",
  },
  {
    icon: FileText,
    dot: "bg-accent-amber",
    title: 'Documentation "README.md" updated',
    time: "2 days ago",
  },
];

export default function RecentActivity() {
  return (
    <div className="panel flex flex-col p-5">
      <h2 className="mb-4 text-base font-semibold text-white">Recent Activity</h2>

      <div className="flex flex-col">
        {ACTIVITY.map(({ icon: Icon, dot, title, time }, i) => (
          <div
            key={i}
            className="flex items-center gap-3 border-b border-white/[0.05] py-3 last:border-none"
          >
            <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-white/[0.04] text-slate-400">
              <Icon size={16} />
            </div>
            <div className="min-w-0 flex-1">
              <p className="truncate text-sm text-slate-200">{title}</p>
              <p className="text-xs text-slate-500">{time}</p>
            </div>
            <span className={`h-2 w-2 shrink-0 rounded-full ${dot}`} />
          </div>
        ))}
      </div>

      <button className="mt-4 flex items-center gap-1.5 self-start rounded-lg border border-white/[0.06] bg-white/[0.02] px-3.5 py-2 text-sm font-medium text-slate-300 transition-colors hover:bg-white/[0.05] hover:text-white">
        View all activity
        <ArrowRight size={14} />
      </button>
    </div>
  );
}
