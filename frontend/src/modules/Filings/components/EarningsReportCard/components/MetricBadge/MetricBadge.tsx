export function MetricBadge({ value, isMargin }: { value: number | string | null | undefined, isMargin?: boolean }) {
  if (value == null) return null;
  const numValue = Number(value);
  const isPositive = numValue >= 0;
  return (
    <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded ml-2 ${isPositive ? 'bg-secondary/10 text-secondary' : 'bg-error/10 text-error'}`}>
      {isPositive ? '+' : ''}{numValue.toFixed(1)}{isMargin ? ' pp YoY' : '% YoY'}
    </span>
  );
}
