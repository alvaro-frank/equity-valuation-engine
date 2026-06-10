import { t } from 'i18next';

export const translateSector = (value?: string): string => {
  if (!value) return '';
  const key = value.toLowerCase()
    .replace(/ /g, '_')
    .replace(/-/g, '_')
    .replace(/&/g, '')
    .replace(/,/g, '')
    .replace(/_+/g, '_')
    .replace(/^_|_$/g, '');
  return t(`sectors.${key}`, { defaultValue: value });
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
  return t(`industries.${key}`, { defaultValue: value });
};
