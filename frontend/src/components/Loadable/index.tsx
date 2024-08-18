import { Suspense } from 'react';
import ILoading from '../ILoading';

const Loadable = (Component: any) => (props: any) =>
  (
    <Suspense fallback={<ILoading />}>
      <Component {...props} />
    </Suspense>
  );

export default Loadable;
