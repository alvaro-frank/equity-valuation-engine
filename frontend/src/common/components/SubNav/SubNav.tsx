export interface SubNavTab {
  id: string;
  label: string;
  icon: string;
}

interface SubNavProps {
  tabs: SubNavTab[];
  activeTabId: string;
  onTabChange: (id: string) => void;
}

export function SubNav({ tabs, activeTabId, onTabChange }: SubNavProps) {
  return (
    <nav className="flex items-center gap-2 mb-8 overflow-x-auto pb-2 custom-scrollbar">
      {tabs.map(tab => (
        <button
          key={tab.id}
          onClick={() => onTabChange(tab.id)}
          className={`flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium transition-all whitespace-nowrap
            ${activeTabId === tab.id 
              ? 'bg-primary text-on-primary shadow-sm' 
              : 'bg-surface-container border border-outline-variant text-on-surface-variant hover:bg-surface-container-high hover:text-on-surface'
            }`}
        >
          <span className="material-symbols-outlined text-[18px]">{tab.icon}</span>
          {tab.label}
        </button>
      ))}
    </nav>
  );
}
