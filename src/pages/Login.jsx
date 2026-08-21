import { useState } from "react";
import { Eye, EyeOff, Sparkles } from "lucide-react";
import { authenticateCustomer } from "../config/customers";

export default function Login({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");

  function handleSubmit(event) {
    event.preventDefault();

    setError("");

    const customer = authenticateCustomer(username, password);

    if (!customer) {
      setError("Invalid username or password.");
      return;
    }

    onLogin(customer);
  }

  return (
    <div className="min-h-screen bg-[#f7f7f5]">
      <div className="grid min-h-screen lg:grid-cols-2">

        {/* Brand panel */}
        <div className="relative hidden overflow-hidden bg-[#111111] lg:flex">
          <div className="absolute inset-0 bg-gradient-to-br from-neutral-900 via-neutral-800 to-black" />

          <div className="relative z-10 flex w-full flex-col justify-between p-12">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-white">
                <Sparkles size={18} className="text-black" />
              </div>

              <span className="text-xl font-semibold tracking-tight text-white">
                VectorLoom
              </span>
            </div>

            <div className="max-w-lg">
              <p className="mb-5 text-sm font-medium uppercase tracking-[0.2em] text-neutral-400">
                Personalized fashion intelligence
              </p>

              <h1 className="text-5xl font-semibold leading-tight tracking-tight text-white">
                Fashion recommendations,
                <br />
                tailored to you.
              </h1>

              <p className="mt-6 max-w-md text-base leading-7 text-neutral-400">
                VectorLoom combines customer behavior and product
                similarity to discover products you'll love.
              </p>
            </div>

            <p className="text-xs text-neutral-500">
              AI-powered recommendation engine
            </p>
          </div>
        </div>

        {/* Login */}
        <div className="flex items-center justify-center px-6 py-12">
          <div className="w-full max-w-md">

            <div className="mb-10 lg:hidden">
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-black">
                  <Sparkles size={18} className="text-white" />
                </div>

                <span className="text-xl font-semibold">
                  VectorLoom
                </span>
              </div>
            </div>

            <div className="mb-8">
              <p className="mb-2 text-sm font-medium uppercase tracking-[0.16em] text-neutral-400">
                Welcome back
              </p>

              <h2 className="text-3xl font-semibold tracking-tight text-neutral-900">
                Sign in to VectorLoom
              </h2>

              <p className="mt-2 text-sm text-neutral-500">
                Discover recommendations selected specifically for you.
              </p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-5">

              <div>
                <label className="mb-2 block text-sm font-medium text-neutral-700">
                  Username
                </label>

                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="Enter username"
                  className="w-full rounded-xl border border-neutral-200 bg-white px-4 py-3 text-sm text-neutral-900 outline-none transition focus:border-neutral-500"
                  required
                />
              </div>

              <div>
                <label className="mb-2 block text-sm font-medium text-neutral-700">
                  Password
                </label>

                <div className="relative">
                  <input
                    type={showPassword ? "text" : "password"}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Enter password"
                    className="w-full rounded-xl border border-neutral-200 bg-white px-4 py-3 pr-12 text-sm text-neutral-900 outline-none transition focus:border-neutral-500"
                    required
                  />

                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-neutral-400 hover:text-neutral-700"
                  >
                    {showPassword ? (
                      <EyeOff size={18} />
                    ) : (
                      <Eye size={18} />
                    )}
                  </button>
                </div>
              </div>

              {error && (
                <div className="rounded-xl border border-red-100 bg-red-50 px-4 py-3 text-sm text-red-600">
                  {error}
                </div>
              )}

              <button
                type="submit"
                className="w-full rounded-xl bg-black py-3.5 text-sm font-semibold text-white transition hover:bg-neutral-800"
              >
                Sign in
              </button>
            </form>

            {/* Demo credentials */}
            <div className="mt-8 rounded-xl border border-neutral-200 bg-white p-4">
              <p className="text-xs font-semibold uppercase tracking-wider text-neutral-400">
                Demo account
              </p>

              <div className="mt-3 flex justify-between text-sm">
                <span className="text-neutral-500">
                  Username
                </span>

                <span className="font-medium text-neutral-900">
                  Touqeer
                </span>
              </div>

              <div className="mt-2 flex justify-between text-sm">
                <span className="text-neutral-500">
                  Password
                </span>

                <span className="font-medium text-neutral-900">
                  password123
                </span>
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>
  );
}