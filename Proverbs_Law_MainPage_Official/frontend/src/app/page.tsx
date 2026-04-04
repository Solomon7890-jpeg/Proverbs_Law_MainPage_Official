"use client";

import Image from "next/image";
import { useState, useEffect } from "react";
import Hero3D from "@/components/Hero3D";

const logos = ["/logo_1.jpg", "/logo_2.jpg", "/logo_3.jpg"];

const modules = [
  {
    icon: "🤖",
    title: "AI Legal Chatbot",
    description:
      "7 specialized AI modes — Navigation, General Legal, Document Validation, Legal Research, Etymology, Case Management, and Regulatory Updates.",
    status: "live" as const,
    href: "#",
  },
  {
    icon: "📄",
    title: "Document Scanner & Analysis",
    description:
      "Upload and analyze legal documents with OCR text extraction, multi-format support (PDF, DOCX, TXT), and AI-powered insights.",
    status: "coming" as const,
    href: "#",
  },
  {
    icon: "⚖️",
    title: "Legal Action Advisor",
    description:
      "Get personalized recommendations for seeking justice — case type analysis, timeline planning, evidence collection guidance.",
    status: "coming" as const,
    href: "#",
  },
  {
    icon: "🔍",
    title: "Legal Research Tools",
    description:
      "Access comprehensive legal databases, case law research, statutory analysis, historical documents, and citation tools.",
    status: "coming" as const,
    href: "#",
  },
  {
    icon: "💼",
    title: "Case Management",
    description:
      "Organize case information, track deadlines and milestones, manage documents and evidence, coordinate case activities.",
    status: "coming" as const,
    href: "#",
  },
  {
    icon: "📝",
    title: "Document Generation",
    description:
      "Create legal documents with AI — contracts, agreements, letters, and more with professional templates.",
    status: "coming" as const,
    href: "#",
  },
  {
    icon: "📧",
    title: "Communications Hub",
    description:
      "Integrated communication system — Twilio SMS messaging, email notifications, phone capabilities, legal alerts.",
    status: "coming" as const,
    href: "#",
  },
  {
    icon: "🎙️",
    title: "Voice & Audio Processing",
    description:
      "Text-to-speech with voice cloning, audio transcription, voice analysis powered by Supertonic Voice Module.",
    status: "coming" as const,
    href: "#",
  },
];

export default function Home() {
  const [currentLogo, setCurrentLogo] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentLogo((prev) => (prev + 1) % logos.length);
    }, 6000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-zinc-950 text-white">
      {/* Hero Section with 3D Immersive Brain */}
      <header className="relative min-h-[70vh] overflow-hidden flex items-center justify-center border-b border-zinc-800">
        <Hero3D />
        
        {/* Overlay Gradients for Depth */}
        <div className="absolute inset-0 bg-gradient-to-t from-zinc-950 via-transparent to-zinc-950/50 pointer-events-none" />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(30,58,138,0.2),transparent_70%)] pointer-events-none" />

        <div className="relative z-10 mx-auto max-w-5xl px-6 py-20 text-center">
          {/* Rotating Logo with Glassmorphism */}
          <div className="mb-10 flex justify-center">
            <div className="relative h-44 w-44 overflow-hidden rounded-full border-4 border-[#eab308] shadow-[0_0_80px_rgba(234,179,8,0.2)] bg-zinc-900/40 backdrop-blur-sm">
              {logos.map((logo, i) => (
                <Image
                  key={logo}
                  src={logo}
                  alt={`ProVerBs Logo ${i + 1}`}
                  fill
                  className={`object-cover transition-opacity duration-1500 ease-in-out ${
                    i === currentLogo ? "opacity-100 scale-105" : "opacity-0 scale-100"
                  }`}
                  style={{ transition: 'opacity 1.5s ease-in-out, transform 1.5s ease-in-out' }}
                  priority={i === 0}
                />
              ))}
            </div>
          </div>

          <h1 className="mb-6 text-5xl font-extrabold tracking-tight sm:text-6xl lg:text-7xl bg-clip-text text-transparent bg-gradient-to-b from-white to-zinc-400">
            ⚖️ ProVerBs Corporate
          </h1>
          <p className="mb-4 text-xl font-medium tracking-wide text-[#eab308] uppercase">
            Lawful vs. Legal: Dual Analysis &ldquo;Adappt&apos;plication&rdquo;
          </p>
          <p className="mx-auto max-w-2xl text-lg text-zinc-400 leading-relaxed">
            Ultimate Brain Rendering Level &bull; 100+ Reasoning Protocols &bull;
            Autonomous Intelligence Evolution &bull; Industry Global Pro Set Up
          </p>

          <div className="mt-8 flex flex-wrap justify-center gap-4">
            <a
              href="#modules"
              className="rounded-full bg-[#9C8E7D] px-8 py-3 font-semibold text-zinc-950 transition hover:bg-[#b0a393]"
            >
              Explore Modules
            </a>
            <a
              href="https://huggingface.co/Solomon7890"
              target="_blank"
              rel="noopener noreferrer"
              className="rounded-full border border-[#9C8E7D]/30 px-8 py-3 font-semibold text-[#9C8E7D] transition hover:border-[#9C8E7D] hover:bg-[#9C8E7D]/10"
            >
              Hugging Face &rarr;
            </a>
          </div>
        </div>
      </header>

      {/* Stats Bar */}
      <section className="border-y border-zinc-800 bg-zinc-900/50">
        <div className="mx-auto flex max-w-5xl flex-wrap justify-center gap-8 px-6 py-6 text-center sm:gap-16">
          {[
            ["100+", "Reasoning Protocols"],
            ["6", "AI Models"],
            ["7", "Legal Modes"],
            ["8", "Module Spaces"],
          ].map(([num, label]) => (
            <div key={label}>
              <div className="text-2xl font-bold text-[#9C8E7D]">{num}</div>
              <div className="text-sm text-zinc-400">{label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* Module Cards */}
      <section id="modules" className="mx-auto max-w-5xl px-6 py-16">
        <h2 className="mb-2 text-center text-3xl font-bold">
          Platform Modules
        </h2>
        <p className="mb-12 text-center text-zinc-400">
          Each module is deployed as its own application &mdash; click to launch
        </p>

        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {modules.map((mod) => (
            <a
              key={mod.title}
              href={mod.href}
              className="group relative rounded-2xl border border-zinc-800 bg-zinc-900/60 p-6 transition-all hover:-translate-y-1 hover:border-[#9C8E7D]/50 hover:shadow-[0_12px_32px_rgba(38,38,38,0.3)]"
            >
              <span
                className={`absolute right-4 top-4 rounded-full px-2 py-0.5 text-xs font-medium ${
                  mod.status === "live"
                    ? "bg-green-900/50 text-green-400"
                    : "bg-zinc-800 text-zinc-500"
                }`}
              >
                {mod.status === "live" ? "Live" : "Coming Soon"}
              </span>

              <div className="mb-3 text-3xl">{mod.icon}</div>
              <h3 className="mb-2 text-lg font-semibold group-hover:text-[#9C8E7D]">
                {mod.title}
              </h3>
              <p className="text-sm leading-relaxed text-zinc-400">
                {mod.description}
              </p>
            </a>
          ))}
        </div>
      </section>

      {/* About Section */}
      <section className="border-t border-zinc-800 bg-zinc-900/30">
        <div className="mx-auto max-w-3xl px-6 py-16 text-center">
          <h2 className="mb-4 text-2xl font-bold">
            Powered by Pro&apos;VerBs™ &amp; ADAPPT-I™ Technology
          </h2>
          <p className="mb-6 text-zinc-400">
            ProVerBs Legal AI combines advanced artificial intelligence with
            comprehensive legal knowledge to provide accessible, accurate legal
            information and tools for professionals, students, businesses, and
            individuals.
          </p>
          <div className="flex flex-wrap justify-center gap-3 text-sm text-zinc-500">
            {[
              "Chain-of-Thought",
              "Self-Consistency",
              "Tree-of-Thoughts",
              "ReAct",
              "Reflexion",
              "RAG",
              "Quantum Reasoning",
              "Multi-Agent Systems",
            ].map((protocol) => (
              <span
                key={protocol}
                className="rounded-full border border-zinc-800 px-3 py-1"
              >
                {protocol}
              </span>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-zinc-800 py-8 text-center text-sm text-zinc-500">
        <p className="mb-2">
          <strong className="text-zinc-400">
            ⚖️ ProVerBs Legal AI Platform
          </strong>{" "}
          | Version 1.0.0
        </p>
        <p className="mb-2">
          <a
            href="https://huggingface.co/Solomon7890"
            className="hover:text-[#9C8E7D]"
          >
            Hugging Face
          </a>{" "}
          &bull;{" "}
          <a
            href="https://github.com/Solomon7890-jpeg"
            className="hover:text-[#9C8E7D]"
          >
            GitHub
          </a>
        </p>
        <p>
          ⚠️ This AI provides general legal information only. Consult with a
          licensed attorney for specific legal matters.
        </p>
        <p className="mt-2 text-zinc-600">
          © 2024 ProVerBs Legal AI. Built by Solomon7890.
        </p>
      </footer>
    </div>
  );
}
