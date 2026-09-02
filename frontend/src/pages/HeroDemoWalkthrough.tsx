import React, { useState } from 'react';
import {
  Play,
  RotateCcw,
  CheckCircle2,
  ShieldCheck,
  AlertTriangle,
  GitFork,
  ArrowRight,
  Sparkles,
  Bot,
  SlidersHorizontal,
  FileCheck2,
  Lock
} from 'lucide-react';
import { EvaluationPipelineResponse, AuditReceipt } from '../types';
import { api } from '../services/api';
import { StatusBadge } from '../components/StatusBadge';
import { ReasoningFlow } from '../components/ReasoningFlow';
import { AuditReceiptModal } from '../components/AuditReceiptModal';

export const HeroDemoWalkthrough: React.FC = () => {
  const [currentStep, setCurrentStep] = useState<number>(0);
  const [loading, setLoading] = useState(false);
  const [evaluation, setEvaluation] = useState<EvaluationPipelineResponse | null>(null);
  const [auditReceipt, setAuditReceipt] = useState<AuditReceipt | null>(null);
  const [isReceiptOpen, setIsReceiptOpen] = useState(false);
  const [stepData, setStepData] = useState<any>(null);

  const formatINR = (val?: number) => {
    if (val === undefined || val === null) return '₹0';
    return `₹${val.toLocaleString('en-IN')}`;
  };

  // Step 1: Initialize Baseline
  const handleStep1Setup = async () => {
    try {
      setLoading(true);
      const res = await api.setupHeroDemo();
      setStepData(res);
      setCurrentStep(1);
    } catch (err) {
      console.error('Setup failed:', err);
    } finally {
      setLoading(false);
    }
  };

  // Step 2: Run Full FinGuard Governance Pipeline
  const handleStep2RunPipeline = async () => {
    try {
      setLoading(true);
      const res = await api.runHeroDemo();
      setEvaluation(res);
      setCurrentStep(2);
    } catch (err) {
      console.error('Run demo failed:', err);
    } finally {
      setLoading(false);
    }
  };

  // Step 3: Human Approves Governed Modification
  const handleStep3Approve = async () => {
    try {
      setLoading(true);
      const res = await api.executeHeroApproval();
      setStepData((prev: any) => ({ ...prev, execution: res }));

      // Fetch the minted audit receipt
      const receipts = await api.getAuditRecords();
      if (receipts.length > 0) {
        setAuditReceipt(receipts[0]);
      }

      setCurrentStep(3);
    } catch (err) {
      console.error('Execution failed:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = async () => {
    setCurrentStep(0);
    setEvaluation(null);
    setAuditReceipt(null);
    setStepData(null);
    await api.resetFinancialState();
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      {/* Top Header */}
      <div className="p-6 rounded-2xl bg-gradient-to-r from-bg-card via-slate-900 to-bg-card border border-emerald-500/30">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-2">
              <span className="px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                PITCH-READY HERO SCENARIO
              </span>
              <span className="text-xs text-slate-400 font-mono">
                5-Minute Interactive Demonstration
              </span>
            </div>
            <h1 className="text-2xl font-extrabold text-white font-mono mt-1">
              Global Multi-Agent Financial Governance Demo
            </h1>
            <p className="text-xs sm:text-sm text-slate-300 mt-1 max-w-2xl">
              Witness how FinGuard AI prevents catastrophic collective liquidity failure when 
              multiple independent autonomous AI agents submit simultaneous uncoordinated financial actions.
            </p>
          </div>

          <div className="flex items-center space-x-3">
            <button
              onClick={handleReset}
              className="px-3 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 font-mono text-xs flex items-center space-x-1.5 transition"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>Reset Demo</span>
            </button>
          </div>
        </div>

        {/* Stepper Progress Bar */}
        <div className="mt-6 grid grid-cols-1 sm:grid-cols-4 gap-3 font-mono text-xs">
          <div
            className={`p-3 rounded-xl border flex items-center space-x-2.5 ${
              currentStep >= 0
                ? 'bg-slate-900 border-brand-blue text-white'
                : 'bg-slate-950/40 border-slate-800 text-slate-500'
            }`}
          >
            <span className="w-6 h-6 rounded-full bg-brand-blue text-white flex items-center justify-center font-bold text-xs">
              1
            </span>
            <span className="truncate">1. Problem Setup</span>
          </div>

          <div
            className={`p-3 rounded-xl border flex items-center space-x-2.5 ${
              currentStep >= 1
                ? 'bg-slate-900 border-amber-500/50 text-white'
                : 'bg-slate-950/40 border-slate-800 text-slate-500'
            }`}
          >
            <span className={`w-6 h-6 rounded-full flex items-center justify-center font-bold text-xs ${
              currentStep >= 1 ? 'bg-amber-500 text-slate-950' : 'bg-slate-800 text-slate-500'
            }`}>
              2
            </span>
            <span className="truncate">2. Agent Collisions</span>
          </div>

          <div
            className={`p-3 rounded-xl border flex items-center space-x-2.5 ${
              currentStep >= 2
                ? 'bg-slate-900 border-purple-500/50 text-white'
                : 'bg-slate-950/40 border-slate-800 text-slate-500'
            }`}
          >
            <span className={`w-6 h-6 rounded-full flex items-center justify-center font-bold text-xs ${
              currentStep >= 2 ? 'bg-purple-500 text-white' : 'bg-slate-800 text-slate-500'
            }`}>
              3
            </span>
            <span className="truncate">3. FinGuard Decision</span>
          </div>

          <div
            className={`p-3 rounded-xl border flex items-center space-x-2.5 ${
              currentStep >= 3
                ? 'bg-slate-900 border-emerald-500 text-white'
                : 'bg-slate-950/40 border-slate-800 text-slate-500'
            }`}
          >
            <span className={`w-6 h-6 rounded-full flex items-center justify-center font-bold text-xs ${
              currentStep >= 3 ? 'bg-emerald-500 text-slate-950' : 'bg-slate-800 text-slate-500'
            }`}>
              4
            </span>
            <span className="truncate">4. Safe Execution</span>
          </div>
        </div>
      </div>

      {/* PHASE 0 & 1: Initial State & Problem Presentation */}
      {currentStep === 0 && (
        <div className="p-8 rounded-2xl bg-bg-card border border-bg-border space-y-6 text-center">
          <div className="max-w-2xl mx-auto space-y-4">
            <div className="w-16 h-16 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center mx-auto text-emerald-400">
              <Play className="w-8 h-8 ml-1" />
            </div>
            <h2 className="text-xl font-bold text-white font-mono">
              Ready to Run the Hero Governance Scenario
            </h2>
            <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 text-left font-mono text-xs space-y-2">
              <div className="flex justify-between">
                <span className="text-slate-400">Merchant Available Cash:</span>
                <span className="text-white font-bold">₹6,00,000</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Mandatory Statutory Reserve:</span>
                <span className="text-amber-400 font-bold">₹5,00,000</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Unreserved Free Cash:</span>
                <span className="text-emerald-400 font-bold">₹1,00,000</span>
              </div>
              <div className="pt-2 border-t border-slate-800 text-slate-300">
                <span className="text-rose-400 font-bold">The Threat:</span> Payout Agent (₹4L) + Growth Agent (₹2L) + Refund Agent (₹1L) = ₹7L concurrent proposed outflow!
              </div>
            </div>
            <button
              onClick={handleStep1Setup}
              disabled={loading}
              className="px-6 py-3 rounded-xl bg-gradient-to-r from-brand-blue to-emerald-500 hover:from-blue-600 hover:to-emerald-600 text-white font-bold font-mono text-sm shadow-xl shadow-blue-500/25 transition flex items-center justify-center space-x-2 mx-auto disabled:opacity-50"
            >
              <span>{loading ? 'Initializing...' : 'Step 1: Initialize Merchant & Discover Agents'}</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}

      {/* PHASE 1: Concurrent Agent Proposals Ingested */}
      {currentStep === 1 && (
        <div className="space-y-6">
          <div className="p-6 rounded-2xl bg-amber-950/20 border border-amber-500/40 space-y-4">
            <div className="flex items-center space-x-2">
              <AlertTriangle className="w-5 h-5 text-amber-400" />
              <h3 className="text-base font-bold text-white font-mono">
                Concurrent Agent Proposals Active in System
              </h3>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">
              Two background agents already have pending proposals in the queue. 
              Now, the <strong className="text-white">Payout Agent</strong> is proposing an urgent <strong className="text-emerald-400">₹4,00,000</strong> supplier settlement.
            </p>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-3 font-mono text-xs">
              <div className="p-3.5 rounded-xl bg-slate-900 border border-slate-800">
                <div className="flex justify-between">
                  <span className="font-bold text-white">Growth Agent</span>
                  <span className="text-amber-400 font-bold">₹2,00,000</span>
                </div>
                <p className="text-[11px] text-slate-400 mt-1 font-sans">
                  Q4 Omnichannel Festive Marketing Blitz
                </p>
              </div>

              <div className="p-3.5 rounded-xl bg-slate-900 border border-slate-800">
                <div className="flex justify-between">
                  <span className="font-bold text-white">Refund Agent</span>
                  <span className="text-amber-400 font-bold">₹1,00,000</span>
                </div>
                <p className="text-[11px] text-slate-400 mt-1 font-sans">
                  Bulk customer refund settlement batch
                </p>
              </div>

              <div className="p-3.5 rounded-xl bg-blue-950/30 border border-blue-500/40 ring-1 ring-blue-500/30">
                <div className="flex justify-between">
                  <span className="font-bold text-white">Payout Agent (New)</span>
                  <span className="text-emerald-400 font-bold">₹4,00,000</span>
                </div>
                <p className="text-[11px] text-slate-400 mt-1 font-sans">
                  Raw material invoice #INV-9902 settlement
                </p>
              </div>
            </div>

            <div className="p-3 rounded-lg bg-slate-950/60 border border-slate-800 flex items-center justify-between font-mono text-xs">
              <span>Combined Proposed Outflows: <strong className="text-rose-400 font-bold">₹7,00,000</strong></span>
              <span>Available Cash: <strong className="text-white">₹6,00,000</strong></span>
              <span>Required Reserve: <strong className="text-amber-400">₹5,00,000</strong></span>
            </div>

            <div className="flex justify-end pt-2">
              <button
                onClick={handleStep2RunPipeline}
                disabled={loading}
                className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-400 hover:from-emerald-400 hover:to-teal-300 text-slate-950 font-bold font-mono text-xs shadow-lg shadow-emerald-500/20 transition flex items-center space-x-2 disabled:opacity-50"
              >
                <Sparkles className="w-4 h-4" />
                <span>{loading ? 'Evaluating Pipeline...' : 'Step 2: Pass Payout Action Through FinGuard'}</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* PHASE 2 & 3: FinGuard 10-Stage Pipeline Reasoning Chain */}
      {currentStep >= 2 && evaluation && (
        <div className="space-y-6">
          <ReasoningFlow
            data={evaluation}
            onOpenAuditModal={() => setIsReceiptOpen(true)}
            onApproveProposal={handleStep3Approve}
          />
        </div>
      )}

      {/* PHASE 3: Execution Successful Screen */}
      {currentStep === 3 && stepData?.execution && (
        <div className="p-6 rounded-2xl bg-gradient-to-r from-emerald-950/40 via-slate-900 to-emerald-950/40 border border-emerald-500/50 glow-emerald space-y-4 font-mono text-xs">
          <div className="flex items-center space-x-3">
            <div className="p-2 rounded-xl bg-emerald-500/20 text-emerald-400">
              <CheckCircle2 className="w-6 h-6" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white font-mono">
                FINANCIAL GOVERNANCE & EXECUTION COMPLETE
              </h3>
              <p className="text-xs text-slate-300">
                Transaction reference: <span className="text-emerald-400 font-bold">{stepData.execution.transaction_reference}</span>
              </p>
            </div>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2">
            <div className="p-3 rounded-lg bg-bg-card border border-slate-800">
              <span className="text-slate-500 text-[10px]">Original Proposal</span>
              <span className="text-slate-300 font-bold block">{formatINR(stepData.execution.original_amount)}</span>
            </div>
            <div className="p-3 rounded-lg bg-bg-card border border-slate-800">
              <span className="text-slate-500 text-[10px]">Executed Amount</span>
              <span className="text-emerald-400 font-bold block">{formatINR(stepData.execution.executed_amount)}</span>
            </div>
            <div className="p-3 rounded-lg bg-bg-card border border-slate-800">
              <span className="text-slate-500 text-[10px]">Deferred Amount</span>
              <span className="text-amber-400 font-bold block">{formatINR(stepData.execution.deferred_amount)}</span>
            </div>
            <div className="p-3 rounded-lg bg-bg-card border border-slate-800">
              <span className="text-slate-500 text-[10px]">Merchant Cash Remaining</span>
              <span className="text-white font-bold block">{formatINR(stepData.execution.updated_cash)}</span>
            </div>
          </div>

          <div className="p-3.5 rounded-xl bg-emerald-950/30 border border-emerald-500/30 text-emerald-200">
            <span className="font-bold text-emerald-400 block mb-1">
              RESERVE FLOOR FULLY PROTECTED (100% INTACT):
            </span>
            Merchant cash balance stands at ₹5,00,000, exactly preserving the statutory reserve requirement without default. 
            Cryptographic audit receipt minted and verifiable.
          </div>

          <div className="flex justify-end space-x-3 pt-2">
            <button
              onClick={() => setIsReceiptOpen(true)}
              className="px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-white font-mono text-xs border border-slate-700 flex items-center space-x-2 transition"
            >
              <FileCheck2 className="w-4 h-4 text-emerald-400" />
              <span>Inspect Cryptographic Receipt</span>
            </button>
          </div>
        </div>
      )}

      {/* Audit Receipt Modal */}
      <AuditReceiptModal
        receipt={auditReceipt}
        isOpen={isReceiptOpen}
        onClose={() => setIsReceiptOpen(false)}
      />
    </div>
  );
};
