import Navbar from "@/components/Navbar";
import Hero from "@/components/Hero";
import Features from "@/components/Features";
import Architecture from "@/components/Architecture";

export default function Home() {
  return (
    <>
      <Navbar />
      <Hero />

      <section id="features">
        <Features />
      </section>

      <section id="architecture">
        <Architecture />
      </section>
    </>
  );
}