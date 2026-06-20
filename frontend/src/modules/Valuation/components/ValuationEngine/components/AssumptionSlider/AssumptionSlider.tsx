export interface AssumptionSliderProps {
  label: string;
  min: number;
  max: number;
  step: number;
  value: number;
  onChange: (val: number) => void;
  isPercentage?: boolean;
  tooltipText?: string;
  isEditable?: boolean;
}

export function AssumptionSlider({
  label,
  min,
  max,
  step,
  value,
  onChange,
  isPercentage = true,
  tooltipText,
  isEditable = true
}: AssumptionSliderProps) {
  const displayValue = isPercentage ? `${(value * 100).toFixed(1)}%` : value.toString();

  return (
    <div className="flex flex-col gap-2 mb-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-1.5 group relative">
          <label className={`text-label-md font-medium text-on-surface ${!isEditable ? 'opacity-60' : ''}`}>{label}</label>
          {tooltipText && (
            <div className="relative flex items-center">
              <span className={`material-symbols-outlined text-[16px] text-on-surface-variant cursor-help transition-opacity ${!isEditable ? 'opacity-60 group-hover:opacity-100' : ''}`}>info</span>
              <div className="absolute left-1/2 -translate-x-1/2 bottom-full mb-2 w-48 p-2 bg-surface-container-highest border border-outline-variant text-on-surface text-xs rounded-md shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all pointer-events-none z-50 text-center font-normal leading-relaxed">
                {tooltipText}
                <div className="absolute left-1/2 -translate-x-1/2 top-full w-0 h-0 border-l-[5px] border-r-[5px] border-t-[5px] border-transparent border-t-outline-variant"></div>
                <div className="absolute left-1/2 -translate-x-1/2 top-[calc(100%-1px)] w-0 h-0 border-l-[4px] border-r-[4px] border-t-[4px] border-transparent border-t-surface-container-highest"></div>
              </div>
            </div>
          )}
        </div>
        <span className={`text-label-md text-primary font-bold bg-primary/10 px-2 py-0.5 rounded ${!isEditable ? 'opacity-60' : ''}`}>
          {displayValue}
        </span>
      </div>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => onChange(parseFloat(e.target.value))}
        disabled={!isEditable}
        className={`w-full h-2 bg-surface-container-highest rounded-lg appearance-none ${
          isEditable ? 'cursor-pointer accent-primary' : 'cursor-not-allowed accent-outline opacity-60'
        }`}
      />
    </div>
  );
}
