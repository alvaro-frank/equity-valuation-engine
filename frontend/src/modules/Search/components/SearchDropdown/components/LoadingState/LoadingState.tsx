export function LoadingState() {
  return (
    <div className="px-4 py-4 text-sm text-on-surface-variant flex items-center gap-2">
      <span className="material-symbols-outlined animate-spin text-[16px]">progress_activity</span>
      Searching tickers...
    </div>
  );
}
