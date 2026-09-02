import React, { useState, useEffect } from 'react';
import { FileText, ShieldCheck, Search, Filter, ArrowUpRight, Copy, Check, Lock } from 'lucide-react';
import { AuditReceipt, LedgerTransaction } from '../types';
import { api } from '../services/api';
import { StatusBadge } from '../components/StatusBadge';
import { AuditReceiptModal } from '../components/AuditReceiptModal';

export const AuditTrail: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'receipts' | 'ledger'>('receipts');
  const [receipts, setReceipts] = useState<AuditReceipt[]>([]);
  const [transactions, setTransactions] = useState<LedgerTransaction[]>([]);
  const [selectedReceipt, setSelectedReceipt] = useState<AuditReceipt | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  useEffect(() => {
    loadAuditData();
  }, []);

  const loadAuditData = async () => {
    try {
      setLoading(true);
      const [recRes, txRes] = await Promise.all([
        api.getAuditRecords(),
        api.getLedgerTransactions()
      ]);
      setReceipts(recRes);
      setTransactions(txRes);
    } catch (err) {
      console.error('Failed loading audit records:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleOpenReceipt = (receipt: AuditReceipt) => {
    setSelectedReceipt(receipt);
    setIsModalOpen(true);
  };

  const formatINR = (val: number) => `₹${val.toLocaleString('en-IN')}`;

  const filteredReceipts = receipts.filter((r) => {
    if (search) {
      const q = search.toLowerCase();
      return (
        r.receipt_number.toLowerCase().includes(q) ||
        r.agent_name.toLowerCase().includes(q) ||
        r.decision_rationale.toLowerCase().includes(q) ||
        r.action_hash.toLowerCase().includes(q)
      );
    }
    return true;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <FileText className="w-5 h-5 text-emerald-400" />
            <h1 className="text-xl font-bold text-white font-mono">
              Immutable Governance Audit Trail & Receipts
            </h1>
          </div>
          <p className="text-xs text-slate-300 mt-1">
            Answers "Why did FinGuard allow, modify, delay, escalate, or block this action?" with cryptographic integrity
          </p>
        </div>

        {/* View Toggle */}
        <div className="flex rounded-xl bg-slate-900 border border-slate-800 p-1 font-mono text-xs self-start sm:self-auto">
          <button
            onClick={() => setActiveTab('receipts')}
            className={`px-3.5 py-1.5 rounded-lg font-bold transition ${
              activeTab === 'receipts'
                ? 'bg-emerald-500 text-slate-950 shadow'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            Decision Receipts ({receipts.length})
          </button>
          <button
            onClick={() => setActiveTab('ledger')}
            className={`px-3.5 py-1.5 rounded-lg font-bold transition ${
              activeTab === 'ledger'
                ? 'bg-emerald-500 text-slate-950 shadow'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            Simulated Ledger ({transactions.length})
          </button>
        </div>
      </div>

      {activeTab === 'receipts' ? (
        <div className="space-y-4">
          {/* Search */}
          <div className="relative">
            <Search className="w-4 h-4 absolute left-3.5 top-3 text-slate-500" />
            <input
              type="text"
              placeholder="Search receipts by receipt number, agent name, or hash..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-10 pr-4 py-2 rounded-xl bg-bg-card border border-slate-800 text-white text-xs font-mono focus:outline-none focus:border-brand-blue"
            />
          </div>

          {/* Table */}
          <div className="rounded-2xl bg-bg-card border border-bg-border overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs font-mono">
                <thead className="bg-slate-900/60 text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-800">
                  <tr>
                    <th className="px-5 py-3">Receipt Number</th>
                    <th className="px-5 py-3">Agent</th>
                    <th className="px-5 py-3">Original / Approved</th>
                    <th className="px-5 py-3">Decision</th>
                    <th className="px-5 py-3">Conflict Detected</th>
                    <th className="px-5 py-3">Signoff</th>
                    <th className="px-5 py-3 text-right">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60">
                  {filteredReceipts.length === 0 ? (
                    <tr>
                      <td colSpan={7} className="px-5 py-8 text-center text-slate-500">
                        No cryptographic receipts minted yet. Execute actions or run the Hero Demo.
                      </td>
                    </tr>
                  ) : (
                    filteredReceipts.map((rec) => (
                      <tr
                        key={rec.receipt_number}
                        onClick={() => handleOpenReceipt(rec)}
                        className="hover:bg-slate-800/40 cursor-pointer transition"
                      >
                        <td className="px-5 py-3.5 font-bold text-white whitespace-nowrap">
                          {rec.receipt_number}
                        </td>
                        <td className="px-5 py-3.5 text-slate-300">
                          {rec.agent_name}
                        </td>
                        <td className="px-5 py-3.5 whitespace-nowrap">
                          <span className="text-slate-400 line-through mr-1.5">
                            {formatINR(rec.original_amount)}
                          </span>
                          <span className="text-emerald-400 font-bold">
                            {formatINR(rec.approved_amount)}
                          </span>
                        </td>
                        <td className="px-5 py-3.5">
                          <StatusBadge type="decision" value={rec.governance_decision} />
                        </td>
                        <td className="px-5 py-3.5">
                          <span
                            className={`px-2 py-0.5 rounded text-[11px] font-bold ${
                              rec.conflict_detected
                                ? 'bg-amber-500/20 text-amber-400'
                                : 'bg-slate-800 text-slate-400'
                            }`}
                          >
                            {rec.conflict_detected ? 'YES' : 'NO'}
                          </span>
                        </td>
                        <td className="px-5 py-3.5 text-slate-400">
                          {rec.human_approver || 'Automated'}
                        </td>
                        <td className="px-5 py-3.5 text-right">
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              handleOpenReceipt(rec);
                            }}
                            className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition"
                          >
                            <ArrowUpRight className="w-3.5 h-3.5" />
                          </button>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      ) : (
        /* Ledger View */
        <div className="rounded-2xl bg-bg-card border border-bg-border overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs font-mono">
              <thead className="bg-slate-900/60 text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-800">
                <tr>
                  <th className="px-5 py-3">Tx Reference</th>
                  <th className="px-5 py-3">Agent</th>
                  <th className="px-5 py-3">Transaction Type</th>
                  <th className="px-5 py-3">Amount</th>
                  <th className="px-5 py-3">Balance After</th>
                  <th className="px-5 py-3">Timestamp</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {transactions.map((tx) => (
                  <tr key={tx.id} className="hover:bg-slate-800/30">
                    <td className="px-5 py-3.5 font-bold text-white">{tx.reference}</td>
                    <td className="px-5 py-3.5 text-slate-300">{tx.agent_id}</td>
                    <td className="px-5 py-3.5 text-slate-400">{tx.transaction_type}</td>
                    <td className="px-5 py-3.5 text-emerald-400 font-bold">
                      {formatINR(tx.amount)}
                    </td>
                    <td className="px-5 py-3.5 text-white font-bold">
                      {formatINR(tx.balance_after)}
                    </td>
                    <td className="px-5 py-3.5 text-slate-500">
                      {new Date(tx.timestamp).toLocaleString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Cryptographic Receipt Modal */}
      <AuditReceiptModal
        receipt={selectedReceipt}
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
      />
    </div>
  );
};
