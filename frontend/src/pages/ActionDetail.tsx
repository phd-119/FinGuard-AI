import React, { useState, useEffect } from 'react';
import { ArrowLeft, Sparkles, CheckCircle2, RotateCcw, AlertCircle, FileCheck2 } from 'lucide-react';
import { EvaluationPipelineResponse, AuditReceipt } from '../types';
import { api } from '../services/api';
import { ReasoningFlow } from '../components/ReasoningFlow';
import { AuditReceiptModal } from '../components/AuditReceiptModal';

interface ActionDetailProps {
  actionId: string;
  onBack: () => void;
}

export const ActionDetail: React.FC<ActionDetailProps> = ({ actionId, onBack }) => {
  const [evaluation, setEvaluation] = useState<EvaluationPipelineResponse | null>(null);
  const [auditReceipt, setAuditReceipt] = useState<AuditReceipt | null>(null);
  const [isReceiptOpen, setIsReceiptOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [executing, setExecuting] = useState(false);

  useEffect(() => {
    loadReasoning();
  }, [actionId]);

  const loadReasoning = async () => {
    try {
      setLoading(true);
      const res = await api.getActionReasoning(actionId);
      setEvaluation(res);
    } catch (err) {
      console.error('Failed loading action reasoning:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async (proposalId: string, amount: number) => {
    try {
      setExecuting(true);
      await api.approveAction(proposalId, {
        human_reviewer: 'Lead Treasury Controller (Internship Pitch Reviewer)',
        approved_amount: amount,
        comments: 'Approved governed amount through FinGuard Control Plane.'
      });

      // Reload reasoning to get fresh executed status
      await loadReasoning();

      // Fetch audit receipt
      const receipts = await api.getAuditRecords();
      const match = receipts.find((r) => r.proposal_id === proposalId);
      if (match) {
        setAuditReceipt(match);
        setIsReceiptOpen(true);
      }
    } catch (err) {
      console.error('Approval failed:', err);
    } finally {
      setExecuting(false);
    }
  };

  const handleViewReceipt = async () => {
    try {
      const receipts = await api.getAuditRecords();
      const match = receipts.find((r) => r.proposal_id === actionId);
      if (match) {
        setAuditReceipt(match);
        setIsReceiptOpen(true);
      } else {
        alert('No executed receipt generated for this action yet.');
      }
    } catch (err) {
      console.error('Failed to get receipt:', err);
    }
  };

  if (loading) {
    return (
      <div className="p-16 text-center font-mono text-xs text-slate-400 space-y-2">
        <Sparkles className="w-6 h-6 text-emerald-400 animate-spin mx-auto" />
        <p>Synthesizing FinGuard 10-Stage Governance Pipeline...</p>
      </div>
    );
  }

  if (!evaluation) {
    return (
      <div className="p-8 text-center font-mono text-xs text-rose-400 space-y-4">
        <p>Failed to load proposal telemetry.</p>
        <button
          onClick={onBack}
          className="px-4 py-2 rounded-xl bg-slate-800 text-white"
        >
          Return to Dashboard
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      {/* Top Bar */}
      <div className="flex items-center justify-between">
        <button
          onClick={onBack}
          className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-mono flex items-center space-x-1.5 transition"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Back to Feed</span>
        </button>

        <div className="flex items-center space-x-2">
          <button
            onClick={loadReasoning}
            className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white transition"
            title="Re-evaluate Pipeline"
          >
            <RotateCcw className="w-4 h-4" />
          </button>
          <button
            onClick={handleViewReceipt}
            className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-xs font-mono flex items-center space-x-1.5 transition"
          >
            <FileCheck2 className="w-3.5 h-3.5 text-emerald-400" />
            <span>Audit Receipt</span>
          </button>
        </div>
      </div>

      {/* 10-Stage Reasoning Chain Visualizer */}
      <ReasoningFlow
        data={evaluation}
        onOpenAuditModal={handleViewReceipt}
        onApproveProposal={(id, amt) => handleApprove(id, amt)}
      />

      {/* Cryptographic Audit Modal */}
      <AuditReceiptModal
        receipt={auditReceipt}
        isOpen={isReceiptOpen}
        onClose={() => setIsReceiptOpen(false)}
      />
    </div>
  );
};
