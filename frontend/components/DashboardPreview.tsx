export default function DashboardPreview() {
  return (
    <section id="dashboard" className="mx-auto max-w-7xl px-6 py-28">
      <div className="mb-12 text-center">
        <p className="text-sm uppercase tracking-[0.3em] text-blue-400">
          Live Dashboard
        </p>

        <h2 className="mt-4 text-4xl font-semibold">
          A smarter way to manage finance operations.
        </h2>

        <p className="mx-auto mt-5 max-w-2xl text-gray-400">
          FinlyAI gives finance teams a clear overview of inventory,
          purchase orders, cash flow, and AI-powered recommendations.
        </p>
      </div>

      <div className="rounded-3xl border border-white/10 bg-white/5 p-8 backdrop-blur-xl">

        <div className="grid gap-6 md:grid-cols-4">

          <div className="rounded-2xl bg-black/30 p-5">
            <p className="text-gray-400 text-sm">Inventory Health</p>
            <h3 className="mt-2 text-3xl font-bold">92%</h3>
            <p className="mt-2 text-green-400 text-sm">Operational</p>
          </div>

          <div className="rounded-2xl bg-black/30 p-5">
            <p className="text-gray-400 text-sm">Purchase Orders</p>
            <h3 className="mt-2 text-3xl font-bold">12</h3>
            <p className="mt-2 text-blue-400 text-sm">Generated Today</p>
          </div>

          <div className="rounded-2xl bg-black/30 p-5">
            <p className="text-gray-400 text-sm">Cash Position</p>
            <h3 className="mt-2 text-3xl font-bold">Healthy</h3>
            <p className="mt-2 text-green-400 text-sm">₹4.8L Available</p>
          </div>

          <div className="rounded-2xl bg-black/30 p-5">
            <p className="text-gray-400 text-sm">AI Confidence</p>
            <h3 className="mt-2 text-3xl font-bold">98%</h3>
            <p className="mt-2 text-purple-400 text-sm">Gemini AI</p>
          </div>

        </div>

        <div className="mt-10 rounded-2xl bg-black/30 p-6">

          <h3 className="text-xl font-semibold">
            AI Recommendation
          </h3>

          <p className="mt-4 text-gray-400">
            Inventory for SKU-102 has dropped below the safety threshold.
            Generate a purchase order of 50 units. Cash flow remains healthy,
            making this an ideal time to replenish stock.
          </p>

        </div>

      </div>
    </section>
  );
}