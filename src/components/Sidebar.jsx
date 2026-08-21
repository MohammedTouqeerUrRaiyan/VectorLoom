import {
  Home,
  Sparkles,
  Compass,
  Heart,
  User,
  LogOut,
  ChevronsUpDown,
} from "lucide-react";

const NAV_ITEMS = [
  { label: "Home", icon: Home },
  { label: "For You", icon: Sparkles },
  { label: "Discover", icon: Compass },
  { label: "Favorites", icon: Heart },
];

export default function Sidebar({
  active,
  onNavigate,
  customer,
  onLogout,
}) {
  const name = customer?.name || "Touqeer";

  return (
    <aside className="flex h-screen w-64 shrink-0 flex-col border-r border-white/[0.06] bg-base-900/95 px-4 py-5">

      {/* Logo */}
      <div className="mb-10 flex items-center gap-2.5 px-1.5">
        <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-accent-blue to-accent-indigo shadow-glow">
          <svg
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
          >
            <path
              d="M4 12L12 4L20 12L12 20L4 12Z"
              stroke="white"
              strokeWidth="2"
              strokeLinejoin="round"
            />

            <path
              d="M12 4V20M4 12H20"
              stroke="white"
              strokeWidth="1.5"
              strokeOpacity="0.6"
            />
          </svg>
        </div>

        <span className="text-[15px] font-bold tracking-tight text-white">
          VectorLoom
        </span>
      </div>

      {/* Navigation */}
      <nav className="flex flex-col gap-1">

        {NAV_ITEMS.map(({ label, icon: Icon }) => (
          <button
            key={label}
            onClick={() => onNavigate?.(label)}
            className={`nav-item text-left ${
              active === label ? "active" : ""
            }`}
          >
            <Icon size={17} strokeWidth={2} />

            {label}
          </button>
        ))}

      </nav>

      {/* Recommendation engine information */}
      <div className="mt-8 rounded-2xl border border-blue-400/10 bg-blue-400/[0.04] p-4">

        <div className="mb-2 flex items-center gap-2">
          <Sparkles
            size={16}
            className="text-blue-400"
          />

          <span className="text-xs font-semibold text-white">
            VectorLoom AI
          </span>
        </div>

        <p className="text-xs leading-relaxed text-slate-500">
          Personalized recommendations powered by
          collaborative and content-based intelligence.
        </p>

      </div>

      <div className="flex-1" />

      {/* User */}
      <div className="relative">

        <button className="flex w-full items-center gap-3 rounded-xl border border-white/[0.06] bg-white/[0.02] px-3 py-2.5 text-left transition-colors hover:bg-white/[0.05]">

          <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-accent-violet to-accent-purple text-xs font-semibold text-white">
            {name.charAt(0).toUpperCase()}
          </div>

          <div className="min-w-0 flex-1">

            <p className="truncate text-sm font-medium text-slate-100">
              {name}
            </p>

            <p className="truncate text-xs text-slate-500">
              Personalized shopper
            </p>

          </div>

          <ChevronsUpDown
            size={14}
            className="shrink-0 text-slate-500"
          />

        </button>

        {/* Logout */}
        {onLogout && (
          <button
            onClick={onLogout}
            className="mt-2 flex w-full items-center gap-2 rounded-xl px-3 py-2 text-xs text-slate-500 transition-colors hover:bg-red-400/[0.06] hover:text-red-400"
          >
            <LogOut size={14} />
            Sign out
          </button>
        )}

      </div>

    </aside>
  );
}