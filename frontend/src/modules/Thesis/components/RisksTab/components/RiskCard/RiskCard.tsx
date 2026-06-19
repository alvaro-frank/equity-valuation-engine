import { CitedText } from '@/common/components/CitedText/CitedText';

interface RiskCardProps {
  risk: string;
  description: string;
  index: number;
}

export function RiskCard({ risk, description, index }: RiskCardProps) {
  return (
    <div className="bg-surface-container-lowest p-5 rounded-xl border border-outline-variant/50 hover:border-error/30 transition-colors flex gap-4 group">
      <div className="w-10 h-10 rounded-full bg-error/10 flex items-center justify-center shrink-0 border border-error/20 group-hover:bg-error/20 transition-colors">
        <span className="font-bold text-error">{index + 1}</span>
      </div>
      <div>
        <h4 className="font-bold text-on-surface text-base mb-2 group-hover:text-error transition-colors">{risk}</h4>
        <p className="text-sm text-on-surface-variant leading-relaxed">
          <CitedText text={description} />
        </p>
      </div>
    </div>
  );
}
