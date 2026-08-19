import { useState, useRef, useEffect } from 'react';
import { useTranslation } from 'react-i18next';

export function MethodDropdown() {
  const { t } = useTranslation();
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [selectedMethod, setSelectedMethod] = useState('dcf');
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsDropdownOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const methods = [
    { id: 'dcf', label: t('valuation.dcf_valuation', 'DCF Valuation') },
    { id: 'val1', label: t('valuation.val1', 'Valuation 1') },
    { id: 'val2', label: t('valuation.val2', 'Valuation 2') }
  ];

  const activeMethodLabel = methods.find(m => m.id === selectedMethod)?.label;

  return (
    <div className="relative mt-1" ref={dropdownRef}>
      <button 
        onClick={() => setIsDropdownOpen(!isDropdownOpen)}
        className="flex items-center gap-1 bg-primary/10 border border-primary/20 text-primary text-xs font-bold px-2 py-0.5 rounded uppercase tracking-wider hover:bg-primary/20 transition-colors"
      >
        {activeMethodLabel}
        <span className="material-symbols-outlined text-[14px]">arrow_drop_down</span>
      </button>
      
      {isDropdownOpen && (
        <div className="absolute top-full left-0 mt-1 bg-surface-container-high border border-outline-variant rounded shadow-lg z-50 min-w-[140px] overflow-hidden">
          {methods.map(method => (
            <button
              key={method.id}
              onClick={() => { setSelectedMethod(method.id); setIsDropdownOpen(false); }}
              className={`w-full text-left px-3 py-2 text-xs font-bold uppercase tracking-wider transition-colors ${selectedMethod === method.id ? 'bg-primary/10 text-primary' : 'text-on-surface hover:bg-surface-container-highest'}`}
            >
              {method.label}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
