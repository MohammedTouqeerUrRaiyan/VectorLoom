import {
  Search,
  Heart,
  ShoppingBag,
  User,
  Menu,
  LogOut,
} from "lucide-react";

export default function Topbar({
  active = "Home",
  onNavigate,
  customer,
  onLogout,
}) {
  return (
    <header className="sticky top-0 z-50 border-b border-neutral-200 bg-white/95 backdrop-blur">
      <div className="store-container">
        <div className="flex h-16 items-center justify-between gap-6">

          {/* Brand */}
          <button
            onClick={() => onNavigate?.("Home")}
            className="flex shrink-0 items-center"
          >
            <span className="text-xl font-bold tracking-[-0.04em] text-black">
              VectorLoom
            </span>
          </button>

          {/* Navigation */}
          <nav className="hidden items-center gap-7 lg:flex">

            <button
              onClick={() => onNavigate?.("Home")}
              className={
                active === "Home"
                  ? "text-sm font-semibold text-black"
                  : "text-sm font-medium text-neutral-500 hover:text-black"
              }
            >
              Home
            </button>

            <button
              onClick={() => onNavigate?.("For You")}
              className={
                active === "For You"
                  ? "text-sm font-semibold text-black"
                  : "text-sm font-medium text-neutral-500 hover:text-black"
              }
            >
              For You
            </button>

            <button
              onClick={() => onNavigate?.("Women")}
              className="text-sm font-medium text-neutral-500 hover:text-black"
            >
              Women
            </button>

            <button
              onClick={() => onNavigate?.("Men")}
              className="text-sm font-medium text-neutral-500 hover:text-black"
            >
              Men
            </button>

            <button
              onClick={() => onNavigate?.("Trending")}
              className="text-sm font-medium text-neutral-500 hover:text-black"
            >
              Trending
            </button>
          </nav>

          {/* Actions */}
          <div className="flex items-center gap-2 sm:gap-3">

            {/* Search */}
            <div className="hidden w-48 items-center gap-2 border-b border-neutral-300 px-1 py-1.5 xl:flex">
              <Search
                size={16}
                strokeWidth={1.8}
                className="shrink-0 text-neutral-500"
              />

              <input
                type="text"
                placeholder="Search products"
                className="w-full bg-transparent text-sm text-neutral-900 placeholder:text-neutral-400 focus:outline-none"
              />
            </div>

            {/* Wishlist */}
            <button
              type="button"
              aria-label="Wishlist"
              className="flex h-9 w-9 items-center justify-center text-neutral-700 transition-colors hover:text-black"
            >
              <Heart size={19} strokeWidth={1.7} />
            </button>

            {/* Shopping bag */}
            <button
              type="button"
              aria-label="Shopping bag"
              className="relative flex h-9 w-9 items-center justify-center text-neutral-700 transition-colors hover:text-black"
            >
              <ShoppingBag size={19} strokeWidth={1.7} />

              <span className="absolute right-0 top-0 flex h-4 min-w-4 items-center justify-center rounded-full bg-black px-1 text-[9px] font-semibold text-white">
                0
              </span>
            </button>

            {/* Customer */}
            <div className="group relative hidden sm:block">

              <button
                type="button"
                className="flex h-9 items-center gap-2 rounded-full px-2 text-neutral-700 hover:bg-neutral-100"
              >
                <div className="flex h-8 w-8 items-center justify-center rounded-full bg-black text-xs font-semibold text-white">
                  {customer?.username?.charAt(0)?.toUpperCase() || "T"}
                </div>

                <span className="hidden text-sm font-medium lg:block">
                  {customer?.username || "Customer"}
                </span>

                <User size={16} className="hidden lg:block" />
              </button>

              {/* Logout */}
              <div className="invisible absolute right-0 top-11 w-48 translate-y-1 rounded-xl border border-neutral-200 bg-white p-2 opacity-0 shadow-lg transition-all group-hover:visible group-hover:translate-y-0 group-hover:opacity-100">

                <div className="border-b border-neutral-100 px-3 py-2">
                  <p className="text-sm font-semibold text-neutral-900">
                    {customer?.username || "Customer"}
                  </p>

                  <p className="mt-1 truncate text-xs text-neutral-400">
                    Personalized account
                  </p>
                </div>

                <button
                  onClick={onLogout}
                  className="mt-1 flex w-full items-center gap-2 rounded-lg px-3 py-2 text-sm text-neutral-600 hover:bg-neutral-100 hover:text-black"
                >
                  <LogOut size={15} />
                  Sign out
                </button>
              </div>
            </div>

            {/* Mobile */}
            <button
              type="button"
              aria-label="Open menu"
              className="flex h-9 w-9 items-center justify-center text-neutral-700 lg:hidden"
            >
              <Menu size={20} strokeWidth={1.8} />
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}