import { useTranslation } from 'react-i18next';

export function HomeHero() {
  const { t } = useTranslation();
  return (
    <>
      <div className="flex items-center gap-3 mb-8">
        <span className="material-symbols-outlined text-5xl text-primary drop-shadow-[0_0_15px_rgba(var(--color-primary),0.3)]">
          monitoring
        </span>
        <h1 className="font-display-lg text-4xl font-bold tracking-tight text-on-surface">
          {t('dashboard.empty_title')}
        </h1>
      </div>
      <p className="text-on-surface-variant text-body-lg mb-8 text-center max-w-lg">
        {t('dashboard.empty_desc')}
      </p>
    </>
  );
}
