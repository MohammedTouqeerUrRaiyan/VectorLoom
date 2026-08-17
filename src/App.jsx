import { useState } from "react";
import Sidebar from "./components/Sidebar";
import Dashboard from "./pages/Dashboard";

export default function App() {
  const [active, setActive] = useState("Dashboard");

  return (
    <div className="flex h-screen w-full overflow-hidden bg-base-950 text-slate-200">
      <Sidebar active={active} onNavigate={setActive} />
      {active === "Dashboard" ? (
        <Dashboard />
      ) : (
        <div className="flex flex-1 items-center justify-center text-slate-500">
          <p className="text-sm">
            <span className="font-medium text-slate-300">{active}</span> — coming soon.
          </p>
        </div>
      )}
    </div>
  );
}
