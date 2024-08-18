import { useRoutes } from 'react-router-dom';
import { lazy } from 'react';
import Loadable from '@/components/Loadable';
import Layout from '@/layouts/index';

/** 主页 */
const Home = Loadable(lazy(() => import('@/pages/home')));

/** 详情 */
const Detail = Loadable(lazy(() => import('@/pages/detail')));

const routes = [
  {
    path: '/',
    element: <Layout />,
    children: [
      { path: '/', element: <Home /> },
      { path: '/home', element: <Home /> },
      { path: '/detail', element: <Detail /> },
      // 可以写404页面
      { path: '*', element: '404 Not Found' },
    ],
  },
];

export default function ThemeRoutes() {
  return useRoutes(routes);
}
