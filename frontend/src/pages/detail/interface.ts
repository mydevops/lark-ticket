export interface IFormField {
  approval_code: string;
  name: string;
  check: {
    call_type: 'sync' | 'async';
    is_open: boolean;
    url: string;
  };
  execute: {
    call_type: 'sync' | 'async';
    is_open: boolean;
    url: string;
  };
  field: {
    is_open: boolean;
    data: {
      code: string;
      url: string;
    }[];
  };
  relation: {
    is_open: boolean;
    data: {
      api_key: string;
      code: string;
    }[];
  };
}

export interface IFieldItem {
  label: string;
  value: string;
}
