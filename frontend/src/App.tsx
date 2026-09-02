import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { Dashboard } from './pages/Dashboard';
import { HeroDemoWalkthrough } from './pages/HeroDemoWalkthrough';
import { AgentsHub } from './pages/AgentsHub';
import { ActionsFeed } from './pages/ActionsFeed';
import { ActionDetail } from './pages/ActionDetail';
import { ConflictCenter } from './pages/ConflictCenter';
import { RiskCenter } from './pages/RiskCenter';
import { SimulationStudio } from './pages/SimulationStudio';
import { ApprovalCenter } from './pages/ApprovalCenter';
import { AuditTrail } from './pages/AuditTrail';
import { ProposeActionModal } from './components/ProposeActionModal';
import { Agent, PendingApproval } from './types';
import { api } from './services/api';

export function App() {
  const [activeTab, setActiveTab] = useState<string>('dashboard');
  const [selectedActionId, setSelectedActionId] = useState<string | null>(null);
  const [agents, setAgents] = useState<Agent[]>([]);
  const [pendingApprovals, setPendingApprovals] = useState<PendingApproval[]>([]);
  const [isProposeModalOpen, setIsProposeModalOpen] = useState(false);
  const [proposeModalAgentId, setProposeModalAgentId] = useState('payout_agent');
  const [isHeroRunning, setIsHeroRunning] = useState(false);
  const [isSubmittingProposal, setIsSubmittingProposal] = useState(false);

  useEffect(() => {
    refreshGlobalData();
  }, []);

  const refreshGlobalData = async () => {
    try {
      const [agentsRes, apprRes] = await Promise.all([
        api.getAgents(),
        api.getPendingApprovals()
      ]);
      setAgents(agentsRes);
      setPendingApprovals(apprRes);
    } catch (err) {
      console.error('Failed refreshing data:', err);
    }
  };

  const handleSelectAction = (actionId: string) => {
    setSelectedActionId(actionId);
    setActiveTab('action-detail');
  };

  const handleBackToFeed = () => {
    setSelectedActionId(null);
    setActiveTab('actions');
  };

  const handleOpenProposeForAgent = (agentId: string) => {
    setProposeModalAgentId(agentId);
    setIsProposeModalOpen(true);
  };

  const handleRunHeroDemo = async () => {
    try {
      setIsHeroRunning(true);
      const res = await api.runHeroDemo();
      await refreshGlobalData();
      setSelectedActionId(res.proposal_id);
      setActiveTab('hero-demo');
    } catch (err) {
      console.error('Hero demo execution failed:', err);
    } finally {
      setIsHeroRunning(false);
    }
  };

  const handleResetSandbox = async () => {
    if (window.confirm('Reset sandbox financial state and active proposals back to pristine ₹6L cash & ₹5L reserve?')) {
      await api.resetFinancialState();
      await refreshGlobalData();
      setActiveTab('dashboard');
    }
  };

  const handleProposeSubmit = async (data: {
    agent_id: string;
    action_type: string;
    amount: number;
    urgency: string;
    priority: number;
    confidence: number;
    reason: string;
  }) => {
    try {
      setIsSubmittingProposal(true);
      const res = await api.proposeAction(data);
      setIsProposeModalOpen(false);
      await refreshGlobalData();
      setSelectedActionId(res.proposal_id);
      setActiveTab('action-detail');
    } catch (err: any) {
      console.error('Proposal submission failed:', err);
      alert(err.response?.data?.detail || 'Proposal submission rejected by FinGuard Action Gateway.');
    } finally {
      setIsSubmittingProposal(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#070B14] text-slate-100 flex flex-col">
      {/* Navigation Header */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={(tab) => {
          setSelectedActionId(null);
          setActiveTab(tab);
        }}
        onOpenProposeModal={() => handleOpenProposeForAgent('payout_agent')}
        onResetState={handleResetSandbox}
        pendingApprovalsCount={pendingApprovals.length}
      />

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {activeTab === 'dashboard' && (
          <Dashboard
            onSelectAction={handleSelectAction}
            onNavigateToHero={() => setActiveTab('hero-demo')}
            onRunHeroDemo={handleRunHeroDemo}
            isHeroRunning={isHeroRunning}
            onOpenProposeModal={() => handleOpenProposeForAgent('payout_agent')}
          />
        )}

        {activeTab === 'hero-demo' && <HeroDemoWalkthrough />}

        {activeTab === 'agents' && (
          <AgentsHub
            onProposeForAgent={handleOpenProposeForAgent}
          />
        )}

        {activeTab === 'actions' && (
          <ActionsFeed
            onSelectAction={handleSelectAction}
            onOpenProposeModal={() => handleOpenProposeForAgent('payout_agent')}
          />
        )}

        {activeTab === 'action-detail' && selectedActionId && (
          <ActionDetail
            actionId={selectedActionId}
            onBack={handleBackToFeed}
          />
        )}

        {activeTab === 'conflicts' && (
          <ConflictCenter onSelectAction={handleSelectAction} />
        )}

        {activeTab === 'risk' && (
          <RiskCenter onSelectAction={handleSelectAction} />
        )}

        {activeTab === 'simulations' && <SimulationStudio />}

        {activeTab === 'approvals' && (
          <ApprovalCenter
            onSelectAction={handleSelectAction}
            onApprovalDone={refreshGlobalData}
          />
        )}

        {activeTab === 'audit' && <AuditTrail />}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800/80 bg-slate-950/60 py-6 font-mono text-xs text-slate-400">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-3">
          <div className="flex items-center space-x-2">
            <span className="font-extrabold text-white">FIN GUARD AI</span>
            <span className="text-slate-600">•</span>
            <span>Financial Governance Control Plane for Autonomous AI Agents</span>
          </div>
          <div className="flex items-center space-x-3 text-slate-500">
            <span>Razorpay AI Builder Internship 2026</span>
            <span>•</span>
            <span className="text-emerald-400 font-semibold">100% Governed Sandbox</span>
          </div>
        </div>
      </footer>

      {/* Propose Action Gateway Modal */}
      <ProposeActionModal
        isOpen={isProposeModalOpen}
        onClose={() => setIsProposeModalOpen(false)}
        onSubmit={handleProposeSubmit}
        agents={agents}
        isSubmitting={isSubmittingProposal}
        initialAgentId={proposeModalAgentId}
      />
    </div>
  );
}

export default App;
