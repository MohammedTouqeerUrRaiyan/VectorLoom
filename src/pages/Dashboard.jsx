import { Database, Box, FlaskConical, CheckCircle2, Lightbulb } from "lucide-react";
import Topbar from "../components/Topbar";
import StatCard from "../components/StatCard";
import RecentActivity from "../components/RecentActivity";
import ModelPerformance from "../components/ModelPerformance";
import RecentProjects from "../components/RecentProjects";
import QuickStart from "../components/QuickStart";
import SystemStatus from "../components/SystemStatus";

const STATS = [
  { label: "Datasets", value: "12", delta: "↑ 2 this week", icon: Database, tone: "blue" },
  { label: "Models", value: "8", delta: "↑ 1 this week", icon: Box, tone: "purple" },
  { label: "Experiments", value: "24", delta: "↑ 5 this week", icon: FlaskConical, tone: "violet" },
  { label: "Tests Passed", value: "92%", delta: "↑ 8% this week", icon: CheckCircle2, tone: "green" },
];

export default function Dashboard() {
  return (
    <div className="flex-1 overflow-y-auto px-8 py-7">
      <Topbar />

      {/* Stat cards */}
      <div className="mb-6 grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {STATS.map((s) => (
          <StatCard key={s.label} {...s} />
        ))}
      </div>

      <div className="grid grid-cols-1 gap-6 xl:grid-cols-3">
        {/* Main column */}
        <div className="flex flex-col gap-6 xl:col-span-2">
          <div className="grid grid-cols-1 gap-6 lg:grid-cols-5">
            <div className="lg:col-span-2">
              <RecentActivity />
            </div>
            <div className="lg:col-span-3">
              <ModelPerformance />
            </div>
          </div>
          <RecentProjects />
        </div>

        {/* Side column */}
        <div className="flex flex-col gap-6">
          <QuickStart />
          <SystemStatus />

          <div className="panel p-5">
            <div className="mb-2 flex items-center gap-2 text-amber-400">
              <Lightbulb size={18} className="fill-amber-400/20" />
              <h2 className="text-base font-semibold text-white">Tips &amp; Tricks</h2>
            </div>
            <p className="mb-4 text-sm leading-relaxed text-slate-400">
              Use keyboard shortcuts to boost your productivity.
            </p>
            <button className="w-full rounded-xl border border-white/[0.08] bg-white/[0.03] py-2.5 text-sm font-medium text-slate-200 transition-colors hover:bg-white/[0.06]">
              View Shortcuts
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
