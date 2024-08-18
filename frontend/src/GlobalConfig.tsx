import { ConfigProvider } from 'antd';
import { PropsWithChildren } from 'react';

export function GlobalConfig({ children }: PropsWithChildren) {
  return (
    <ConfigProvider
      theme={{
        components: {
          Menu: {},
        },
      }}
    >
      {children}
    </ConfigProvider>
  );
}
