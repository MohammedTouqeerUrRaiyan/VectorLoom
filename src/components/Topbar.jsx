import { Search, Bell } from "lucide-react";

export default function Topbar() {
  return (
    <div className="mb-8 flex items-start justify-between gap-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-white">
          Welcome back, User! <span className="inline-block">👋</span>
        </h1>
        <p className="mt-1 text-sm text-slate-500">
          Here's what's happening with your projects today.
        </p>
      </div>

      <div className="flex items-center gap-4">
        <div className="flex w-72 items-center gap-2.5 rounded-xl border border-white/[0.08] bg-base-850 px-3.5 py-2.5 text-slate-500 transition-colors focus-within:border-accent-blue/50">
          <Search size={16} />
          <input
            type="text"
            placeholder="Search anything..."
            className="w-full bg-transparent text-sm text-slate-200 placeholder:text-slate-500 focus:outline-none"
          />
          <kbd className="rounded-md border border-white/[0.08] bg-white/[0.04] px-1.5 py-0.5 text-[11px] font-medium text-slate-500">
            Ctrl+K
          </kbd>
        </div>

        <button className="relative flex h-10 w-10 items-center justify-center rounded-xl border border-white/[0.08] bg-base-850 text-slate-400 transition-colors hover:text-slate-100">
          <Bell size={17} />
          <span className="absolute -right-1 -top-1 flex h-4 w-4 items-center justify-center rounded-full bg-accent-indigo text-[10px] font-semibold text-white">
            3
          </span>
        </button>

        <div className="flex h-10 w-10 items-center justify-center rounded-full bg-gradient-to-br from-accent-violet to-accent-purple text-sm font-semibold text-white">
          U
        </div>
      </div>
    </div>
  );
}
