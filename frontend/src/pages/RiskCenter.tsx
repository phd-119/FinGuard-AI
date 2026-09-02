import React, { useState, useEffect } from 'react';
import { AlertTriangle, ShieldCheck, ShieldAlert, TrendingUp, Activity, ArrowRight, Bot } from 'lucide-react';
import { api } from '../services/api';
import { StatusBadge } from '../components/StatusBadge';
import { MetricCard } from '../components/MetricCard';

interface RiskCenterProps {
  onSelectAction: (actionId: string) => void;
}

export const RiskCenter: React.FC<RiskCenterProps> = ({ onSelectAction }) => {
  const [riskData, setRiskData] = useState<any>(null);
  const [agents, setAgents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadRiskData();
  }, []);

  const loadRiskData = async () => {
    try {
      setLoading(true);
      const [riskRes, agentsRes] = await Promise.all([
        api.getRiskOverview(),
        api.getAgents()
      ]);
      setRiskData(riskRes);
      setAgents(agentsRes);
    } catch (err) {
      console.error('Failed loading risk data:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatINR = (val: number) => `₹${val.toLocaleString('en-IN')}`;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <div className="flex items-center space-x-2">
          <ShieldAlert className="w-5 h-5 text-rose-400" />
          <h1 className="text-xl font-bold text-white font-mono">
            Risk & Trust Analytics Center
          </h1>
          <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 font-mono font-bold">
            ML REGRESSION ACTIVE
          </span>
        </div>
        <p className="text-xs text-slate-300 mt-1">
          Multi-factor continuous risk scoring (0-100), reserve breach probability forecasting, and autonomous agent trust telemetry
        </p>
      </div>

      {/* Top Risk Metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          title="Average Risk Score"
          value={`${riskData?.average_risk_score ?? 42.5}/100`}
          subtitle="Fleet-wide proposal risk"
          icon={Activity}
          variant="blue"
        />
        <MetricCard
          title="High / Critical Risk"
          value={riskData?.high_critical_count ?? 0}
          subtitle="Proposals under dual control"
          icon={AlertTriangle}
          variant={riskData?.high_critical_count > 0 ? 'rose' : 'default'}
        />
        <MetricCard
          title="Medium Risk Actions"
          value={riskData?.medium_count ?? 0}
          subtitle="Monitored within envelope"
          icon={TrendingUp}
          variant="amber"
        />
        <MetricCard
          title="Protected Actions"
          value={riskData?.low_count ?? 0}
          subtitle="Safe autonomous execution"
          icon={ShieldCheck}
          variant="emerald"
        />
      </div>

      {/* Agent Risk & Trust Telemetry */}
      <div className="rounded-2xl bg-bg-card border border-bg-border p-6 space-y-4">
        <div className="flex items-center space-x-2">
          <Bot className="w-4 h-4 text-brand-blue" />
          <h2 className="text-sm font-bold text-white font-mono uppercase tracking-wider">
            Agent Risk Exposure & Reputation Telemetry
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {agents.map((ag) => (
            <div
              key={ag.id}
              className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-3"
            >
              <div className="flex items-center justify-between">
                <span className="font-bold text-white font-mono text-xs">{ag.name}</span>
                <StatusBadge type="trust" value={ag.trust_level} />
              </div>

              <div className="space-y-1 font-mono text-xs">
                <div className="flex justify-between text-slate-400 text-[11px]">
                  <span>Trust Score</span>
                  <span className="text-emerald-400 font-bold">{ag.trust_score.toFixed(1)}/100</span>
                </div>
                <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                  <div
                    className="bg-gradient-to-r from-brand-blue to-emerald-400 h-1.5 rounded-full"
                    style={{ width: `${Math.min(100, ag.trust_score)}%` }}
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-2 text-[11px] font-mono text-slate-400 pt-1 border-t border-slate-800/80">
                <div>
                  <span className="text-slate-500 text-[10px] block">Proposals</span>
                  <span className="text-white font-bold">{ag.total_proposals}</span>
                </div>
                <div>
                  <span className="text-slate-500 text-[10px] block">Violations</span>
                  <span className={ag.violation_count > 0 ? 'text-rose-400 font-bold' : 'text-emerald-400 font-bold'}>
                    {ag.violation_count}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Recent Evaluated Proposals Risk Log */}
      <div className="rounded-2xl bg-bg-card border border-bg-border overflow-hidden">
        <div className="p-5 border-b border-slate-800 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <ShieldAlert className="w-4 h-4 text-rose-400" />
            <h2 className="text-sm font-bold text-white font-mono uppercase tracking-wider">
              Recent Multi-Factor Risk Assessments
            </h2>
          </div>
          <span className="text-xs text-slate-400 font-mono">
            Gradient Boosting Continuous Scorer
          </span>
        </div>

        <div className="divide-y divide-slate-800/60 font-mono text-xs">
          {riskData?.recent_assessments?.length === 0 ? (
            <div className="p-8 text-center text-slate-500">
              No recent risk assessments logged. Run the Hero Demo or propose an action.
            </div>
          ) : (
            riskData?.recent_assessments?.map((item: any, idx: number) => (
              <div
                key={idx}
                onClick={() => onSelectAction(item.proposal_id)}
                className="p-4 hover:bg-slate-800/40 cursor-pointer transition flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3"
              >
                <div className="space-y-1 max-w-2xl">
                  <div className="flex items-center space-x-2">
                    <span className="font-bold text-white">{item.agent_name}</span>
                    <span className="text-slate-600">•</span>
                    <span className="text-emerald-400 font-bold">{formatINR(item.amount)}</span>
                    <StatusBadge type="risk" value={item.risk_level} />
                  </div>
                  <p className="text-xs text-slate-300 font-sans">{item.explanation}</p>
                </div>

                <div className="flex items-center space-x-3 self-end sm:self-auto">
                  <span className={`text-base font-extrabold ${
                    item.risk_score >= 70 ? 'text-rose-400' : item.risk_score >= 40 ? 'text-amber-400' : 'text-emerald-400'
                  }`}>
                    {item.risk_score.toFixed(1)}/100
                  </span>
                  <button className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition">
                    <ArrowRight className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};
