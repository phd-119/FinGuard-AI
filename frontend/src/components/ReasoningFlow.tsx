import React, { useState } from 'react';
import {
  Bot,
  Compass,
  ShieldAlert,
  Wallet,
  GitFork,
  TrendingDown,
  AlertTriangle,
  SlidersHorizontal,
  Lightbulb,
  CheckCircle2,
  Lock,
  FileCheck2,
  ChevronDown,
  ChevronUp,
  Sparkles,
  Clock,
  ArrowRight
} from 'lucide-react';
import { EvaluationPipelineResponse } from '../types';
import { StatusBadge } from './StatusBadge';

interface ReasoningFlowProps {
  data: EvaluationPipelineResponse;
  onOpenAuditModal?: (proposalId: string) => void;
  onApproveProposal?: (proposalId: string, amount: number) => void;
}

export const ReasoningFlow: React.FC<ReasoningFlowProps> = ({
  data,
  onOpenAuditModal,
  onApproveProposal
}) => {
  const [expandedSteps, setExpandedSteps] = useState<Record<number, boolean>>({
    1: true,
    2: true,
    3: true,
    4: true,
    5: true,
    6: true,
    7: true,
    8: true,
    9: true,
    10: true
  });

  const toggleStep = (step: number) => {
    setExpandedSteps((prev) => ({ ...prev, [step]: !prev[step] }));
  };

  const expandAll = () => {
    const all: Record<number, boolean> = {};
    for (let i = 1; i <= 10; i++) all[i] = true;
    setExpandedSteps(all);
  };

  const collapseAll = () => {
    setExpandedSteps({});
  };

  const formatINR = (val: number) => `₹${val.toLocaleString('en-IN')}`;

  return (
    <div className="space-y-4">
      {/* Top Controls Bar */}
      <div className="flex items-center justify-between p-4 rounded-xl bg-bg-card border border-bg-border">
        <div>
          <div className="flex items-center space-x-2">
            <Sparkles className="w-4 h-4 text-emerald-400" />
            <h3 className="text-sm font-bold text-white font-mono uppercase tracking-wider">
              FinGuard 10-Stage Governance Reasoning Chain
            </h3>
          </div>
          <p className="text-xs text-slate-400 mt-0.5">
            Transparent, auditable, and unbypassable financial safety adjudication
          </p>
        </div>
        <div className="flex items-center space-x-2 text-xs font-mono">
          <button
            onClick={expandAll}
            className="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 transition"
          >
            Expand All
          </button>
          <button
            onClick={collapseAll}
            className="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 transition"
          >
            Collapse All
          </button>
        </div>
      </div>

      {/* Stage 1: Proposed Financial Action */}
      <div className="rounded-xl bg-bg-card border border-bg-border overflow-hidden transition">
        <button
          onClick={() => toggleStep(1)}
          className="w-full px-4 py-3.5 flex items-center justify-between bg-slate-900/40 hover:bg-slate-900/80 transition text-left"
        >
          <div className="flex items-center space-x-3">
            <div className="p-2 rounded-lg bg-blue-500/10 text-brand-blue border border-blue-500/20">
              <Bot className="w-4 h-4" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-xs font-mono font-bold text-slate-400">STAGE 01</span>
                <span className="text-sm font-semibold text-white">Proposed Financial Action</span>
                <StatusBadge type="urgency" value={data.intent.urgency} />
              </div>
              <p className="text-xs text-slate-400">
                {data.agent_name} proposes {formatINR(data.original_amount)} for {data.action_type}
              </p>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <span className="text-sm font-bold font-mono text-white">
              {formatINR(data.original_amount)}
            </span>
            {expandedSteps[1] ? <ChevronUp className="w-4 h-4 text-slate-400" /> : <ChevronDown className="w-4 h-4 text-slate-400" />}
          </div>
        </button>

        {expandedSteps[1] && (
          <div className="p-4 border-t border-bg-border bg-bg-subtle/50 space-y-3 text-xs">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              <div className="p-3 rounded-lg bg-bg-card border border-slate-800">
                <span className="text-slate-400 block text-[11px] font-mono">Agent Identity</span>
                <span className="font-semibold text-white font-mono">{data.agent_name} ({data.agent_id})</span>
              </div>
              <div className="p-3 rounded-lg bg-bg-card border border-slate-800">
                <span className="text-slate-400 block text-[11px] font-mono">Action Type</span>
                <span className="font-semibold text-white font-mono">{data.action_type}</span>
              </div>
              <div className="p-3 rounded-lg bg-bg-card border border-slate-800">
                <span className="text-slate-400 block text-[11px] font-mono">Reported Confidence</span>
                <span className="font-semibold text-emerald-400 font-mono">{(data.intent.confidence * 100).toFixed(1)}%</span>
              </div>
            </div>
            <div className="p-3 rounded-lg bg-bg-card border border-slate-800">
              <span className="text-slate-400 block text-[11px] font-mono mb-1">Agent Stated Rationale</span>
              <p className="text-slate-200">{data.intent.explanation}</p>
            </div>
          </div>
        )}
      </div>

      {/* Stage 2: Financial Intent Check */}
      <div className="rounded-xl bg-bg-card border border-bg-border overflow-hidden transition">
        <button
          onClick={() => toggleStep(2)}
          className="w-full px-4 py-3.5 flex items-center justify-between bg-slate-900/40 hover:bg-slate-900/80 transition text-left"
        >
          <div className="flex items-center space-x-3">
            <div className="p-2 rounded-lg bg-cyan-500/10 text-brand-cyan border border-cyan-500/20">
              <Compass className="w-4 h-4" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-xs font-mono font-bold text-slate-400">STAGE 02</span>
                <span className="text-sm font-semibold text-white">Financial Intent Engine (ML)</span>
              </div>
              <p className="text-xs text-slate-400">
                Classified: <span className="text-cyan-300 font-mono">{data.intent.intent_label}</span> — {data.intent.purpose}
              </p>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <span className="text-xs px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 font-mono">
              {(data.intent.confidence * 100).toFixed(1)}% CONFIDENCE
            </span>
            {expandedSteps[2] ? <ChevronUp className="w-4 h-4 text-slate-400" /> : <ChevronDown className="w-4 h-4 text-slate-400" />}
          </div>
        </button>

        {expandedSteps[2] && (
          <div className="p-4 border-t border-bg-border bg-bg-subtle/50 space-y-2 text-xs">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              <div className="p-3 rounded-lg bg-bg-card border border-slate-800">
                <span className="text-slate-400 block text-[11px] font-mono">Intent Purpose</span>
                <span className="text-slate-200 font-medium">{data.intent.purpose}</span>
              </div>
              <div className="p-3 rounded-lg bg-bg-card border border-slate-800">
                <span className="text-slate-400 block text-[11px] font-mono">Financial Effect Vector</span>
                <span className="text-amber-400 font-mono font-semibold">{data.intent.financial_effect}</span>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Stage 3: Policy Compliance Engine */}
      <div className="rounded-xl bg-bg-card border border-bg-border overflow-hidden transition">
        <button
          onClick={() => toggleStep(3)}
          className="w-full px-4 py-3.5 flex items-center justify-between bg-slate-900/40 hover:bg-slate-900/80 transition text-left"
        >
          <div className="flex items-center space-x-3">
            <div className="p-2 rounded-lg bg-purple-500/10 text-brand-purple border border-purple-500/20">
              <ShieldAlert className="w-4 h-4" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-xs font-mono font-bold text-slate-400">STAGE 03</span>
                <span className="text-sm font-semibold text-white">Policy Engine Evaluation</span>
              </div>
              <p className="text-xs text-slate-400">
                {data.policy_checks.filter((p) => p.is_compliant).length} Passed / {data.policy_checks.length} Evaluated
              </p>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            {data.policy_checks.some((p) => !p.is_compliant) ? (
              <span className="text-xs px-2 py-0.5 rounded bg-rose-500/15 text-rose-400 border border-rose-500/30 font-mono font-semibold">
                POLICY WARNING
              </span>
            ) : (
              <span className="text-xs px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 font-mono font-semibold">
                100% COMPLIANT
              </span>
            )}
            {expandedSteps[3] ? <ChevronUp className="w-4 h-4 text-slate-400" /> : <ChevronDown className="w-4 h-4 text-slate-400" />}
          </div>
        </button>

        {expandedSteps[3] && (
          <div className="p-4 border-t border-bg-border bg-bg-subtle/50 space-y-2 text-xs">
            <div className="space-y-2">
              {data.policy_checks.map((pol) => (
                <div
                  key={pol.policy_code}
                  className={`p-3 rounded-lg border flex items-start justify-between ${
                    pol.is_compliant
                      ? 'bg-slate-900/50 border-slate-800'
                      : 'bg-rose-950/20 border-rose-500/30'
                  }`}
                >
                  <div>
                    <div className="flex items-center space-x-2">
                      <span className="font-mono font-bold text-white">{pol.policy_name}</span>
                      <span className="text-[10px] text-slate-400 font-mono">({pol.policy_code})</span>
                    </div>
                    <p className="text-xs text-slate-300 mt-1">{pol.message}</p>
                  </div>
                  <span
                    className={`px-2 py-0.5 rounded text-[11px] font-mono font-bold ${
                      pol.is_compliant
                        ? 'bg-emerald-500/10 text-emerald-400'
                        : 'bg-rose-500/20 text-rose-400'
                    }`}
                  >
                    {pol.is_compliant ? 'PASS' : 'BREACH'}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Stage 4: Cross-Agent Conflict Engine (CORE INNOVATION) */}
      <div
        className={`rounded-xl border overflow-hidden transition ${
          data.conflict.conflict_detected
            ? 'bg-amber-950/15 border-amber-500/40 glow-amber'
            : 'bg-bg-card border-bg-border'
        }`}
      >
        <button
          onClick={() => toggleStep(4)}
          className="w-full px-4 py-3.5 flex items-center justify-between bg-slate-900/40 hover:bg-slate-900/80 transition text-left"
        >
          <div className="flex items-center space-x-3">
            <div
              className={`p-2 rounded-lg border ${
                data.conflict.conflict_detected
                  ? 'bg-amber-500/20 text-amber-400 border-amber-500/30 animate-pulse'
                  : 'bg-slate-800 text-slate-400 border-slate-700'
              }`}
            >
              <GitFork className="w-4 h-4" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-xs font-mono font-bold text-slate-400">STAGE 04</span>
                <span className="text-sm font-semibold text-white">
                  Cross-Agent Conflict Engine (Global Governance)
                </span>
                <span className="text-[10px] px-1.5 py-0.2 rounded bg-brand-blue/20 text-blue-300 font-mono">
                  KEY INNOVATION
                </span>
              </div>
              <p className="text-xs text-slate-300">
                {data.conflict.conflict_detected
                  ? `GLOBAL CONFLICT: ${data.conflict.detected_agents.length} Concurrent Agents Outflow = ${formatINR(data.conflict.aggregate_outflow)}`
                  : 'No concurrent multi-agent conflicts detected'}
              </p>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <StatusBadge type="conflict" value={data.conflict.severity} />
            {expandedSteps[4] ? <ChevronUp className="w-4 h-4 text-slate-400" /> : <ChevronDown className="w-4 h-4 text-slate-400" />}
          </div>
        </button>

        {expandedSteps[4] && (
          <div className="p-4 border-t border-bg-border bg-bg-subtle/60 space-y-3 text-xs">
            <div className="p-3.5 rounded-lg bg-amber-950/20 border border-amber-500/30 text-amber-200 leading-relaxed">
              <span className="font-bold text-amber-300 block font-mono mb-1">
                GLOBAL FINANCIAL CONFLICT ANALYSIS:
              </span>
              {data.conflict.explanation}
            </div>

            {data.conflict.detected_agents.length > 0 && (
              <div className="space-y-2">
                <span className="text-xs font-mono font-semibold text-slate-400 uppercase tracking-wider">
                  Discovered Concurrent Agent Proposals:
                </span>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-2.5">
                  {data.conflict.detected_agents.map((ag) => (
                    <div
                      key={ag.agent_id}
                      className={`p-3 rounded-lg border ${
                        ag.is_current_subject
                          ? 'bg-blue-950/20 border-blue-500/40 ring-1 ring-blue-500/30'
                          : 'bg-slate-900/60 border-slate-800'
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <span className="font-bold text-white font-mono">{ag.agent_name}</span>
                        {ag.is_current_subject && (
                          <span className="text-[10px] px-1 rounded bg-blue-500/20 text-blue-400 font-mono">
                            SUBJECT
                          </span>
                        )}
                      </div>
                      <div className="mt-2 flex items-baseline justify-between">
                        <span className="text-slate-400 text-[11px]">{ag.action_type}</span>
                        <span className="text-sm font-bold font-mono text-emerald-400">
                          {formatINR(ag.amount)}
                        </span>
                      </div>
                      <p className="text-[11px] text-slate-400 mt-1 truncate" title={ag.reason}>
                        {ag.reason}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <div className="grid grid-cols-2 md:grid-cols-4 gap-2 pt-2 border-t border-slate-800">
              <div className="p-2.5 rounded bg-slate-900/50 border border-slate-800">
                <span className="text-slate-400 text-[10px] font-mono block">Available Cash</span>
                <span className="font-mono font-bold text-white">{formatINR(data.conflict.available_cash)}</span>
              </div>
              <div className="p-2.5 rounded bg-slate-900/50 border border-slate-800">
                <span className="text-slate-400 text-[10px] font-mono block">Mandatory Reserve</span>
                <span className="font-mono font-bold text-amber-400">{formatINR(data.conflict.required_reserve)}</span>
              </div>
              <div className="p-2.5 rounded bg-slate-900/50 border border-slate-800">
                <span className="text-slate-400 text-[10px] font-mono block">Aggregate Outflows</span>
                <span className="font-mono font-bold text-rose-400">{formatINR(data.conflict.aggregate_outflow)}</span>
              </div>
              <div className="p-2.5 rounded bg-slate-900/50 border border-slate-800">
                <span className="text-slate-400 text-[10px] font-mono block">Projected Shortfall</span>
                <span className="font-mono font-bold text-rose-400">{formatINR(data.conflict.projected_shortfall)}</span>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Stage 5: Future Impact Prediction */}
      <div className="rounded-xl bg-bg-card border border-bg-border overflow-hidden transition">
        <button
          onClick={() => toggleStep(5)}
          className="w-full px-4 py-3.5 flex items-center justify-between bg-slate-900/40 hover:bg-slate-900/80 transition text-left"
        >
          <div className="flex items-center space-x-3">
            <div className="p-2 rounded-lg bg-orange-500/10 text-orange-400 border border-orange-500/20">
              <TrendingDown className="w-4 h-4" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-xs font-mono font-bold text-slate-400">STAGE 05</span>
                <span className="text-sm font-semibold text-white">Future Impact & Liquidity Forecast</span>
              </div>
              <p className="text-xs text-slate-400">
                Post-Execution Cash: <span className="text-white font-mono">{formatINR(data.future_impact.projected_cash)}</span> | Pressure: <span className="text-orange-400 font-mono">{data.future_impact.future_cash_pressure}</span>
              </p>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <span className="text-xs font-mono text-slate-300">
              Ratio: <span className="font-bold text-emerald-400">{data.future_impact.projected_liquidity_ratio}x</span>
            </span>
            {expandedSteps[5] ? <ChevronUp className="w-4 h-4 text-slate-400" /> : <ChevronDown className="w-4 h-4 text-slate-400" />}
          </div>
        </button>

        {expandedSteps[5] && (
          <div className="p-4 border-t border-bg-border bg-bg-subtle/50 space-y-2 text-xs">
            <p className="text-slate-300 leading-relaxed">{data.future_impact.explanation}</p>
          </div>
        )}
      </div>

      {/* Stage 6: Multi-Factor Risk Assessment */}
      <div className="rounded-xl bg-bg-card border border-bg-border overflow-hidden transition">
        <button
          onClick={() => toggleStep(6)}
          className="w-full px-4 py-3.5 flex items-center justify-between bg-slate-900/40 hover:bg-slate-900/80 transition text-left"
        >
          <div className="flex items-center space-x-3">
            <div className="p-2 rounded-lg bg-rose-500/10 text-brand-rose border border-rose-500/20">
              <AlertTriangle className="w-4 h-4" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-xs font-mono font-bold text-slate-400">STAGE 06</span>
                <span className="text-sm font-semibold text-white">Multi-Factor Risk Engine (ML Regressor)</span>
              </div>
              <p className="text-xs text-slate-400">
                Synthesizing capital magnitude, reserve impact, and cross-agent concurrency
              </p>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <span className="text-sm font-bold font-mono text-rose-400">
              {data.risk_assessment.risk_score.toFixed(1)}/100
            </span>
            <StatusBadge type="risk" value={data.risk_assessment.risk_level} />
            {expandedSteps[6] ? <ChevronUp className="w-4 h-4 text-slate-400" /> : <ChevronDown className="w-4 h-4 text-slate-400" />}
          </div>
        </button>

        {expandedSteps[6] && (
          <div className="p-4 border-t border-bg-border bg-bg-subtle/50 space-y-3 text-xs">
            <div className="space-y-1.5">
              <span className="text-slate-400 font-mono block text-[11px]">Primary Risk Drivers:</span>
              <ul className="space-y-1">
                {data.risk_assessment.risk_factors.map((factor, idx) => (
                  <li key={idx} className="flex items-center space-x-2 text-slate-200">
                    <span className="w-1.5 h-1.5 rounded-full bg-rose-400" />
                    <span>{factor}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </div>

      {/* Stage 7: What-If Simulation Studio */}
      <div className="rounded-xl bg-bg-card border border-bg-border overflow-hidden transition">
        <button
          onClick={() => toggleStep(7)}
          className="w-full px-4 py-3.5 flex items-center justify-between bg-slate-900/40 hover:bg-slate-900/80 transition text-left"
        >
          <div className="flex items-center space-x-3">
            <div className="p-2 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              <SlidersHorizontal className="w-4 h-4" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-xs font-mono font-bold text-slate-400">STAGE 07</span>
                <span className="text-sm font-semibold text-white">What-If Simulation Studio</span>
              </div>
              <p className="text-xs text-slate-400">
                Simulated 4 counterfactual scenarios across cash buffers and liquidity curves
              </p>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <span className="text-xs px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 font-mono">
              4 SCENARIOS TESTED
            </span>
            {expandedSteps[7] ? <ChevronUp className="w-4 h-4 text-slate-400" /> : <ChevronDown className="w-4 h-4 text-slate-400" />}
          </div>
        </button>

        {expandedSteps[7] && (
          <div className="p-4 border-t border-bg-border bg-bg-subtle/50 space-y-3 text-xs">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {data.what_if_scenarios.map((sc) => (
                <div
                  key={sc.scenario_id}
                  className={`p-3.5 rounded-xl border transition ${
                    sc.is_recommended
                      ? 'bg-emerald-950/20 border-emerald-500/50 glow-emerald ring-1 ring-emerald-500/30'
                      : 'bg-bg-card border-slate-800 opacity-80'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-white font-mono">{sc.name}</span>
                    {sc.is_recommended && (
                      <span className="px-2 py-0.5 rounded-full text-[10px] font-extrabold bg-emerald-500 text-slate-950 font-mono">
                        SAFEST OPTION
                      </span>
                    )}
                  </div>
                  <p className="text-slate-300 text-[11px] mt-1">{sc.description}</p>
                  <div className="mt-3 grid grid-cols-3 gap-2 pt-2 border-t border-slate-800/80 font-mono text-[10px]">
                    <div>
                      <span className="text-slate-500 block">Outflow</span>
                      <span className="text-white font-bold">{formatINR(sc.immediate_outflow)}</span>
                    </div>
                    <div>
                      <span className="text-slate-500 block">Post Cash</span>
                      <span className="text-white font-bold">{formatINR(sc.remaining_cash)}</span>
                    </div>
                    <div>
                      <span className="text-slate-500 block">Risk Score</span>
                      <span className={sc.risk_score > 60 ? 'text-rose-400 font-bold' : 'text-emerald-400 font-bold'}>
                        {sc.risk_score.toFixed(0)}/100
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Stage 8: Safe Governed Alternative */}
      <div className="rounded-xl bg-bg-card border border-bg-border overflow-hidden transition">
        <button
          onClick={() => toggleStep(8)}
          className="w-full px-4 py-3.5 flex items-center justify-between bg-slate-900/40 hover:bg-slate-900/80 transition text-left"
        >
          <div className="flex items-center space-x-3">
            <div className="p-2 rounded-lg bg-amber-500/10 text-amber-400 border border-amber-500/20">
              <Lightbulb className="w-4 h-4" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-xs font-mono font-bold text-slate-400">STAGE 08</span>
                <span className="text-sm font-semibold text-white">Safe Alternative Synthesis</span>
              </div>
              <p className="text-xs text-slate-400">
                Constructive mitigation: <span className="text-amber-300 font-mono">{data.safe_alternative.alternative_type}</span>
              </p>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            {expandedSteps[8] ? <ChevronUp className="w-4 h-4 text-slate-400" /> : <ChevronDown className="w-4 h-4 text-slate-400" />}
          </div>
        </button>

        {expandedSteps[8] && (
          <div className="p-4 border-t border-bg-border bg-bg-subtle/50 space-y-3 text-xs">
            <div className="p-3.5 rounded-lg bg-slate-900/70 border border-slate-800">
              <span className="text-xs font-mono font-bold text-emerald-400 block mb-1">
                RECOMMENDED ACTION:
              </span>
              <p className="text-sm font-medium text-white">{data.safe_alternative.recommended_action}</p>
              <p className="text-xs text-slate-400 mt-2">{data.safe_alternative.rationale}</p>
            </div>
          </div>
        )}
      </div>

      {/* Stage 9: Apex Governance Decision */}
      <div className="rounded-xl bg-gradient-to-r from-bg-card to-slate-900 border-2 border-emerald-500/40 glow-emerald overflow-hidden">
        <button
          onClick={() => toggleStep(9)}
          className="w-full px-4 py-4 flex items-center justify-between bg-slate-900/60 hover:bg-slate-900 transition text-left"
        >
          <div className="flex items-center space-x-3">
            <div className="p-2.5 rounded-xl bg-emerald-500/20 text-emerald-400 border border-emerald-500/40">
              <CheckCircle2 className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-xs font-mono font-bold text-emerald-400">STAGE 09</span>
                <span className="text-base font-extrabold text-white">Governed Apex Decision</span>
              </div>
              <p className="text-xs text-slate-300 mt-0.5">
                {data.decision.decision_reason}
              </p>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <StatusBadge type="decision" value={data.decision.decision} className="text-sm px-3 py-1" />
            {expandedSteps[9] ? <ChevronUp className="w-4 h-4 text-slate-400" /> : <ChevronDown className="w-4 h-4 text-slate-400" />}
          </div>
        </button>

        {expandedSteps[9] && (
          <div className="p-4 border-t border-emerald-500/20 bg-bg-subtle/70 space-y-3 text-xs">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3 font-mono">
              <div className="p-3 rounded-lg bg-bg-card border border-slate-800">
                <span className="text-slate-400 block text-[11px]">Approved Execution Amount</span>
                <span className="text-base font-bold text-emerald-400">
                  {formatINR(data.decision.modified_amount ?? data.original_amount)}
                </span>
              </div>
              <div className="p-3 rounded-lg bg-bg-card border border-slate-800">
                <span className="text-slate-400 block text-[11px]">Deferred Buffer Amount</span>
                <span className="text-base font-bold text-amber-400">
                  {formatINR(data.decision.deferred_amount ?? 0)}
                </span>
              </div>
              <div className="p-3 rounded-lg bg-bg-card border border-slate-800">
                <span className="text-slate-400 block text-[11px]">Human Dual-Control Required</span>
                <span className="text-base font-bold text-purple-400">
                  {data.decision.requires_human_approval ? 'YES (ESCALATED)' : 'NO (AUTO-ALLOWED)'}
                </span>
              </div>
            </div>

            {/* Human Approval Action Trigger */}
            {data.status === 'AWAITING_APPROVAL' && onApproveProposal && (
              <div className="p-4 rounded-xl bg-amber-950/30 border border-amber-500/40 flex flex-col sm:flex-row items-center justify-between gap-3">
                <div>
                  <span className="text-xs font-bold text-amber-300 font-mono block">
                    HUMAN APPROVAL REQUIRED (DUAL SIGN-OFF)
                  </span>
                  <p className="text-xs text-slate-300">
                    Sign off to execute the recommended governed amount of {formatINR(data.decision.modified_amount || data.original_amount)}.
                  </p>
                </div>
                <button
                  onClick={() =>
                    onApproveProposal(
                      data.proposal_id,
                      data.decision.modified_amount ?? data.original_amount
                    )
                  }
                  className="px-4 py-2 rounded-lg bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-bold font-mono text-xs shadow-lg shadow-emerald-500/20 transition whitespace-nowrap flex items-center space-x-2"
                >
                  <CheckCircle2 className="w-4 h-4" />
                  <span>Sign & Execute Governed Action</span>
                </button>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Stage 10: Execution & Cryptographic Audit Trail */}
      <div className="rounded-xl bg-bg-card border border-bg-border overflow-hidden transition">
        <div className="px-4 py-3.5 flex items-center justify-between bg-slate-900/40 text-left">
          <div className="flex items-center space-x-3">
            <div className="p-2 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              <FileCheck2 className="w-4 h-4" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-xs font-mono font-bold text-slate-400">STAGE 10</span>
                <span className="text-sm font-semibold text-white">Execution Simulator & Audit Receipt</span>
              </div>
              <p className="text-xs text-slate-400">
                Status: <span className="font-mono text-emerald-400 font-bold">{data.status}</span>
              </p>
            </div>
          </div>
          {onOpenAuditModal && (
            <button
              onClick={() => onOpenAuditModal(data.proposal_id)}
              className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs font-mono text-slate-200 border border-slate-700 flex items-center space-x-1.5 transition"
            >
              <FileCheck2 className="w-3.5 h-3.5 text-emerald-400" />
              <span>View Audit Receipt</span>
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
