export default function Hero() {
  return (
    <section id="hero" className="relative flex min-h-screen flex-col items-center justify-center px-6 pt-32 text-center">

      {/* Background Glow */}
      <div className="absolute inset-0 -z-10 bg-[radial-gradient(circle_at_top,rgba(59,130,246,0.18),transparent_40%),radial-gradient(circle_at_bottom_right,rgba(168,85,247,0.18),transparent_35%)]" />

      {/* Badge */}
      <div className="mb-6 rounded-full border border-blue-500/30 bg-blue-500/10 px-5 py-2 text-sm text-blue-300 backdrop-blur-md">
        ✨ Powered by Gemini AI • Real-Time Financial Automation
      </div>

      {/* Heading */}
      <h1 className="max-w-4xl text-5xl font-semibold tracking-tight md:text-7xl">
        Finance Operations,
        <span className="block bg-gradient-to-r from-blue-400 via-cyan-300 to-purple-400 bg-clip-text text-transparent">
          Reimagined with AI
        </span>
      </h1>

      {/* Description */}
      <p className="mt-8 max-w-2xl text-lg leading-8 text-gray-400">
        FinlyAI intelligently monitors inventory, automates purchase orders,
        generates financial reports, and provides AI-powered CFO
        recommendations—all from one intelligent platform.
      </p>

      {/* Buttons */}
      <div className="mt-12 mb-20 flex flex-wrap justify-center gap-5">

        <a
          href="/dashboard"
          className="rounded-xl bg-blue-600 px-8 py-4 text-lg font-semibold transition-all duration-300 hover:bg-blue-500 hover:scale-105"
        >
          View Dashboard
        </a>

        <a
          href="#features"
          className="rounded-xl border border-white/20 px-8 py-4 text-lg text-white transition-all duration-300 hover:border-blue-400 hover:bg-white/5 hover:scale-105"
        >
          Explore Features
        </a>

      </div>

    </section>
  );
}