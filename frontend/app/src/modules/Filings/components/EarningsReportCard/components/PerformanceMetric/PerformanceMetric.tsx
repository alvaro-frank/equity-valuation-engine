import { MetricBadge } from '../MetricBadge';

export function PerformanceMetric({ label, value, growth, isMargin }: { label: string; value: string; growth?: number | string | null, isMargin?: boolean }) {
  return (
    <div className="bg-surface-container border border-outline-variant rounded p-4">
      <span className="text-xs font-semibold text-on-surface-variant uppercase tracking-wider block mb-1">{label}</span>
      <div className="flex items-center">
        <span className="text-xl font-bold text-on-surface">{value}</span>
        <MetricBadge value={growth} isMargin={isMargin} />
      </div>
    </div>
  );
}
