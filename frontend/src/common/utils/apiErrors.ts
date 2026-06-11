export interface ApiErrorDetails {
  key: number | string;
  details: {
    title: string;
    message: string;
    icon: string;
  };
  rawMessage?: string;
  ticker?: string;
}

export interface ApiError extends Error {
  response?: {
    status?: number;
    data?: { detail?: string };
  };
}

export const getErrorDetails = (key: number | string, t: (key: string) => string) => {
  const map: Record<number | string, { title: string, message: string, icon: string }> = {
    404: {
      title: t('api_errors.404_title'),
      message: t('api_errors.404_desc'),
      icon: "search_off"
    },
    429: {
      title: t('api_errors.429_title'),
      message: t('api_errors.429_desc'),
      icon: "hourglass_empty"
    },
    503: {
      title: t('api_errors.503_title'),
      message: t('api_errors.503_desc'),
      icon: "engineering"
    },
    DEFAULT: {
      title: t('api_errors.default_title'),
      message: t('api_errors.default_desc'),
      icon: "error_outline"
    }
  };
  return map[key] || map['DEFAULT'];
};

export const parseApiError = (error: unknown, t: (key: string) => string, ticker?: string): ApiErrorDetails => {
  const getStatusCode = (err: unknown) => (err as ApiError)?.response?.status;
  const statusCode = getStatusCode(error);
  const apiErrorMsg = (error as ApiError)?.response?.data?.detail || (error as ApiError)?.message || '';
  
  let errorKey: number | string = 'DEFAULT';
  
  if (statusCode === 404) errorKey = 404;
  else if (statusCode === 429 || apiErrorMsg.includes('429') || apiErrorMsg.includes('RESOURCE_EXHAUSTED') || apiErrorMsg.toLowerCase().includes('quota')) errorKey = 429;
  else if (statusCode === 503 || apiErrorMsg.includes('503') || apiErrorMsg.includes('UNAVAILABLE') || apiErrorMsg.includes('high demand')) errorKey = 503;

  return {
    key: errorKey,
    details: getErrorDetails(errorKey, t),
    rawMessage: apiErrorMsg,
    ticker
  };
};
