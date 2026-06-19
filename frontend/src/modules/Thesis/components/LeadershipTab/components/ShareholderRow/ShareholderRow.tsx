interface ShareholderRowProps {
  investor: string;
  pct: number;
}

export function ShareholderRow({ investor, pct }: ShareholderRowProps) {
  return (
    <div className="flex items-center justify-between p-3 bg-surface-container-lowest border border-outline-variant/50 rounded-lg">
      <span className="text-sm text-on-surface-variant font-medium line-clamp-1 pr-2">{investor}</span>
      <span className="text-sm font-mono text-on-surface font-bold bg-surface-container-high px-2 py-0.5 rounded border border-outline-variant/50 shrink-0">
        {Number(pct).toFixed(2)}%
      </span>
    </div>
  );
}
