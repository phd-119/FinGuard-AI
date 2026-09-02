import React from 'react';
import { LucideIcon } from 'lucide-react';

interface MetricCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: LucideIcon;
  trend?: string;
  trendPositive?: boolean;
  variant?: 'default' | 'emerald' | 'amber' | 'rose' | 'blue' | 'purple';
  onClick?: () => void;
}

export const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  subtitle,
  icon: Icon,
  trend,
  trendPositive,
  variant = 'default',
  onClick
}) => {
  const variantStyles = {
    default: 'border-slate-800 bg-[#0D1424] hover:border-slate-700',
    emerald: 'border-emerald-500/20 bg-emerald-950/10 hover:border-emerald-500/40 glow-emerald',
    amber: 'border-amber-500/20 bg-amber-950/10 hover:border-amber-500/40 glow-amber',
    rose: 'border-rose-500/20 bg-rose-950/10 hover:border-rose-500/40 glow-rose',
    blue: 'border-blue-500/20 bg-blue-950/10 hover:border-blue-500/40 glow-blue',
    purple: 'border-purple-500/20 bg-purple-950/10 hover:border-purple-500/40'
  };

  const iconColors = {
    default: 'text-slate-400 bg-slate-800/60',
    emerald: 'text-emerald-400 bg-emerald-500/10',
    amber: 'text-amber-400 bg-amber-500/10',
    rose: 'text-rose-400 bg-rose-500/10',
    blue: 'text-blue-400 bg-blue-500/10',
    purple: 'text-purple-400 bg-purple-500/10'
  };

  return (
    <div
      onClick={onClick}
      className={`relative p-5 rounded-xl border backdrop-blur-sm transition-all duration-200 ${variantStyles[variant]} ${
        onClick ? 'cursor-pointer hover:-translate-y-0.5' : ''
      }`}
    >
      <div className="flex items-center justify-between">
        <span className="text-xs font-semibold uppercase tracking-wider text-slate-400 font-mono">
          {title}
        </span>
        <div className={`p-2 rounded-lg ${iconColors[variant]}`}>
          <Icon className="w-4 h-4" />
        </div>
      </div>

      <div className="mt-3 flex items-baseline justify-between">
        <span className="text-2xl font-bold tracking-tight text-white font-mono">
          {value}
        </span>
        {trend && (
          <span
            className={`text-xs font-semibold font-mono ${
              trendPositive ? 'text-emerald-400' : 'text-rose-400'
            }`}
          >
            {trend}
          </span>
        )}
      </div>

      {subtitle && (
        <p className="mt-1 text-xs text-slate-400">
          {subtitle}
        </p>
      )}
    </div>
  );
};
