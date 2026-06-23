import { CitedText } from '@/common/components/CitedText/CitedText';

interface ProductCardProps {
  product: string;
  desc: string;
}

export function ProductCard({ product, desc }: ProductCardProps) {
  return (
    <div className="bg-surface-container-lowest p-6 rounded-2xl border border-outline-variant/50">
      <h4 className="font-bold text-on-surface text-sm mb-1">{product}</h4>
      <p className="text-xs text-on-surface-variant leading-relaxed">
        <CitedText text={desc} />
      </p>
    </div>
  );
}
