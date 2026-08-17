import { Folder, Code2, RotateCw, ArrowRight, Star } from "lucide-react";

const PROJECTS = [
  {
    name: "VectorLoom-main",
    updated: "Updated 2 hours ago",
    icon: Folder,
    iconTone: "bg-accent-blue/15 text-accent-blue",
    starred: true,
  },
  {
    name: "airline-dynamics",
    updated: "Updated 1 day ago",
    icon: Code2,
    iconTone: "bg-accent-purple/15 text-accent-purple",
  },
  {
    name: "Qlearning-Project",
    updated: "Updated 3 days ago",
    icon: RotateCw,
    iconTone: "bg-accent-violet/15 text-accent-violet",
  },
  {
    name: "forecasting-model",
    updated: "Updated 5 days ago",
    icon: Code2,
    iconTone: "bg-orange-500/15 text-orange-400",
  },
];

export default function RecentProjects() {
  return (
    <div className="panel p-5">
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-base font-semibold text-white">Recent Projects</h2>
        <button className="flex items-center gap-1.5 text-sm font-medium text-accent-blue hover:text-accent-blue/80">
          View all projects
          <ArrowRight size={14} />
        </button>
      </div>

      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-4">
        {PROJECTS.map(({ name, updated, icon: Icon, iconTone, starred }) => (
          <button
            key={name}
            className="flex flex-col items-start gap-3 rounded-xl border border-white/[0.06] bg-white/[0.02] p-4 text-left transition-all duration-200 hover:-translate-y-0.5 hover:border-white/[0.12] hover:bg-white/[0.04]"
          >
            <div className="flex w-full items-start justify-between">
              <div className={`flex h-9 w-9 items-center justify-center rounded-lg ${iconTone}`}>
                <Icon size={17} />
              </div>
              {starred && <Star size={15} className="fill-amber-400 text-amber-400" />}
            </div>
            <div className="min-w-0">
              <p className="truncate text-sm font-semibold text-slate-100">{name}</p>
              <p className="mt-0.5 text-xs text-slate-500">{updated}</p>
            </div>
            <span className="rounded-md border border-white/[0.08] bg-white/[0.03] px-2 py-0.5 text-[11px] font-medium text-slate-400">
              Python
            </span>
          </button>
        ))}
      </div>
    </div>
  );
}
