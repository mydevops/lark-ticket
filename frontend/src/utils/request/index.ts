export const enum HTTP_STATUS {
  OK = 200,
  CREATED = 201,
  NO_CONTENT = 204,
  BAD_REQUEST = 400,
  UNAUTHORIZED = 401,
  FORBIDDEN = 403,
  NOT_FOUND = 404,
  METHOD_NOT_ALLOWED = 405,
  INTERNAL_SERVER_ERROR = 500,
}

export const enum HTTP_SERVICE_CODE {
  Success = 0,
  NormalError = 20001,
}

type Config = {
  method?: string;
  requestContentType?: 'form' | 'json';
  headers?: Record<string, any>;
  data?: Record<string, any>;
  rawData?: 'json';
};
export const request = async (url: string, config?: Config): Promise<any> => {
  const {
    data = {},
    requestContentType,
    method,
    ...reset
  } = {
    method: 'POST',
    requestContentType: 'json',
    ...config,
  };
  if (method.toUpperCase() === 'GET' && data) {
    const params = new URLSearchParams(data);
    const response = await fetch(`${url}?${params}`, {
      ...reset,
    });
    return response;
  }

  let configData: string | FormData | null = data ? JSON.stringify(data) : null;

  if (data && requestContentType === 'form') {
    const formData = new FormData();
    for (const key in data) {
      formData.append(key, data[key]);
    }
    configData = formData;
  }
  const response = await fetch(url, {
    method,
    ...reset,
    ...(configData && {
      body: configData,
    }),
  });
  return response;
};

export const baseRequest = async <T = any>(
  url: string,
  config?: Config,
): Promise<BizResponse<T>> => {
  const response = await request(url, config);
  if (!response.ok) {
    return Promise.reject(response);
  }
  const resJson = await response.json();
  return resJson;
};

const publicPath = '/api/v1/web';

export const localRequest = async <T = any>(url: string, config?: Config) => {
  const requestUrl = /^(https?:\/\/)/.test(url) ? url : publicPath + url;
  return baseRequest<T>(requestUrl, config);
};
