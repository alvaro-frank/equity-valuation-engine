import { useTranslation } from 'react-i18next';
import { ProductCard } from '../ProductCard';

interface ProductsListProps {
  products?: Record<string, string>;
}

export function ProductsList({ products }: ProductsListProps) {
  const { t } = useTranslation();
  return (
    <div>
      <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-3 flex items-center gap-2">
        <span className="material-symbols-outlined text-on-surface-variant">category</span>
        {t('thesis_view.products_title')}
      </h3>
      <div className="space-y-3">
        {Object.entries(products || {}).map(([product, desc]) => (
          <ProductCard key={product} product={product} desc={desc as string} />
        ))}
      </div>
    </div>
  );
}
