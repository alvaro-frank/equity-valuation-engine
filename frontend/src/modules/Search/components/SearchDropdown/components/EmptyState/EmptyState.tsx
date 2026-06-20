interface EmptyStateProps {
  searchTerm: string;
}

export function EmptyState({ searchTerm }: EmptyStateProps) {
  return (
    <div className="px-4 py-4 text-sm text-on-surface-variant flex items-center gap-2">
      <span className="material-symbols-outlined text-[16px]">search_off</span>
      No tickers found matching "{searchTerm}"
    </div>
  );
}
