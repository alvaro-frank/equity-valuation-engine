import { t } from 'i18next';

const formatDefault = (val: string): string => {
  return val
    .split(/[-_]/)
    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ');
};

export const translateSector = (value?: string): string => {
  if (!value) return '';
  const key = value.toLowerCase()
    .replace(/ /g, '_')
    .replace(/-/g, '_')
    .replace(/&/g, '')
    .replace(/,/g, '')
    .replace(/_+/g, '_')
    .replace(/^_|_$/g, '');
  return t(`sectors.${key}`, { defaultValue: formatDefault(value) });
};

export const translateIndustry = (value?: string): string => {
  if (!value) return '';
  const key = value.toLowerCase()
    .replace(/ /g, '_')
    .replace(/-/g, '_')
    .replace(/&/g, '')
    .replace(/,/g, '')
    .replace(/_+/g, '_')
    .replace(/^_|_$/g, '');
  return t(`industries.${key}`, { defaultValue: formatDefault(value) });
};
