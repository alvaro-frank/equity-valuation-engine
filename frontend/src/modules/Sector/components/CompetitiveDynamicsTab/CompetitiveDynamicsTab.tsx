import { useTranslation } from 'react-i18next';

interface CompetitiveDynamicsTabProps {
  sectorData: any;
}

export function CompetitiveDynamicsTab({ sectorData }: CompetitiveDynamicsTabProps) {
  const { t } = useTranslation();

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-in slide-in-from-bottom-4 duration-500">
      {/* Rivalry */}
      <div className="bg-surface-container border border-outline-variant p-6 rounded flex flex-col gap-4">
        <div className="flex items-center gap-3 pb-3 border-b border-outline-variant">
          <span className="material-symbols-outlined text-primary text-[28px]">swords</span>
          <h3 className="font-display-sm text-xl text-on-surface">{t('sector_view.rivalry')}</h3>
        </div>
        <div className="space-y-4">
          {Object.entries(sectorData.rivalry_among_competitors).map(([factor, analysis]) => (
            <div key={factor}>
              <p className="text-on-surface font-semibold text-sm mb-1">{factor}</p>
              <p className="text-on-surface-variant text-sm leading-relaxed">{analysis as string}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Threat of New Entrants */}
      <div className="bg-surface-container border border-outline-variant p-6 rounded flex flex-col gap-4">
        <div className="flex items-center gap-3 pb-3 border-b border-outline-variant">
          <span className="material-symbols-outlined text-primary text-[28px]">shield</span>
          <h3 className="font-display-sm text-xl text-on-surface">{t('sector_view.new_entrants')}</h3>
        </div>
        <div className="space-y-4">
          {Object.entries(sectorData.threat_of_new_entrants).map(([factor, analysis]) => (
            <div key={factor}>
              <p className="text-on-surface font-semibold text-sm mb-1">{factor}</p>
              <p className="text-on-surface-variant text-sm leading-relaxed">{analysis as string}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Obsolescence */}
      <div className="bg-surface-container border border-outline-variant p-6 rounded flex flex-col gap-4">
        <div className="flex items-center gap-3 pb-3 border-b border-outline-variant">
          <span className="material-symbols-outlined text-primary text-[28px]">hourglass_empty</span>
          <h3 className="font-display-sm text-xl text-on-surface">{t('sector_view.obsolescence')}</h3>
        </div>
        <div className="space-y-4">
          {Object.entries(sectorData.threat_of_obsolescence).map(([factor, analysis]) => (
            <div key={factor}>
              <p className="text-on-surface font-semibold text-sm mb-1">{factor}</p>
              <p className="text-on-surface-variant text-sm leading-relaxed">{analysis as string}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Suppliers */}
      <div className="bg-surface-container border border-outline-variant p-6 rounded flex flex-col gap-4">
        <div className="flex items-center gap-3 pb-3 border-b border-outline-variant">
          <span className="material-symbols-outlined text-primary text-[28px]">inventory</span>
          <h3 className="font-display-sm text-xl text-on-surface">{t('sector_view.suppliers')}</h3>
        </div>
        <div className="space-y-4">
          {Object.entries(sectorData.bargaining_power_of_suppliers).map(([factor, analysis]) => (
            <div key={factor}>
              <p className="text-on-surface font-semibold text-sm mb-1">{factor}</p>
              <p className="text-on-surface-variant text-sm leading-relaxed">{analysis as string}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Customers */}
      <div className="bg-surface-container border border-outline-variant p-6 rounded flex flex-col gap-4 md:col-span-2 lg:col-span-1">
        <div className="flex items-center gap-3 pb-3 border-b border-outline-variant">
          <span className="material-symbols-outlined text-primary text-[28px]">shopping_cart</span>
          <h3 className="font-display-sm text-xl text-on-surface">{t('sector_view.customers')}</h3>
        </div>
        <div className="space-y-4">
          {Object.entries(sectorData.bargaining_power_of_customers).map(([factor, analysis]) => (
            <div key={factor}>
              <p className="text-on-surface font-semibold text-sm mb-1">{factor}</p>
              <p className="text-on-surface-variant text-sm leading-relaxed">{analysis as string}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
