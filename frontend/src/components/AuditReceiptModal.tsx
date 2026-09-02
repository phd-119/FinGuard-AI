import React, { useState } from 'react';
import { X, Copy, Check, ShieldCheck, FileText, Download } from 'lucide-react';
import { AuditReceipt } from '../types';
import { StatusBadge } from './StatusBadge';

interface AuditReceiptModalProps {
  receipt: AuditReceipt | null;
  isOpen: boolean;
  onClose: () => void;
}

export const AuditReceiptModal: React.FC<AuditReceiptModalProps> = ({
  receipt,
  isOpen,
  onClose
}) => {
  const [copied, setCopied] = useState(false);

  if (!isOpen || !receipt) return null;

  const copyToClipboard = () => {
    navigator.clipboard.writeText(JSON.stringify(receipt, null, 2));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const formatINR = (val: number) => `₹${val.toLocaleString('en-IN')}`;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-fade-in">
      <div className="relative w-full max-w-2xl bg-[#0D1424] border border-emerald-500/40 rounded-2xl shadow-2xl overflow-hidden glow-emerald">
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-slate-900/60">
          <div className="flex items-center space-x-3">
            <div className="p-2 rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <h3 className="text-base font-bold text-white font-mono">
                  FINANCIAL GOVERNANCE RECEIPT
                </h3>
                <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 font-mono font-bold">
                  VERIFIED
                </span>
              </div>
              <p className="text-xs text-slate-400 font-mono">
                Receipt #{receipt.receipt_number}
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-4 max-h-[75vh] overflow-y-auto font-mono text-xs">
          {/* Key Facts */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <div className="p-3 rounded-lg bg-bg-subtle border border-slate-800">
              <span className="text-slate-500 block text-[10px]">Autonomous Agent</span>
              <span className="text-white font-bold">{receipt.agent_name}</span>
            </div>
            <div className="p-3 rounded-lg bg-bg-subtle border border-slate-800">
              <span className="text-slate-500 block text-[10px]">Decision</span>
              <StatusBadge type="decision" value={receipt.governance_decision} />
            </div>
            <div className="p-3 rounded-lg bg-bg-subtle border border-slate-800">
              <span className="text-slate-500 block text-[10px]">Original Amount</span>
              <span className="text-slate-300 font-bold">{formatINR(receipt.original_amount)}</span>
            </div>
            <div className="p-3 rounded-lg bg-bg-subtle border border-slate-800">
              <span className="text-slate-500 block text-[10px]">Approved Amount</span>
              <span className="text-emerald-400 font-bold">{formatINR(receipt.approved_amount)}</span>
            </div>
          </div>

          {/* Rationale Box */}
          <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 space-y-2">
            <span className="text-[10px] uppercase font-bold text-slate-400 tracking-wider">
              FinGuard Decision Rationale & Safety Justification:
            </span>
            <p className="text-slate-200 font-sans text-xs leading-relaxed">
              {receipt.decision_rationale}
            </p>
          </div>

          {/* Cross-Agent Conflict Summary if any */}
          {receipt.conflict_detected && (
            <div className="p-3.5 rounded-xl bg-amber-950/20 border border-amber-500/30 text-amber-200">
              <span className="font-bold block text-amber-300 mb-1">
                Cross-Agent Conflict Intercepted:
              </span>
              <p className="font-sans text-xs">{receipt.conflict_summary}</p>
            </div>
          )}

          {/* Cryptographic Proof & Hash */}
          <div className="p-3 rounded-lg bg-[#070B14] border border-slate-800 space-y-1">
            <span className="text-[10px] text-slate-500 block">Cryptographic Action SHA-256 Hash:</span>
            <span className="text-[11px] text-emerald-400/90 break-all select-all font-mono">
              {receipt.action_hash}
            </span>
          </div>

          {/* Metadata */}
          <div className="flex flex-wrap items-center justify-between text-[11px] text-slate-400 pt-2 border-t border-slate-800">
            <span>Reviewer: <strong className="text-slate-200">{receipt.human_approver || 'Autonomous Plane'}</strong></span>
            <span>Timestamp: <strong className="text-slate-200">{new Date(receipt.timestamp).toLocaleString()}</strong></span>
          </div>
        </div>

        {/* Footer actions */}
        <div className="px-6 py-3.5 border-t border-slate-800 bg-slate-900/40 flex items-center justify-between">
          <button
            onClick={copyToClipboard}
            className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition text-xs font-mono flex items-center space-x-1.5"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
            <span>{copied ? 'Copied JSON!' : 'Copy JSON Payload'}</span>
          </button>
          <button
            onClick={onClose}
            className="px-4 py-1.5 rounded-lg bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-bold text-xs font-mono transition"
          >
            Close Receipt
          </button>
        </div>
      </div>
    </div>
  );
};
