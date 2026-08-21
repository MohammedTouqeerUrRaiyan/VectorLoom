import { Heart, ArrowUpRight } from "lucide-react";

function getColourClass(colour = "") {
  const value = colour.toLowerCase();

  if (value.includes("black")) {
    return "from-zinc-800 via-zinc-900 to-black";
  }

  if (value.includes("white")) {
    return "from-white via-slate-100 to-slate-300";
  }

  if (value.includes("grey") || value.includes("gray")) {
    return "from-slate-400 via-slate-500 to-slate-700";
  }

  if (value.includes("green")) {
    return "from-emerald-700 via-green-800 to-slate-900";
  }

  if (value.includes("blue")) {
    return "from-blue-600 via-blue-800 to-slate-900";
  }

  if (value.includes("red")) {
    return "from-red-600 via-red-800 to-slate-900";
  }

  if (value.includes("yellow")) {
    return "from-yellow-400 via-yellow-600 to-slate-900";
  }

  return "from-slate-700 via-slate-800 to-slate-950";
}

export default function ProductCard({ product }) {
  const score = Math.round(product.score * 100);

  return (
    <article className="group overflow-hidden rounded-2xl border border-slate-200 bg-white transition-all duration-300 hover:-translate-y-1 hover:shadow-xl">
      {/* Product visual */}
      <div
        className={`relative flex h-72 items-center justify-center overflow-hidden bg-gradient-to-br ${getColourClass(
          product.colour
        )}`}
      >
        <div className="text-center">
          <p className="text-[11px] font-semibold uppercase tracking-[0.25em] text-white/60">
            {product.product_type || "Product"}
          </p>

          <p className="mt-2 text-sm font-medium uppercase tracking-wider text-white/80">
            {product.colour || "Unknown colour"}
          </p>
        </div>

        {/* Wishlist */}
        <button
          type="button"
          aria-label={`Add ${product.product_name} to wishlist`}
          className="absolute right-4 top-4 flex h-9 w-9 items-center justify-center rounded-full bg-white/90 text-slate-700 shadow-sm transition hover:bg-white"
        >
          <Heart size={17} />
        </button>

        {/* Recommendation score */}
        <div className="absolute bottom-4 left-4 rounded-full bg-white px-3 py-1.5 text-xs font-semibold text-slate-900 shadow-sm">
          {score}% Match
        </div>

        {/* Arrow */}
        <button
          type="button"
          aria-label={`View ${product.product_name}`}
          className="absolute bottom-4 right-4 flex h-9 w-9 translate-y-2 items-center justify-center rounded-full bg-white text-slate-900 opacity-0 shadow-sm transition-all duration-300 group-hover:translate-y-0 group-hover:opacity-100"
        >
          <ArrowUpRight size={17} />
        </button>
      </div>

      {/* Product information */}
      <div className="p-5">
        <div className="mb-2">
          <h3 className="truncate text-base font-semibold text-slate-900">
            {product.product_name}
          </h3>

          <p className="mt-1 text-sm text-slate-500">
            {product.product_type} · {product.colour}
          </p>
        </div>

        <div className="mb-3 flex flex-wrap gap-2">
          <span className="rounded-full bg-slate-100 px-2.5 py-1 text-[11px] font-medium text-slate-600">
            {product.product_group}
          </span>

          <span className="rounded-full bg-slate-100 px-2.5 py-1 text-[11px] font-medium text-slate-600">
            {product.graphical_appearance || "Solid"}
          </span>
        </div>

        <p className="line-clamp-2 text-sm leading-relaxed text-slate-500">
          {product.description}
        </p>

        <div className="mt-4 border-t border-slate-100 pt-4">
          <p className="text-xs font-medium text-slate-400">
            {product.reason === "Content"
              ? "Matches your style"
              : "Recommended for you"}
          </p>

          <p className="mt-1 text-xs text-slate-500">
            {product.reason === "Content"
              ? "Based on product characteristics and similarity."
              : "Combines customer behavior with product similarity."}
          </p>
        </div>
      </div>
    </article>
  );
}