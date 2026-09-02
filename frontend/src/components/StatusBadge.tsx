import React from 'react';

interface StatusBadgeProps {
  type: 'decision' | 'risk' | 'status' | 'conflict' | 'urgency' | 'trust';
  value: string | number | null | undefined;
  className?: string;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ type, value, className = '' }) => {
  if (value === null || value === undefined) {
    return <span className="text-xs text-slate-500 font-mono">-</span>;
  }

  const strVal = String(value).toUpperCase();

  let colorClasses = 'bg-slate-800 text-slate-300 border-slate-700';

  if (type === 'decision') {
    switch (strVal) {
      case 'ALLOW':
        colorClasses = 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
        break;
      case 'MODIFY':
        colorClasses = 'bg-amber-500/10 text-amber-400 border-amber-500/30';
        break;
      case 'DELAY':
        colorClasses = 'bg-blue-500/10 text-blue-400 border-blue-500/30';
        break;
      case 'ESCALATE':
        colorClasses = 'bg-purple-500/10 text-purple-400 border-purple-500/30';
        break;
      case 'BLOCK':
        colorClasses = 'bg-rose-500/10 text-rose-400 border-rose-500/30';
        break;
    }
  } else if (type === 'risk' || type === 'conflict') {
    switch (strVal) {
      case 'LOW':
      case 'NONE':
        colorClasses = 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
        break;
      case 'MEDIUM':
        colorClasses = 'bg-amber-500/10 text-amber-400 border-amber-500/30';
        break;
      case 'HIGH':
        colorClasses = 'bg-orange-500/10 text-orange-400 border-orange-500/30';
        break;
      case 'CRITICAL':
        colorClasses = 'bg-rose-500/15 text-rose-400 border-rose-500/40 animate-pulse';
        break;
    }
  } else if (type === 'status') {
    switch (strVal) {
      case 'EXECUTED':
      case 'APPROVED':
        colorClasses = 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
        break;
      case 'AWAITING_APPROVAL':
      case 'PROPOSED':
      case 'EVALUATING':
        colorClasses = 'bg-amber-500/10 text-amber-400 border-amber-500/30';
        break;
      case 'BLOCKED':
      case 'REJECTED':
        colorClasses = 'bg-rose-500/10 text-rose-400 border-rose-500/30';
        break;
      case 'DELAYED':
        colorClasses = 'bg-blue-500/10 text-blue-400 border-blue-500/30';
        break;
    }
  } else if (type === 'trust') {
    switch (strVal) {
      case 'VERIFIED':
      case 'HIGH':
        colorClasses = 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
        break;
      case 'MEDIUM':
        colorClasses = 'bg-amber-500/10 text-amber-400 border-amber-500/30';
        break;
      case 'LOW':
      case 'RESTRICTED':
        colorClasses = 'bg-rose-500/10 text-rose-400 border-rose-500/30';
        break;
    }
  } else if (type === 'urgency') {
    switch (strVal) {
      case 'LOW':
        colorClasses = 'bg-slate-800 text-slate-400 border-slate-700';
        break;
      case 'MEDIUM':
        colorClasses = 'bg-blue-500/10 text-blue-400 border-blue-500/30';
        break;
      case 'HIGH':
        colorClasses = 'bg-amber-500/10 text-amber-400 border-amber-500/30';
        break;
      case 'CRITICAL':
        colorClasses = 'bg-rose-500/10 text-rose-400 border-rose-500/30';
        break;
    }
  }

  return (
    <span
      className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold font-mono border ${colorClasses} ${className}`}
    >
      {strVal}
    </span>
  );
};
