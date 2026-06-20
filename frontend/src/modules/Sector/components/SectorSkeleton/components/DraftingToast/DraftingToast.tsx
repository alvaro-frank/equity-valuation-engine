export interface DraftingToastProps {
  language: string;
}

export function DraftingToast({ language }: DraftingToastProps) {
  return (
    <div className="fixed bottom-6 right-6 z-50 bg-surface-container-highest border border-outline-variant px-4 py-3 rounded shadow-lg flex items-center gap-3 animate-bounce shadow-[0_4px_20px_rgba(0,0,0,0.4)]">
      <div className="animate-spin rounded-full h-4 w-4 border-t-2 border-b-2 border-primary"></div>
      <span className="text-on-surface font-medium text-sm animate-pulse">
        {language === 'pt' ? 'A redigir Análise Setorial...' : 'Drafting Sector Analysis...'}
      </span>
    </div>
  );
}
