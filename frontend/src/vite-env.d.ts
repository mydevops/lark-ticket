/// <reference types="vite/client" />

declare type BizResponse<T = any> = {
  retcode: number;
  msg: string;
  resp: T;
  error: string;
};
