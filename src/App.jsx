import { useState } from "react";
import Login from "./pages/Login";
import Topbar from "./components/Topbar";
import Dashboard from "./pages/Dashboard";

export default function App() {
  const [customer, setCustomer] = useState(() => {
    const savedCustomer = localStorage.getItem("vectorloom_customer");

    return savedCustomer ? JSON.parse(savedCustomer) : null;
  });

  const [active, setActive] = useState("Home");

  function handleLogin(customerData) {
    localStorage.setItem(
      "vectorloom_customer",
      JSON.stringify(customerData)
    );

    setCustomer(customerData);
    setActive("Home");
  }

  function handleLogout() {
    localStorage.removeItem("vectorloom_customer");
    setCustomer(null);
  }

  if (!customer) {
    return <Login onLogin={handleLogin} />;
  }

  return (
    <div className="min-h-screen bg-[#f7f7f5] text-neutral-900">
      <Topbar
        active={active}
        onNavigate={setActive}
        customer={customer}
        onLogout={handleLogout}
      />

      <main>
        {active === "Home" || active === "For You" ? (
          <Dashboard customer={customer} />
        ) : (
          <div className="store-container py-20">
            <div className="text-center">
              <p className="text-xs font-semibold uppercase tracking-[0.2em] text-neutral-400">
                VectorLoom
              </p>

              <h2 className="mt-3 text-2xl font-semibold tracking-tight">
                {active}
              </h2>

              <p className="mt-2 text-sm text-neutral-500">
                This section will be available soon.
              </p>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}