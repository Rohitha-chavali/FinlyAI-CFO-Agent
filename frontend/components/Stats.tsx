const stats = [
  {
    title: "Inventory Health",
    value: "92%",
    icon: "📦",
  },
  {
    title: "Purchase Orders",
    value: "12",
    icon: "📄",
  },
  {
    title: "Cash Position",
    value: "Healthy",
    icon: "💰",
  },
  {
    title: "AI Confidence",
    value: "98%",
    icon: "🤖",
  },
];

export default function Stats() {
  return (
    <section className="mx-auto -mt-20 grid max-w-6xl gap-6 px-6 pb-24 md:grid-cols-4">
      {stats.map((item) => (
        <div
          key={item.title}
          className="rounded-3xl border border-white/10 bg-white/5 p-6 backdrop-blur-xl transition-all duration-300 hover:-translate-y-2 hover:border-blue-500/30"
        >
          <p className="text-3xl">{item.icon}</p>

          <h3 className="mt-4 text-lg font-semibold">
            {item.title}
          </h3>

          <p className="mt-2 text-3xl font-bold">
            {item.value}
          </p>
        </div>
      ))}
    </section>
  );
}