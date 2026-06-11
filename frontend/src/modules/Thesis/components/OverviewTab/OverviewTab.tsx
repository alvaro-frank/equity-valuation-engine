import { useTranslation } from 'react-i18next';
import { QualityStarRating } from '../QualityStarRating';

// --- Sub-Components (Rule 2.21, 2.23, 2.30, 2.41) ---

function TextSection({ icon, iconColor, title, content }: { icon: string; iconColor: string; title: string; content: string }) {
  return (
    <div>
      <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-3 flex items-center gap-2">
        <span className={`material-symbols-outlined ${iconColor}`}>{icon}</span>
        {title}
      </h3>
      <div className="prose prose-sm dark:prose-invert max-w-none text-on-surface-variant leading-relaxed bg-surface-container-lowest p-5 rounded-lg border border-outline-variant/50">
        <p>{content}</p>
      </div>
    </div>
  );
}

import type { QualityPillars } from '@/common/types/valuation';

function QualitySection({ qualityPillars }: { qualityPillars: QualityPillars | undefined }) {
  const { t } = useTranslation();
  if (!qualityPillars) return null;

  return (
    <div>
      <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-3 flex items-center gap-2">
        <span className="material-symbols-outlined text-[16px] text-primary">verified</span>
        {t('thesis_view.quality_pillars.title')}
      </h3>
      <QualityStarRating data={qualityPillars} />
    </div>
  );
}

function ProductCard({ product, desc }: { product: string; desc: string }) {
  return (
    <div className="bg-surface-container-lowest p-4 rounded-lg border border-outline-variant/50 hover:border-outline-variant transition-colors group">
      <h4 className="font-bold text-on-surface text-sm mb-1 group-hover:text-primary transition-colors">{product}</h4>
      <p className="text-xs text-on-surface-variant leading-relaxed">{desc}</p>
    </div>
  );
}

function ProductsList({ products }: { products: Record<string, string> }) {
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

// --- Main Component ---

import type { QualitativeValuationResult } from '@/common/types/valuation';

interface OverviewTabProps {
  qualData: QualitativeValuationResult;
}

export function OverviewTab({ qualData }: OverviewTabProps) {
  const { t } = useTranslation();

  return (
    <div className="space-y-8 animate-in slide-in-from-right-4 fade-in duration-300">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-6">
          <TextSection 
            icon="storefront" 
            iconColor="text-primary" 
            title={t('company_profile.title')} 
            content={qualData.business_description} 
          />
          <TextSection 
            icon="payments" 
            iconColor="text-tertiary" 
            title={t('company_profile.revenue_model')} 
            content={qualData.revenue_model} 
          />
          <TextSection 
            icon="explore" 
            iconColor="text-secondary" 
            title={t('thesis_view.strategy_title')} 
            content={qualData.strategy} 
          />
          
          <QualitySection qualityPillars={qualData.quality_pillars} />
        </div>

        <div className="space-y-6">
          <ProductsList products={qualData.products_services} />
        </div>
      </div>
    </div>
  );
}
