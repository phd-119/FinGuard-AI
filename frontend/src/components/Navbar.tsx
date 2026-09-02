import React from 'react';
import {
  ShieldCheck,
  Bot,
  Activity,
  GitFork,
  ShieldAlert,
  SlidersHorizontal,
  CheckCircle2,
  FileText,
  Play,
  RotateCcw,
  PlusCircle
} from 'lucide-react';

interface NavbarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  onOpenProposeModal: () => void;
  onResetState: () => void;
  pendingApprovalsCount: number;
}

export const Navbar: React.FC<NavbarProps> = ({
  activeTab,
  setActiveTab,
  onOpenProposeModal,
  onResetState,
  pendingApprovalsCount
}) => {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: Activity },
    { id: 'hero-demo', label: 'Hero Demo', icon: Play, highlight: true },
    { id: 'agents', label: 'Autonomous Agents', icon: Bot },
    { id: 'actions', label: 'Live Actions Gateway', icon: Activity },
    { id: 'conflicts', label: 'Conflict Center', icon: GitFork },
    { id: 'risk', label: 'Risk Center', icon: ShieldAlert },
    { id: 'simulations', label: 'What-If Simulations', icon: SlidersHorizontal },
    {
      id: 'approvals',
      label: 'Approval Center',
      icon: CheckCircle2,
      badge: pendingApprovalsCount > 0 ? pendingApprovalsCount : undefined
    },
    { id: 'audit', label: 'Audit Trail', icon: FileText }
  ];

  return (
    <header className="sticky top-0 z-40 w-full border-b border-slate-800/80 bg-[#070B14]/90 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Status Badge */}
          <div className="flex items-center space-x-4">
            <div
              onClick={() => setActiveTab('dashboard')}
              className="flex items-center space-x-3 cursor-pointer group"
            >
              <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-blue to-emerald-400 p-0.5 shadow-lg shadow-emerald-500/20 group-hover:scale-105 transition-transform">
                <div className="w-full h-full bg-[#070B14] rounded-[10px] flex items-center justify-center">
                  <ShieldCheck className="w-5 h-5 text-emerald-400" />
                </div>
              </div>
              <div>
                <div className="flex items-center space-x-2">
                  <span className="text-lg font-extrabold tracking-tight text-white font-mono">
                    FIN<span className="text-emerald-400">GUARD</span>.AI
                  </span>
                  <span className="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 font-mono font-semibold">
                    CONTROL PLANE
                  </span>
                </div>
                <p className="text-[10px] text-slate-400 hidden sm:block">
                  Financial Governance for Autonomous AI Agents
                </p>
              </div>
            </div>

            {/* Live System State Badge */}
            <div className="hidden lg:flex items-center space-x-2 pl-4 border-l border-slate-800">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
              </span>
              <span className="text-xs font-mono font-medium text-slate-300">
                SYSTEM: <span className="text-emerald-400 font-bold">PROTECTED</span>
              </span>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex items-center space-x-3">
            <button
              onClick={onResetState}
              title="Reset sandbox state to pristine ₹6L cash & ₹5L reserve"
              className="p-2 text-slate-400 hover:text-white rounded-lg bg-slate-800/60 hover:bg-slate-800 border border-slate-700 transition flex items-center space-x-1.5 text-xs font-mono"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">Reset Sandbox</span>
            </button>

            <button
              onClick={onOpenProposeModal}
              className="px-3 py-2 text-xs font-semibold font-mono rounded-lg bg-gradient-to-r from-brand-blue to-emerald-500 hover:from-blue-600 hover:to-emerald-600 text-white shadow-lg shadow-blue-500/20 transition flex items-center space-x-1.5"
            >
              <PlusCircle className="w-3.5 h-3.5" />
              <span>Propose Action</span>
            </button>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="flex space-x-1 overflow-x-auto py-2.5 scrollbar-none border-t border-slate-800/40">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`flex items-center space-x-2 px-3.5 py-1.5 rounded-lg text-xs font-medium font-mono whitespace-nowrap transition-all ${
                  isActive
                    ? item.highlight
                      ? 'bg-gradient-to-r from-emerald-500/20 to-brand-blue/20 text-emerald-400 border border-emerald-500/40 shadow-sm'
                      : 'bg-slate-800 text-white border border-slate-700'
                    : item.highlight
                    ? 'text-emerald-400 hover:bg-emerald-500/10 border border-emerald-500/20'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50 border border-transparent'
                }`}
              >
                <Icon className={`w-3.5 h-3.5 ${isActive ? 'text-emerald-400' : ''}`} />
                <span>{item.label}</span>
                {item.badge !== undefined && (
                  <span className="px-1.5 py-0.2 rounded-full text-[10px] font-bold bg-rose-500 text-white">
                    {item.badge}
                  </span>
                )}
              </button>
            );
          })}
        </nav>
      </div>
    </header>
  );
};
