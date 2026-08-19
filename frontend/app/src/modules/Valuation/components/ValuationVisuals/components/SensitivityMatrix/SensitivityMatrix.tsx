export interface SensitivityMatrixProps {
  matrix: {
    wacc: number;
    terminal_growth: number;
    intrinsic_value: number;
  }[][];
  currentPrice: number;
}

export function SensitivityMatrix({ matrix, currentPrice }: SensitivityMatrixProps) {
  if (!matrix || matrix.length === 0) return null;

  return (
    <div className="flex-1 flex items-stretch justify-center overflow-x-auto">
      <table className="w-full h-full border-collapse">
        <thead>
          <tr>
            <th className="p-4 border border-outline-variant bg-surface-container-highest text-sm text-on-surface-variant font-medium">
              WACC \ T.G.R.
            </th>
            {matrix[0].map((cell, i) => (
              <th key={i} className="p-4 border border-outline-variant bg-surface-container-highest text-base text-on-surface font-medium min-w-[100px]">
                {(cell.terminal_growth * 100).toFixed(1)}%
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {matrix.map((row, i) => (
            <tr key={i}>
              <td className="p-4 border border-outline-variant bg-surface-container-highest text-base text-on-surface font-medium text-center">
                {(row[0].wacc * 100).toFixed(1)}%
              </td>
              {row.map((cell, j) => {
                const safeCurrentPrice = Number(currentPrice) || 0;
                const margin = safeCurrentPrice > 0 ? ((cell.intrinsic_value - safeCurrentPrice) / safeCurrentPrice) * 100 : 0;
                const isUndervalued = margin > 0;
                // Calculate intensity (0 to 1) capping at 40% margin
                const intensity = Math.min(Math.abs(margin) / 40, 1);
                
                // We use inline styles for the heatmap effect
                const bgColor = isUndervalued 
                  ? `rgba(76, 175, 80, ${0.1 + intensity * 0.4})` // Green shades
                  : `rgba(244, 67, 54, ${0.1 + intensity * 0.4})`; // Red shades

                return (
                  <td 
                    key={j} 
                    style={{ backgroundColor: bgColor }}
                    className="p-4 border border-outline-variant text-center text-lg font-medium text-on-surface transition-colors duration-300"
                  >
                    ${cell.intrinsic_value.toFixed(2)}
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
