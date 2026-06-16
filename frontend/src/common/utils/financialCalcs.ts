export function calcYoY(
  current: number | null | undefined,
  previous: number | null | undefined,
  isMargin = false
): number | null {
  if (current == null || previous == null || previous === 0) return null;
  if (isMargin) return current - previous;
  return ((current - previous) / Math.abs(previous)) * 100;
}
