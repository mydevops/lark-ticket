import { Outlet } from 'react-router-dom';
import { Layout } from 'antd';
import { GlobalConfig } from '../GlobalConfig';

export default function RootLayout() {
  return (
    <GlobalConfig>
      <Layout style={{ minHeight: '100vh', background: '#fff' }}>
        <Outlet />
      </Layout>
    </GlobalConfig>
  );
}
