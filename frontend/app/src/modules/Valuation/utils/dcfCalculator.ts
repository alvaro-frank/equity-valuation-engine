import type { DCFAssumptions, DCFScenario } from '@/common/types/valuation';

/**
 * Calculates the DCF scenario mathematically in the browser, providing instant feedback.
 * Uses the exact same Gordon Growth Model logic as the backend.
 */
export const calculateDCFScenario = (
  assumptions: DCFAssumptions,
  baseFcf: number,
  sharesOutstanding: number,
  netCash: number,
  scenarioName: string = 'Custom'
): DCFScenario => {
  const { fcf_growth_1_to_5, fcf_growth_6_to_10, wacc, terminal_growth_rate } = assumptions;

  let pvFcfs = 0;
  let previousFcf = baseFcf;
  const projectedFcfs: number[] = [];

  // Years 1-5
  for (let i = 1; i <= 5; i++) {
    const fcf = previousFcf * (1 + fcf_growth_1_to_5);
    projectedFcfs.push(fcf);
    pvFcfs += fcf / Math.pow(1 + wacc, i);
    previousFcf = fcf;
  }

  // Years 6-10
  for (let i = 6; i <= 10; i++) {
    const fcf = previousFcf * (1 + fcf_growth_6_to_10);
    projectedFcfs.push(fcf);
    pvFcfs += fcf / Math.pow(1 + wacc, i);
    previousFcf = fcf;
  }

  // Terminal Value Calculation (Gordon Growth Model)
  const finalYearFcf = projectedFcfs[9];
  const terminalValue = (finalYearFcf * (1 + terminal_growth_rate)) / (wacc - terminal_growth_rate);
  const pvTerminalValue = terminalValue / Math.pow(1 + wacc, 10);

  const enterpriseValue = pvFcfs + pvTerminalValue;
  const equityValue = enterpriseValue + netCash;
  const intrinsicValuePerShare = equityValue / sharesOutstanding;

  return {
    scenario_name: scenarioName,
    assumptions,
    base_fcf: baseFcf,
    shares_outstanding: sharesOutstanding,
    net_cash: netCash,
    projected_fcfs: projectedFcfs,
    terminal_value: terminalValue,
    intrinsic_value_per_share: Number(intrinsicValuePerShare.toFixed(2)),
  };
};

/**
 * Generates a 5x5 sensitivity matrix grid.
 * Y-axis: WACC variations (-0.02, -0.01, 0, +0.01, +0.02)
 * X-axis: Terminal Growth variations (-0.01, -0.005, 0, +0.005, +0.01)
 */
export interface SensitivityPoint {
  wacc: number;
  terminal_growth: number;
  intrinsic_value: number;
}

export const generateSensitivityMatrix = (
  baseScenario: DCFScenario
): SensitivityPoint[][] => {
  const baseWacc = baseScenario.assumptions.wacc;
  const baseTerminalGrowth = baseScenario.assumptions.terminal_growth_rate;

  const waccVariations = [-0.02, -0.01, 0, 0.01, 0.02];
  const tgrVariations = [-0.01, -0.005, 0, 0.005, 0.01];

  const matrix: SensitivityPoint[][] = [];

  for (const waccDelta of waccVariations) {
    const row: SensitivityPoint[] = [];
    for (const tgrDelta of tgrVariations) {
      const testAssumptions = {
        ...baseScenario.assumptions,
        wacc: baseWacc + waccDelta,
        terminal_growth_rate: baseTerminalGrowth + tgrDelta,
      };

      const result = calculateDCFScenario(
        testAssumptions,
        baseScenario.base_fcf,
        baseScenario.shares_outstanding,
        baseScenario.net_cash,
        'Sensitivity'
      );

      row.push({
        wacc: testAssumptions.wacc,
        terminal_growth: testAssumptions.terminal_growth_rate,
        intrinsic_value: result.intrinsic_value_per_share,
      });
    }
    matrix.push(row);
  }

  return matrix;
};
