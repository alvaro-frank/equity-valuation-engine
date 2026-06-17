export function calcYoY(
  current: number | null | undefined,
  previous: number | null | undefined,
  isMargin = false
): number | null {
  if (current == null || previous == null) return null;
  const numCurrent = Number(current);
  const numPrevious = Number(previous);
  
  if (numPrevious === 0) return null;
  if (isMargin) return numCurrent - numPrevious;
  return ((numCurrent - numPrevious) / Math.abs(numPrevious)) * 100;
}
