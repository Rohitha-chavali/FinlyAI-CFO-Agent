import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="fixed top-0 left-0 z-50 w-full border-b border-white/10 bg-black/40 backdrop-blur-xl">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-8 py-5">

        {/* Logo */}
        <Link
          href="/"
          className="flex items-center gap-3 transition hover:opacity-90"
        >
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-blue-500 to-purple-500 font-bold text-white">
            F
          </div>

          <span className="text-xl font-semibold tracking-tight">
            FinlyAI
          </span>
        </Link>

        {/* Navigation */}
        <div className="hidden md:flex items-center gap-8 text-sm text-gray-300">

          <a href="/#features" className="transition hover:text-white">
            Features
          </a>

          <Link
            href="/dashboard"
            className="transition hover:text-white"
          >
            Dashboard
          </Link>

          <a href="/#architecture" className="transition hover:text-white">
            Architecture
          </a>

        </div>

      </div>
    </nav>
  );
}