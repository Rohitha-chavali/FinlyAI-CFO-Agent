const features = [
  {
    title: "Smart Inventory Monitoring",
    description:
      "Continuously tracks stock levels and instantly detects items that fall below safety thresholds.",
  },
  {
    title: "Automated Purchase Orders",
    description:
      "Generates purchase orders automatically and prepares vendor-ready documents in seconds.",
  },
  {
    title: "AI Financial Advisor",
    description:
      "Uses Gemini AI to analyze cash flow and recommend whether purchases should be approved.",
  },
];

export default function Features() {
  return (
    <section id="features" className="mx-auto max-w-7xl px-6 py-28">
      <div className="mb-16 text-center">
        <p className="text-sm uppercase tracking-[0.3em] text-blue-400">
          Features
        </p>

        <h2 className="mt-4 text-4xl font-semibold">
          Everything your finance team needs.
        </h2>

        <p className="mx-auto mt-5 max-w-2xl text-gray-400">
          FinlyAI combines inventory tracking, automated procurement,
          and AI-driven financial intelligence into one unified platform.
        </p>
      </div>

      <div className="grid gap-8 md:grid-cols-3">
        {features.map((feature) => (
          <div
            key={feature.title}
            className="rounded-3xl border border-white/10 bg-white/5 p-8 backdrop-blur-xl transition duration-300 hover:border-blue-500/30 hover:bg-white/10"
          >
            <h3 className="text-2xl font-semibold">
              {feature.title}
            </h3>

            <p className="mt-4 leading-7 text-gray-400">
              {feature.description}
            </p>
          </div>
        ))}
      </div>
    </section>
  );
}