import {
  LayoutDashboard,
  Database,
  Box,
  FlaskConical,
  Code2,
  CheckCircle2,
  FileText,
  Settings,
  Plus,
  Upload,
  Play,
  ClipboardCheck,
  ChevronsUpDown,
} from "lucide-react";

const NAV_ITEMS = [
  { label: "Dashboard", icon: LayoutDashboard },
  { label: "Data", icon: Database },
  { label: "Models", icon: Box },
  { label: "Experiments", icon: FlaskConical },
  { label: "Notebooks", icon: Code2 },
  { label: "Tests", icon: CheckCircle2 },
  { label: "Docs", icon: FileText },
  { label: "Settings", icon: Settings },
];

const QUICK_ACTIONS = [
  { label: "New Project", icon: Plus },
  { label: "Upload Dataset", icon: Upload },
  { label: "Train Model", icon: Play },
  { label: "Run Tests", icon: ClipboardCheck },
];

export default function Sidebar({ active, onNavigate }) {
  return (
    <aside className="flex h-full w-64 shrink-0 flex-col border-r border-white/[0.06] bg-base-900/95 px-4 py-5">
      {/* Logo */}
      <div className="mb-8 flex items-center gap-2.5 px-1.5">
        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-accent-blue to-accent-indigo shadow-glow">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
            <path
              d="M4 12L12 4L20 12L12 20L4 12Z"
              stroke="white"
              strokeWidth="2"
              strokeLinejoin="round"
            />
            <path d="M12 4V20M4 12H20" stroke="white" strokeWidth="1.5" strokeOpacity="0.6" />
          </svg>
        </div>
        <span className="text-[15px] font-bold tracking-tight text-white">VectorLoom</span>
      </div>

      {/* Nav */}
      <nav className="flex flex-col gap-1">
        {NAV_ITEMS.map(({ label, icon: Icon }) => (
          <button
            key={label}
            onClick={() => onNavigate?.(label)}
            className={`nav-item text-left ${active === label ? "active" : ""}`}
          >
            <Icon size={17} strokeWidth={2} />
            {label}
          </button>
        ))}
      </nav>

      {/* Quick actions */}
      <div className="mt-8">
        <p className="mb-2 px-1.5 text-[11px] font-semibold uppercase tracking-wider text-slate-500">
          Quick Actions
        </p>
        <div className="flex flex-col gap-2">
          {QUICK_ACTIONS.map(({ label, icon: Icon }) => (
            <button key={label} className="quick-action">
              <Icon size={16} strokeWidth={2} />
              {label}
            </button>
          ))}
        </div>
      </div>

      <div className="flex-1" />

      {/* User */}
      <button className="flex items-center gap-3 rounded-xl border border-white/[0.06] bg-white/[0.02] px-3 py-2.5 text-left transition-colors hover:bg-white/[0.05]">
        <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-accent-violet to-accent-purple text-xs font-semibold text-white">
          U
        </div>
        <div className="min-w-0 flex-1">
          <p className="truncate text-sm font-medium text-slate-100">User Name</p>
          <p className="truncate text-xs text-slate-500">user@email.com</p>
        </div>
        <ChevronsUpDown size={14} className="shrink-0 text-slate-500" />
      </button>
    </aside>
  );
}
