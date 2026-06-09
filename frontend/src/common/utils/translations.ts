import { t } from 'i18next';

export const translateSector = (value?: string): string => {
  if (!value) return '';
  return t(`sectors.${value.toLowerCase().replace(/ /g, '_')}`, { defaultValue: value });
};
