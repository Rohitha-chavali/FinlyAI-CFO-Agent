export default function Architecture() {
  return (
    <section
      id="architecture"
      className="mx-auto max-w-7xl px-6 py-28"
    >
      <div className="text-center">

        <p className="text-sm uppercase tracking-[0.3em] text-blue-400">
          Architecture
        </p>

        <h2 className="mt-4 text-4xl font-semibold">
          How FinlyAI Works
        </h2>

      </div>

      <div className="mt-20 grid gap-6 md:grid-cols-5">

        <div className="rounded-3xl border border-white/10 bg-white/5 p-6 text-center">
          <h3 className="font-semibold">Inventory</h3>
          <p className="mt-3 text-gray-400 text-sm">
            Reads CSV inventory data.
          </p>
        </div>

        <div className="flex items-center justify-center text-3xl text-blue-400">
          →
        </div>

        <div className="rounded-3xl border border-white/10 bg-white/5 p-6 text-center">
          <h3 className="font-semibold">Billing</h3>
          <p className="mt-3 text-gray-400 text-sm">
            Generates Purchase Orders.
          </p>
        </div>

        <div className="flex items-center justify-center text-3xl text-blue-400">
          →
        </div>

        <div className="rounded-3xl border border-white/10 bg-white/5 p-6 text-center">
          <h3 className="font-semibold">Gemini AI</h3>
          <p className="mt-3 text-gray-400 text-sm">
            Provides financial recommendations.
          </p>
        </div>

      </div>
    </section>
  );
}