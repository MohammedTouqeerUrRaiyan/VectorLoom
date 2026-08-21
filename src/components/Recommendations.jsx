import { useEffect, useState } from "react";
import {
  Sparkles,
  Users,
  Brain,
  TrendingUp,
  RefreshCw,
} from "lucide-react";

const API_BASE_URL = "http://127.0.0.1:8000";

const FALLBACK_CUSTOMER_ID =
  "75c54a755b8a467e53e0a4e01833deb029734feb22ad25438137925123a38f8b";

export default function Recommendations({ customer }) {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const customerId =
    customer?.customer_id ||
    customer?.id ||
    FALLBACK_CUSTOMER_ID;

  async function fetchRecommendations() {
    try {
      setLoading(true);
      setError("");

      const response = await fetch(
        `${API_BASE_URL}/api/v1/recommendations/${customerId}?limit=5`
      );

      if (!response.ok) {
        throw new Error(
          `Recommendation API returned ${response.status}`
        );
      }

      const data = await response.json();

      setRecommendations(data.recommendations || []);
    } catch (err) {
      console.error("Recommendation error:", err);
      setError("Unable to load recommendations.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchRecommendations();
  }, [customerId]);

  if (loading) {
    return (
      <section className="panel p-6">
        <div className="flex items-center gap-3">
          <Sparkles className="text-blue-400" size={20} />

          <div>
            <h2 className="text-lg font-semibold text-white">
              Personalized Recommendations
            </h2>

            <p className="text-sm text-slate-400">
              VectorLoom is generating recommendations...
            </p>
          </div>
        </div>
      </section>
    );
  }

  if (error) {
    return (
      <section className="panel p-6">
        <h2 className="mb-2 text-lg font-semibold text-white">
          Personalized Recommendations
        </h2>

        <p className="text-sm text-red-400">
          {error}
        </p>

        <button
          onClick={fetchRecommendations}
          className="mt-4 flex items-center gap-2 rounded-xl border border-white/[0.08] px-4 py-2 text-sm text-slate-300 hover:bg-white/[0.05]"
        >
          <RefreshCw size={15} />
          Retry
        </button>
      </section>
    );
  }

  return (
    <section className="panel p-6">

      {/* Header */}
      <div className="mb-6 flex items-start justify-between gap-4">

        <div>
          <div className="mb-2 flex items-center gap-2">
            <Sparkles
              size={20}
              className="text-blue-400"
            />

            <h2 className="text-lg font-semibold text-white">
              Recommended for You
            </h2>
          </div>

          <p className="text-sm text-slate-400">
            Personalized recommendations powered by
            VectorLoom's hybrid recommendation engine.
          </p>
        </div>

        <button
          onClick={fetchRecommendations}
          title="Refresh recommendations"
          className="rounded-xl border border-white/[0.08] p-2 text-slate-400 transition hover:bg-white/[0.05] hover:text-white"
        >
          <RefreshCw size={16} />
        </button>
      </div>

      {/* Recommendation explanation */}
      <div className="mb-6 grid grid-cols-1 gap-3 md:grid-cols-3">

        <div className="rounded-xl border border-blue-400/10 bg-blue-400/[0.04] p-4">
          <div className="mb-2 flex items-center gap-2">
            <Users size={16} className="text-blue-400" />

            <span className="text-xs font-semibold uppercase tracking-wide text-blue-400">
              Collaborative
            </span>
          </div>

          <p className="text-xs leading-relaxed text-slate-400">
            Learns from behavior patterns of similar customers.
          </p>
        </div>

        <div className="rounded-xl border border-purple-400/10 bg-purple-400/[0.04] p-4">
          <div className="mb-2 flex items-center gap-2">
            <Brain size={16} className="text-purple-400" />

            <span className="text-xs font-semibold uppercase tracking-wide text-purple-400">
              Content-Based
            </span>
          </div>

          <p className="text-xs leading-relaxed text-slate-400">
            Compares product attributes and descriptions.
          </p>
        </div>

        <div className="rounded-xl border border-emerald-400/10 bg-emerald-400/[0.04] p-4">
          <div className="mb-2 flex items-center gap-2">
            <TrendingUp size={16} className="text-emerald-400" />

            <span className="text-xs font-semibold uppercase tracking-wide text-emerald-400">
              Hybrid Ranking
            </span>
          </div>

          <p className="text-xs leading-relaxed text-slate-400">
            Combines both signals to rank the final products.
          </p>
        </div>

      </div>

      {/* Products */}
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">

        {recommendations.map((product, index) => {

          const score = Number(product.score || 0);

          const percentage = Math.min(
            score * 100,
            100
          );

          const isHybrid =
            product.reason?.toLowerCase().includes("collaborative");

          return (
            <div
              key={product.article_id}
              className="group overflow-hidden rounded-2xl border border-white/[0.06] bg-white/[0.02] transition-all duration-200 hover:-translate-y-1 hover:border-white/[0.14] hover:bg-white/[0.04]"
            >

              {/* Product visual */}
              <div className="relative flex h-40 items-center justify-center bg-gradient-to-br from-slate-800 via-slate-900 to-black">

                <div className="text-center">
                  <p className="text-xs uppercase tracking-[0.2em] text-slate-500">
                    {product.product_type || "Product"}
                  </p>

                  <p className="mt-2 text-sm font-medium text-slate-400">
                    {product.colour}
                  </p>
                </div>

                {/* Rank */}
                <div className="absolute left-3 top-3 rounded-full bg-black/40 px-2.5 py-1 text-xs font-semibold text-white backdrop-blur">
                  #{index + 1}
                </div>

              </div>

              {/* Content */}
              <div className="p-4">

                <div className="mb-2">
                  <h3 className="font-semibold text-white">
                    {product.product_name}
                  </h3>

                  <p className="mt-1 text-xs text-slate-500">
                    {product.product_type}
                    {" • "}
                    {product.colour}
                  </p>
                </div>

                <p className="mb-4 line-clamp-3 text-sm leading-relaxed text-slate-400">
                  {product.description}
                </p>

                {/* Recommendation reason */}
                <div className="mb-4 rounded-xl border border-white/[0.06] bg-black/20 p-3">

                  <div className="mb-1 flex items-center gap-2">

                    {isHybrid ? (
                      <Users
                        size={14}
                        className="text-blue-400"
                      />
                    ) : (
                      <Brain
                        size={14}
                        className="text-purple-400"
                      />
                    )}

                    <span className="text-xs font-semibold text-slate-200">
                      {product.reason || "Recommended for you"}
                    </span>

                  </div>

                  <p className="text-xs leading-relaxed text-slate-500">
                    {isHybrid
                      ? "Matches your behavior patterns and product preferences."
                      : "Matches your product preferences and item characteristics."}
                  </p>

                </div>

                {/* Scores */}
                <div className="border-t border-white/[0.06] pt-3">

                  <div className="mb-2 flex items-center justify-between">

                    <span className="text-[11px] uppercase tracking-wide text-slate-500">
                      Recommendation Score
                    </span>

                    <span className="text-sm font-semibold text-white">
                      {percentage.toFixed(1)}%
                    </span>

                  </div>

                  {/* Score bar */}
                  <div className="mb-4 h-1.5 overflow-hidden rounded-full bg-white/[0.06]">

                    <div
                      className="h-full rounded-full bg-gradient-to-r from-blue-500 to-indigo-500 transition-all"
                      style={{
                        width: `${percentage}%`,
                      }}
                    />

                  </div>

                  {/* Model signals */}
                  <div className="grid grid-cols-2 gap-3">

                    <div>
                      <p className="text-[10px] uppercase tracking-wide text-slate-500">
                        Collaborative
                      </p>

                      <p className="mt-1 text-sm font-medium text-slate-300">
                        {Number(
                          product.collaborative_score || 0
                        ).toFixed(2)}
                      </p>
                    </div>

                    <div>
                      <p className="text-[10px] uppercase tracking-wide text-slate-500">
                        Content
                      </p>

                      <p className="mt-1 text-sm font-medium text-slate-300">
                        {Number(
                          product.content_score || 0
                        ).toFixed(2)}
                      </p>
                    </div>

                  </div>

                </div>
              </div>
            </div>
          );
        })}

      </div>

      {recommendations.length === 0 && (
        <div className="py-10 text-center">
          <p className="text-sm text-slate-400">
            No recommendations available.
          </p>
        </div>
      )}

    </section>
  );
}