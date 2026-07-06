import Link from "next/link";

export default function Dashboard() {
  return (
    <main className="min-h-screen bg-[#050816] text-white">

      <nav className="border-b border-white/10 bg-black/40 backdrop-blur-xl">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-8 py-5">

          <Link
            href="/"
            className="flex items-center gap-3"
          >
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-blue-500 to-purple-500 font-bold">
              F
            </div>

            <span className="text-xl font-semibold">
              FinlyAI
            </span>
          </Link>

          <Link
            href="/"
            className="rounded-xl border border-white/10 px-5 py-2 hover:bg-white/5"
          >
            ← Back Home
          </Link>

        </div>
      </nav>

      <div className="mx-auto max-w-7xl px-8 py-10">

        <h1 className="text-5xl font-bold">
          Dashboard
        </h1>

        <p className="mt-3 text-gray-400">
          AI-powered financial operations overview.
        </p>

        <div className="mt-12 grid gap-6 md:grid-cols-4">

          <div className="rounded-3xl border border-white/10 bg-white/5 p-6">
            <p className="text-gray-400">Inventory Health</p>
            <h2 className="mt-3 text-4xl font-bold">92%</h2>
          </div>

          <div className="rounded-3xl border border-white/10 bg-white/5 p-6">
            <p className="text-gray-400">Low Stock Alerts</p>
            <h2 className="mt-3 text-4xl font-bold">4</h2>
          </div>

          <div className="rounded-3xl border border-white/10 bg-white/5 p-6">
            <p className="text-gray-400">Purchase Orders</p>
            <h2 className="mt-3 text-4xl font-bold">12</h2>
          </div>

          <div className="rounded-3xl border border-white/10 bg-white/5 p-6">
            <p className="text-gray-400">Cash Position</p>
            <h2 className="mt-3 text-3xl font-bold text-green-400">
              Healthy
            </h2>
          </div>

        </div>

        <div className="mt-8 grid gap-6 md:grid-cols-2">

          <div className="rounded-3xl border border-white/10 bg-white/5 p-8">

            <h2 className="text-2xl font-semibold">
              AI Recommendation
            </h2>

            <p className="mt-5 leading-8 text-gray-400">
              Inventory for SKU-102 has dropped below the safety threshold.
              Generate a purchase order for 50 units.
              Current cash flow comfortably supports the purchase.
            </p>

          </div>

          <div className="rounded-3xl border border-white/10 bg-white/5 p-8">

            <h2 className="text-2xl font-semibold">
              Recent Activity
            </h2>

            <ul className="mt-5 space-y-4 text-gray-300">
              <li>✓ Inventory scan completed</li>
              <li>✓ Purchase Order #1024 generated</li>
              <li>✓ Gemini AI financial analysis completed</li>
              <li>✓ Audit log updated</li>
            </ul>

          </div>

        </div>

      </div>

    </main>
  );
}