import { Spin } from 'antd';
const styles = {
  width: '100%',
  height: '100%',
  minHeight: '400px',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
};

const Loading = () => {
  return (
    <div style={styles}>
      <Spin size="large" />
    </div>
  );
};

export default Loading;
