import { CitedText } from '@/common/components/CitedText/CitedText';
import type { CompetitorData } from '@/common/types/valuation';

interface CompetitorCardProps {
  competitor: CompetitorData;
}

export function CompetitorCard({ competitor }: CompetitorCardProps) {
  return (
    <div className="bg-surface-container-lowest p-4 rounded-lg border border-outline-variant/50 hover:border-primary/30 transition-all hover:shadow-sm cursor-pointer group">
      <div className="flex items-center gap-3 mb-2">
        <div className="w-8 h-8 bg-surface-container-high rounded-full flex items-center justify-center border border-outline-variant shrink-0 group-hover:bg-primary/10 group-hover:border-primary/30 transition-colors">
          <span className="material-symbols-outlined text-[16px] text-on-surface-variant group-hover:text-primary transition-colors">corporate_fare</span>
        </div>
        <h4 className="font-bold text-on-surface text-sm flex items-center gap-2">
          {competitor.name}
          {competitor.ticker !== "PRIVATE" && (
            <span className="bg-surface-container-high text-on-surface-variant text-[10px] px-2 py-0.5 rounded border border-outline-variant font-mono">
              {competitor.ticker}
            </span>
          )}
        </h4>
      </div>
      <p className="text-xs text-on-surface-variant leading-relaxed pl-11">
        <CitedText text={competitor.overlap} />
      </p>
    </div>
  );
}
