import React, { useState, useEffect } from 'react';
import { CheckCircle2, XCircle, AlertTriangle, ShieldCheck, ArrowRight, Bot } from 'lucide-react';
import { PendingApproval } from '../types';
import { api } from '../services/api';
import { StatusBadge } from '../components/StatusBadge';

interface ApprovalCenterProps {
  onSelectAction: (actionId: string) => void;
  onApprovalDone: () => void;
}

export const ApprovalCenter: React.FC<ApprovalCenterProps> = ({
  onSelectAction,
  onApprovalDone
}) => {
  const [approvals, setApprovals] = useState<PendingApproval[]>([]);
  const [loading, setLoading] = useState(true);
  const [processingId, setProcessingId] = useState<string | null>(null);

  useEffect(() => {
    loadApprovals();
  }, []);

  const loadApprovals = async () => {
    try {
      setLoading(true);
      const res = await api.getPendingApprovals();
      setApprovals(res);
    } catch (err) {
      console.error('Failed loading approvals:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async (proposalId: string, amount: number) => {
    try {
      setProcessingId(proposalId);
      await api.approveAction(proposalId, {
        human_reviewer: 'Treasury Lead (You)',
        approved_amount: amount,
        comments: 'Approved governed amount via Human Approval Center.'
      });
      await loadApprovals();
      onApprovalDone();
    } catch (err) {
      console.error('Approval failed:', err);
    } finally {
      setProcessingId(null);
    }
  };

  const handleReject = async (proposalId: string) => {
    try {
      setProcessingId(proposalId);
      await api.rejectAction(proposalId, {
        human_reviewer: 'Treasury Lead (You)',
        comments: 'Rejected by human reviewer due to liquidity preservation priority.'
      });
      await loadApprovals();
      onApprovalDone();
    } catch (err) {
      console.error('Rejection failed:', err);
    } finally {
      setProcessingId(null);
    }
  };

  const formatINR = (val: number) => `₹${val.toLocaleString('en-IN')}`;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <div className="flex items-center space-x-2">
          <CheckCircle2 className="w-5 h-5 text-purple-400" />
          <h1 className="text-xl font-bold text-white font-mono">
            Human Approval & Dual-Control Center
          </h1>
        </div>
        <p className="text-xs text-slate-300 mt-1">
          High-risk, policy exception, or modified autonomous agent proposals requiring dual human authorization
        </p>
      </div>

      {/* Approvals List */}
      <div className="space-y-4">
        {approvals.length === 0 ? (
          <div className="p-12 rounded-2xl bg-bg-card border border-bg-border text-center text-slate-500 font-mono text-xs">
            <ShieldCheck className="w-8 h-8 text-emerald-400 mx-auto mb-2" />
            <p>No actions currently pending human approval.</p>
            <p className="text-slate-600 mt-1">All proposed actions have been governed or auto-cleared.</p>
          </div>
        ) : (
          approvals.map((appr) => (
            <div
              key={appr.approval_id}
              className="p-6 rounded-2xl bg-gradient-to-r from-bg-card via-slate-900 to-bg-card border border-purple-500/40 glow-purple space-y-4"
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-4">
                <div className="flex items-center space-x-3 font-mono">
                  <div className="p-2 rounded-xl bg-purple-500/20 text-purple-400">
                    <Bot className="w-5 h-5" />
                  </div>
                  <div>
                    <div className="flex items-center space-x-2">
                      <span className="text-sm font-bold text-white">{appr.agent_name}</span>
                      <span className="text-slate-500">•</span>
                      <span className="text-slate-400">{appr.action_type}</span>
                      <StatusBadge type="decision" value={appr.governance_decision} />
                    </div>
                    <span className="text-xs text-slate-400">
                      Requested at: {new Date(appr.requested_at).toLocaleString()}
                    </span>
                  </div>
                </div>

                <div className="flex items-center space-x-2">
                  <StatusBadge type="risk" value={appr.risk_level} />
                  <button
                    onClick={() => onSelectAction(appr.proposal_id)}
                    className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition"
                  >
                    <ArrowRight className="w-4 h-4" />
                  </button>
                </div>
              </div>

              {/* Rationale & Modification breakdown */}
              <div className="p-3.5 rounded-xl bg-slate-950/70 border border-slate-800 text-xs font-sans text-slate-200">
                <span className="font-mono font-bold text-amber-300 block mb-1">
                  FinGuard Recommendation:
                </span>
                {appr.decision_reason}
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 font-mono text-xs">
                <div className="p-3 rounded-lg bg-bg-subtle border border-slate-800">
                  <span className="text-slate-500 text-[10px] block">Original Requested</span>
                  <span className="text-slate-300 font-bold">{formatINR(appr.original_amount)}</span>
                </div>
                <div className="p-3 rounded-lg bg-bg-subtle border border-slate-800">
                  <span className="text-slate-500 text-[10px] block">Recommended Immediate</span>
                  <span className="text-emerald-400 font-bold">{formatINR(appr.recommended_amount)}</span>
                </div>
                <div className="p-3 rounded-lg bg-bg-subtle border border-slate-800">
                  <span className="text-slate-500 text-[10px] block">Deferred Balance</span>
                  <span className="text-amber-400 font-bold">{formatINR(appr.deferred_amount)}</span>
                </div>
                <div className="p-3 rounded-lg bg-bg-subtle border border-slate-800">
                  <span className="text-slate-500 text-[10px] block">Assessed Risk Score</span>
                  <span className="text-rose-400 font-bold">{appr.risk_score.toFixed(0)}/100</span>
                </div>
              </div>

              {/* Approval Buttons */}
              <div className="pt-2 flex items-center justify-end space-x-3 font-mono text-xs">
                <button
                  onClick={() => handleReject(appr.proposal_id)}
                  disabled={processingId === appr.proposal_id}
                  className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-rose-950/60 hover:text-rose-400 hover:border-rose-500/40 text-slate-300 border border-slate-700 transition flex items-center space-x-1.5 disabled:opacity-50"
                >
                  <XCircle className="w-4 h-4" />
                  <span>Reject Outright</span>
                </button>

                <button
                  onClick={() => handleApprove(appr.proposal_id, appr.recommended_amount)}
                  disabled={processingId === appr.proposal_id}
                  className="px-5 py-2 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-400 hover:from-emerald-400 hover:to-teal-300 text-slate-950 font-bold transition flex items-center space-x-1.5 shadow-lg shadow-emerald-500/20 disabled:opacity-50"
                >
                  <CheckCircle2 className="w-4 h-4" />
                  <span>
                    {processingId === appr.proposal_id
                      ? 'Executing...'
                      : `Sign & Execute (${formatINR(appr.recommended_amount)})`}
                  </span>
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
