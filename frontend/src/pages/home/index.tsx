import Main from '@/components/Main';
import { Table, Card, message, Button, Popconfirm } from 'antd';
import { useRequest } from 'ahooks';
import { Link } from 'react-router-dom';
import type { TableProps } from 'antd';
import { localRequest, HTTP_SERVICE_CODE } from '@/utils/request';

interface TableListItem {
  approval_code: string;
  name: string;
}

const Home = () => {
  const [messageApi, contextHandler] = message.useMessage();

  // 获取列表
  const { run, data, loading } = useRequest(async () => {
    const res = await localRequest<{ body: TableListItem[] }>('/configs', { method: 'GET' });
    if (res.retcode !== HTTP_SERVICE_CODE.Success) {
      messageApi.error(res.error);
      return;
    }
    return res.resp.body;
  });

  // 删除
  const deleteItem = async (approval_code: string) => {
    const response = await localRequest(`/config/${approval_code}`, {
      method: 'DELETE',
    });
    console.log(response);
    if (response.retcode !== HTTP_SERVICE_CODE.Success) {
      messageApi.error(response.error);
      return;
    }
    messageApi.success('删除成功');
    run();
  };

  const columns: TableProps<TableListItem>['columns'] = [
    {
      title: '审批配置名称',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '审批定义 code',
      dataIndex: 'approval_code',
      key: 'approval_code',
    },
    {
      title: '操作',
      key: 'action',
      width: 300,
      render: (_, record) => (
        <>
          <Button type="link">
            <Link to={`/detail?type=search&approval_code=${record.approval_code}`}>详情</Link>
          </Button>
          <Button type="link">
            <Link to={`/detail?type=edit&approval_code=${record.approval_code}`}>编辑</Link>
          </Button>
          <Popconfirm
            title="确定删除该审批配置吗?"
            onConfirm={() => deleteItem(record.approval_code)}
            okText="Yes"
            cancelText="No"
          >
            <Button type="link" danger>
              删除
            </Button>
          </Popconfirm>
        </>
      ),
    },
  ];

  return (
    <Main>
      {contextHandler}
      <Card
        extra={
          <Button type="primary">
            <Link to={`/detail`}>新增审批配置</Link>
          </Button>
        }
      >
        <Table
          rowKey="approval_code"
          loading={loading}
          dataSource={data}
          bordered
          columns={columns}
          pagination={false}
        />
      </Card>
    </Main>
  );
};

export default Home;
