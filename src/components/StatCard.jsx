export default function StatCard({ label, value, delta, icon: Icon, tone }) {
  const tones = {
    blue: {
      bg: "bg-gradient-to-br from-accent-blue/15 via-base-850 to-base-850",
      iconWrap: "bg-accent-blue/15 text-accent-blue",
      delta: "text-emerald-400",
    },
    violet: {
      bg: "bg-gradient-to-br from-accent-violet/15 via-base-850 to-base-850",
      iconWrap: "bg-accent-violet/15 text-accent-violet",
      delta: "text-emerald-400",
    },
    purple: {
      bg: "bg-gradient-to-br from-accent-purple/15 via-base-850 to-base-850",
      iconWrap: "bg-accent-purple/15 text-accent-purple",
      delta: "text-emerald-400",
    },
    green: {
      bg: "bg-gradient-to-br from-accent-green/15 via-base-850 to-base-850",
      iconWrap: "bg-accent-green/15 text-accent-green",
      delta: "text-emerald-400",
    },
  };

  const t = tones[tone] ?? tones.blue;

  return (
    <div className={`stat-card ${t.bg}`}>
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-slate-400">{label}</p>
          <p className="mt-2 text-3xl font-bold tracking-tight text-white">{value}</p>
        </div>
        <div className={`flex h-10 w-10 items-center justify-center rounded-xl ${t.iconWrap}`}>
          <Icon size={20} strokeWidth={2} />
        </div>
      </div>
      <p className={`mt-3 text-xs font-medium ${t.delta}`}>{delta}</p>
    </div>
  );
}
