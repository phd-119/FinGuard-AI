import React from 'react';
import { Play, Sparkles, AlertCircle, ArrowRight } from 'lucide-react';

interface HeroDemoBannerProps {
  onRunHeroDemo: () => void;
  onNavigateToHero: () => void;
  isRunning?: boolean;
}

export const HeroDemoBanner: React.FC<HeroDemoBannerProps> = ({
  onRunHeroDemo,
  onNavigateToHero,
  isRunning = false
}) => {
  return (
    <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-blue-950/60 via-slate-900 to-emerald-950/60 border border-emerald-500/30 p-6 glow-emerald">
      <div className="absolute top-0 right-0 -mr-16 -mt-16 w-64 h-64 rounded-full bg-emerald-500/10 blur-3xl pointer-events-none" />
      <div className="absolute bottom-0 left-0 -ml-16 -mb-16 w-64 h-64 rounded-full bg-blue-500/10 blur-3xl pointer-events-none" />

      <div className="relative z-10 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div className="space-y-1.5 max-w-2xl">
          <div className="flex items-center space-x-2">
            <span className="px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
              FLAGSHIP INTERNSHIP SHOWCASE
            </span>
            <span className="text-xs text-slate-400 font-mono">
              Razorpay AI Builder Buildathon 2026
            </span>
          </div>
          <h2 className="text-lg sm:text-xl font-extrabold text-white font-mono tracking-tight">
            Global Multi-Agent Financial Conflict Demo
          </h2>
          <p className="text-xs sm:text-sm text-slate-300">
            Demonstrates why evaluating AI agents in isolation causes liquidity failure: 
            <strong className="text-white"> Payout (₹4L) + Growth (₹2L) + Refund (₹1L) = ₹7L Outflow</strong> vs 
            <strong className="text-emerald-400"> ₹6L Cash & ₹5L Reserve</strong>. 
            FinGuard detects the global conflict and safely modifies execution.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-3 w-full md:w-auto">
          <button
            onClick={onRunHeroDemo}
            disabled={isRunning}
            className="flex-1 md:flex-initial px-5 py-2.5 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-400 hover:from-emerald-400 hover:to-teal-300 text-slate-950 font-bold font-mono text-xs shadow-lg shadow-emerald-500/25 transition-all flex items-center justify-center space-x-2 disabled:opacity-50"
          >
            <Play className={`w-4 h-4 ${isRunning ? 'animate-spin' : 'fill-slate-950'}`} />
            <span>{isRunning ? 'Governing Hero Scenario...' : 'Run FinGuard Demo'}</span>
          </button>

          <button
            onClick={onNavigateToHero}
            className="px-4 py-2.5 rounded-xl bg-slate-800/80 hover:bg-slate-800 text-slate-200 border border-slate-700 hover:border-slate-600 font-mono text-xs transition flex items-center space-x-1.5"
          >
            <span>Interactive Walkthrough</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
    </div>
  );
};
