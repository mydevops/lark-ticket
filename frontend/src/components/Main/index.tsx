import React from 'react';
type MainProps = {
  children: React.ReactNode;
};
const Main = ({ children }: MainProps) => {
  return <div className="w-11/12 mx-auto mt-6">{children}</div>;
};

export default Main;
