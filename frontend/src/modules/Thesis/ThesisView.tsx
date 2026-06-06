import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useQualitativeData } from '@/modules/Valuation/hooks/useValuationData';
import { MoatRadarChart } from './components/MoatRadarChart';
import { QualityStarRating } from './components/QualityStarRating';

interface ThesisViewProps {
  ticker: string;
}

export function ThesisView({ ticker }: ThesisViewProps) {
  const { t } = useTranslation();
  const { data: qualData, isLoading, error, refetch } = useQualitativeData(ticker);
  
  const [activeSubTab, setActiveSubTab] = useState<'overview' | 'moat' | 'leadership' | 'history' | 'risks'>('overview');

  const subTabs = [
    { id: 'overview', label: t('thesis_view.tab_overview'), icon: 'lightbulb' },
    { id: 'moat', label: t('thesis_view.tab_moat'), icon: 'security' },
    { id: 'leadership', label: t('thesis_view.tab_leadership'), icon: 'groups' },
    { id: 'history', label: t('thesis_view.tab_history'), icon: 'history' },
    { id: 'risks', label: t('thesis_view.tab_risks'), icon: 'warning' }
  ] as const;

  if (isLoading) {
    return (
      <div className="max-w-[1200px] mx-auto space-y-panel-gap animate-in fade-in duration-500">
        <div className="h-12 bg-surface-container-high rounded animate-pulse w-full max-w-2xl mb-8"></div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="md:col-span-2 space-y-6">
            <div className="h-64 bg-surface-container-high rounded border border-outline-variant animate-pulse"></div>
            <div className="h-48 bg-surface-container-high rounded border border-outline-variant animate-pulse"></div>
          </div>
          <div className="space-y-6">
            <div className="h-48 bg-surface-container-high rounded border border-outline-variant animate-pulse"></div>
            <div className="h-64 bg-surface-container-high rounded border border-outline-variant animate-pulse"></div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh] text-center px-4">
        <div className="w-16 h-16 bg-error/10 border border-error/20 rounded-full flex items-center justify-center mb-4">
          <span className="material-symbols-outlined text-[32px] text-error">error</span>
        </div>
        <h2 className="font-display-sm text-display-sm font-bold text-on-surface mb-2">
          Unable to generate Investment Thesis
        </h2>
        <p className="text-body-md text-on-surface-variant max-w-md mb-6 leading-relaxed">
          {error.message || "An error occurred while evaluating the qualitative aspects of this business."}
        </p>
        <button 
          onClick={() => refetch()}
          className="flex items-center gap-2 px-6 py-2 bg-surface-container-highest border border-outline-variant hover:border-outline text-on-surface rounded-full transition-colors font-medium"
        >
          <span className="material-symbols-outlined text-[18px]">refresh</span>
          {t('dashboard.try_again')}
        </button>
      </div>
    );
  }

  if (!qualData) return null;

  return (
    <div className="max-w-[1400px] mx-auto pb-12 animate-in fade-in duration-500">
      
      {/* Header */}
      <div className="flex items-end justify-between px-2 pt-2 pb-6 border-b border-outline-variant mb-6">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="font-display-md text-display-md text-on-surface">{qualData.ticker.name || ticker}</h1>
            <span className="bg-primary/10 border border-primary/20 text-primary text-xs font-bold px-2 py-0.5 rounded uppercase tracking-wider">
              {t('nav.thesis')}
            </span>
          </div>
          <p className="text-body-sm text-on-surface-variant mt-1.5 flex items-center gap-2">
            <span className="material-symbols-outlined text-[16px]">domain</span>
            {qualData.ticker.sector} / {qualData.ticker.industry}
          </p>
        </div>
      </div>

      {/* Internal Sub-Navigation */}
      <nav className="flex items-center gap-2 mb-8 overflow-x-auto pb-2 custom-scrollbar">
        {subTabs.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveSubTab(tab.id)}
            className={`flex items-center gap-2 px-4 py-2.5 rounded-lg text-sm font-medium transition-all whitespace-nowrap ${
              activeSubTab === tab.id 
                ? 'bg-secondary-container text-on-secondary-container shadow-sm border border-secondary-container/50' 
                : 'text-on-surface-variant hover:text-on-surface hover:bg-surface-container-high border border-transparent'
            }`}
          >
            <span className="material-symbols-outlined text-[18px]">{tab.icon}</span>
            {tab.label}
          </button>
        ))}
      </nav>

      {/* Content Area */}
      <div className="bg-surface-container-low border border-outline-variant rounded-xl p-6 min-h-[500px]">
        
        {/* TAB: OVERVIEW & STRATEGY */}
        {activeSubTab === 'overview' && (
          <div className="space-y-8 animate-in slide-in-from-right-4 fade-in duration-300">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              <div className="lg:col-span-2 space-y-6">
                <div>
                  <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-3 flex items-center gap-2">
                    <span className="material-symbols-outlined text-primary">storefront</span>
                    {t('company_profile.title')}
                  </h3>
                  <div className="prose prose-sm dark:prose-invert max-w-none text-on-surface-variant leading-relaxed bg-surface-container-lowest p-5 rounded-lg border border-outline-variant/50">
                    <p>{qualData.business_description}</p>
                  </div>
                </div>

                <div>
                  <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-3 flex items-center gap-2">
                    <span className="material-symbols-outlined text-tertiary">payments</span>
                    {t('company_profile.revenue_model')}
                  </h3>
                  <div className="bg-tertiary/10 border border-tertiary/20 p-5 rounded-lg">
                    <p className="text-body-sm text-on-surface-variant leading-relaxed">{qualData.revenue_model}</p>
                  </div>
                </div>

                <div>
                  <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-3 flex items-center gap-2">
                    <span className="material-symbols-outlined text-secondary">explore</span>
                    {t('thesis_view.strategy_title')}
                  </h3>
                  <div className="prose prose-sm dark:prose-invert max-w-none text-on-surface-variant leading-relaxed bg-surface-container-lowest p-5 rounded-lg border border-outline-variant/50">
                    <p>{qualData.strategy}</p>
                  </div>
                </div>
              </div>

              <div className="space-y-6">
                {qualData.quality_pillars && (
                  <QualityStarRating data={qualData.quality_pillars} />
                )}

                <div>
                  <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-3 flex items-center gap-2">
                    <span className="material-symbols-outlined text-on-surface-variant">category</span>
                    {t('thesis_view.products_title')}
                  </h3>
                  <div className="space-y-3">
                    {Object.entries(qualData.products_services).map(([product, desc]) => (
                      <div key={product} className="bg-surface-container-lowest p-4 rounded-lg border border-outline-variant/50 hover:border-outline-variant transition-colors group">
                        <h4 className="font-bold text-on-surface text-sm mb-1 group-hover:text-primary transition-colors">{product}</h4>
                        <p className="text-xs text-on-surface-variant leading-relaxed">{desc}</p>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* TAB: MOAT & RIVALS */}
        {activeSubTab === 'moat' && (
          <div className="space-y-8 animate-in slide-in-from-right-4 fade-in duration-300">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <div className="space-y-6">
                <div>
                  <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-3 flex items-center gap-2">
                    <span className="material-symbols-outlined text-primary">fort</span>
                    {t('thesis_view.moat_title')}
                  </h3>
                  <div className="grid grid-cols-1 2xl:grid-cols-2 gap-6 bg-surface-container-lowest p-6 rounded-lg border border-outline-variant/50 items-center">
                    <div className="prose prose-sm dark:prose-invert max-w-none text-on-surface-variant leading-relaxed">
                      <p>{qualData.competitive_advantage}</p>
                    </div>
                    {qualData.moat_sources && (
                      <MoatRadarChart data={qualData.moat_sources} />
                    )}
                  </div>
                </div>

                <div>
                  <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-3 flex items-center gap-2">
                    <span className="material-symbols-outlined text-tertiary">trending_up</span>
                    {t('thesis_view.moat_trajectory')}
                  </h3>
                  <div className="prose prose-sm dark:prose-invert max-w-none text-on-surface-variant leading-relaxed bg-tertiary/5 p-6 rounded-lg border border-tertiary/20">
                    <p>{qualData.moat_trajectory || t('thesis_view.no_data')}</p>
                  </div>
                </div>
              </div>

              <div>
                <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-3 flex items-center gap-2">
                  <span className="material-symbols-outlined text-error">swords</span>
                  {t('thesis_view.competitors_title')}
                </h3>
                <div className="grid grid-cols-1 gap-3">
                  {Object.entries(qualData.competitors).map(([competitor, overlap]) => (
                    <div key={competitor} className="bg-surface-container-lowest p-4 rounded-lg border border-outline-variant/50 hover:border-outline-variant transition-all hover:shadow-sm">
                      <div className="flex items-center gap-3 mb-2">
                        <div className="w-8 h-8 bg-surface-container-high rounded-full flex items-center justify-center border border-outline-variant shrink-0">
                          <span className="material-symbols-outlined text-[16px] text-on-surface-variant">corporate_fare</span>
                        </div>
                        <h4 className="font-bold text-on-surface text-sm">{competitor}</h4>
                      </div>
                      <p className="text-xs text-on-surface-variant leading-relaxed pl-11">{overlap}</p>
                    </div>
                  ))}
                  {Object.keys(qualData.competitors).length === 0 && (
                    <p className="text-sm text-on-surface-variant italic p-4">{t('thesis_view.no_data')}</p>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* TAB: LEADERSHIP & OWNERSHIP */}
        {activeSubTab === 'leadership' && (
          <div className="space-y-8 animate-in slide-in-from-right-4 fade-in duration-300">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              <div className="lg:col-span-1 space-y-6">
                
                <div className="bg-surface-container-lowest border border-outline-variant/50 rounded-xl overflow-hidden">
                  <div className="bg-surface-container-high p-4 border-b border-outline-variant/50 flex flex-col items-center text-center">
                    <div className="w-20 h-20 bg-primary/10 rounded-full flex items-center justify-center mb-3 border border-primary/20">
                      <span className="material-symbols-outlined text-[32px] text-primary">person</span>
                    </div>
                    <h3 className="font-bold text-on-surface text-lg">{qualData.ceo_name}</h3>
                    <p className="text-xs text-on-surface-variant uppercase tracking-wider">{t('company_header.ceo')}</p>
                  </div>
                  <div className="p-4 flex items-center justify-between bg-primary/5">
                    <span className="text-sm text-on-surface font-medium">Skin in the Game:</span>
                    <span className="bg-primary text-on-primary text-xs font-bold px-2.5 py-1 rounded">
                      {Number(qualData.ceo_ownership) < 0.1 ? Number(qualData.ceo_ownership).toFixed(2) : Number(qualData.ceo_ownership).toFixed(1)}% {t('dashboard.owned')}
                    </span>
                  </div>
                </div>

                <div>
                  <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-3 flex items-center gap-2">
                    <span className="material-symbols-outlined text-secondary">pie_chart</span>
                    {t('thesis_view.shareholders_title')}
                  </h3>
                  <div className="space-y-2">
                    {Object.entries(qualData.major_shareholders).map(([investor, pct]) => (
                      <div key={investor} className="flex items-center justify-between p-3 bg-surface-container-lowest border border-outline-variant/50 rounded-lg">
                        <span className="text-sm text-on-surface-variant font-medium line-clamp-1 pr-2">{investor}</span>
                        <span className="text-sm font-mono text-on-surface font-bold bg-surface-container-high px-2 py-0.5 rounded border border-outline-variant/50 shrink-0">
                          {Number(pct).toFixed(2)}%
                        </span>
                      </div>
                    ))}
                    {Object.keys(qualData.major_shareholders).length === 0 && (
                      <p className="text-sm text-on-surface-variant italic p-4">{t('thesis_view.no_data')}</p>
                    )}
                  </div>
                </div>

              </div>

              <div className="lg:col-span-2">
                <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-3 flex items-center gap-2">
                  <span className="material-symbols-outlined text-primary">insights</span>
                  {t('thesis_view.leadership_title')}
                </h3>
                <div className="prose prose-sm dark:prose-invert max-w-none text-on-surface-variant leading-relaxed bg-surface-container-lowest p-6 rounded-lg border border-outline-variant/50 min-h-[400px]">
                  <p>{qualData.management_insights}</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* TAB: HISTORY & CRISES */}
        {activeSubTab === 'history' && (
          <div className="space-y-8 animate-in slide-in-from-right-4 fade-in duration-300">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <div>
                <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-3 flex items-center gap-2">
                  <span className="material-symbols-outlined text-primary">history_edu</span>
                  {t('thesis_view.history_title')}
                </h3>
                <div className="prose prose-sm dark:prose-invert max-w-none text-on-surface-variant leading-relaxed bg-surface-container-lowest p-6 rounded-lg border border-outline-variant/50 h-[calc(100%-40px)]">
                  <p>{qualData.company_history || t('thesis_view.no_data')}</p>
                </div>
              </div>

              <div>
                <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-3 flex items-center gap-2">
                  <span className="material-symbols-outlined text-error">tsunami</span>
                  {t('thesis_view.crises_title')}
                </h3>
                <div className="prose prose-sm dark:prose-invert max-w-none text-on-surface-variant leading-relaxed bg-error/5 p-6 rounded-lg border border-error/20 h-[calc(100%-40px)]">
                  <p>{qualData.historical_context_crises}</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* TAB: RISKS */}
        {activeSubTab === 'risks' && (
          <div className="space-y-6 animate-in slide-in-from-right-4 fade-in duration-300">
            <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-4 flex items-center gap-2">
              <span className="material-symbols-outlined text-error">warning</span>
              {t('thesis_view.risks_title')}
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {Object.entries(qualData.risk_factors).map(([risk, description], index) => (
                <div key={risk} className="bg-surface-container-lowest p-5 rounded-xl border border-outline-variant/50 hover:border-error/30 transition-colors flex gap-4 group">
                  <div className="w-10 h-10 rounded-full bg-error/10 flex items-center justify-center shrink-0 border border-error/20 group-hover:bg-error/20 transition-colors">
                    <span className="font-bold text-error">{index + 1}</span>
                  </div>
                  <div>
                    <h4 className="font-bold text-on-surface text-base mb-2 group-hover:text-error transition-colors">{risk}</h4>
                    <p className="text-sm text-on-surface-variant leading-relaxed">{description}</p>
                  </div>
                </div>
              ))}
              {Object.keys(qualData.risk_factors).length === 0 && (
                <p className="text-sm text-on-surface-variant italic p-4 col-span-2">{t('thesis_view.no_data')}</p>
              )}
            </div>
          </div>
        )}

      </div>
    </div>
  );
}
