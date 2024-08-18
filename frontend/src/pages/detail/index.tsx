import Main from '@/components/Main';
import { Card } from 'antd';
import { Link } from 'react-router-dom';
import { RollbackOutlined } from '@ant-design/icons';
import Form from './Form';

const Index = () => {
  return (
    <Main>
      <Card
        extra={
          <Link className="text-gray-900" to="/home">
            返回
            <RollbackOutlined className="ml-2" />
          </Link>
        }
      >
        <Form />
      </Card>
    </Main>
  );
};

export default Index;
