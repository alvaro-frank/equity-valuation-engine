import { CitedText } from '@/common/components/CitedText/CitedText';

interface ProductCardProps {
  product: string;
  desc: string;
}

export function ProductCard({ product, desc }: ProductCardProps) {
  return (
    <div className="bg-surface-container-lowest p-4 rounded-lg border border-outline-variant/50 hover:border-outline-variant transition-colors group">
      <h4 className="font-bold text-on-surface text-sm mb-1 group-hover:text-primary transition-colors">{product}</h4>
      <p className="text-xs text-on-surface-variant leading-relaxed">
        <CitedText text={desc} />
      </p>
    </div>
  );
}
