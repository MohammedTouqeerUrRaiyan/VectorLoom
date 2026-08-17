import { PlayCircle, UploadCloud, FlaskConical, ClipboardCheck, ChevronRight } from "lucide-react";

const ITEMS = [
  {
    icon: PlayCircle,
    title: "New Notebook",
    subtitle: "Start coding in a notebook",
    tone: "text-accent-blue bg-accent-blue/15",
  },
  {
    icon: UploadCloud,
    title: "Upload Data",
    subtitle: "Import your dataset",
    tone: "text-accent-green bg-accent-green/15",
  },
  {
    icon: FlaskConical,
    title: "Train a Model",
    subtitle: "Train with your data",
    tone: "text-accent-violet bg-accent-violet/15",
  },
  {
    icon: ClipboardCheck,
    title: "Run Tests",
    subtitle: "Validate your code",
    tone: "text-accent-amber bg-accent-amber/15",
  },
];

export default function QuickStart() {
  return (
    <div className="panel p-5">
      <h2 className="mb-4 text-base font-semibold text-white">Quick Start</h2>
      <div className="flex flex-col gap-1.5">
        {ITEMS.map(({ icon: Icon, title, subtitle, tone }) => (
          <button
            key={title}
            className="flex items-center gap-3 rounded-xl px-2.5 py-2.5 text-left transition-colors hover:bg-white/[0.04]"
          >
            <div className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-lg ${tone}`}>
              <Icon size={17} />
            </div>
            <div className="min-w-0 flex-1">
              <p className="text-sm font-medium text-slate-100">{title}</p>
              <p className="text-xs text-slate-500">{subtitle}</p>
            </div>
            <ChevronRight size={16} className="shrink-0 text-slate-600" />
          </button>
        ))}
      </div>
    </div>
  );
}
