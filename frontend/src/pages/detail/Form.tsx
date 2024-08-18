import { message, Form, Input, Divider, Radio, Button, Space, Select } from 'antd';
import { useEffect, useState } from 'react';
import type { IFormField, IFieldItem } from './interface';
import { useLocation, useNavigate } from 'react-router-dom';
import { MinusCircleOutlined, PlusOutlined } from '@ant-design/icons';
import { localRequest, HTTP_SERVICE_CODE } from '@/utils/request';

const Index = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [fieldList, setFieldList] = useState<IFieldItem[]>([]);
  const [messageApi, contextHandler] = message.useMessage();
  const searchParams = new URLSearchParams(location.search);
  const approval_code = searchParams.get('approval_code');
  const type = searchParams.get('type');
  const [form] = Form.useForm();
  const disabled = type === 'search';

  // 监听form变化。form中的判断会用到
  const approvalCode = Form.useWatch(['approval_code'], form);
  const checkOpen = Form.useWatch(['check', 'is_open'], form);
  const executeOpen = Form.useWatch(['execute', 'is_open'], form);
  const fieldOpen = Form.useWatch(['field', 'is_open'], form);
  const relationOpen = Form.useWatch(['relation', 'is_open'], form);
  const showList = Form.useWatch(['field', 'data'], form);

  // 获取fieldsList
  const getFieldsList = async (approval_code: string) => {
    const response = await localRequest<{ body: IFieldItem[] }>(`/lark/approval/fields`, {
      method: 'GET',
      data: { approval_code },
    });
    if (response.retcode !== HTTP_SERVICE_CODE.Success) {
      messageApi.error(response.error);
      return;
    }
    setFieldList(response.resp.body);
  };

  // 获取详情
  const getDetail = async () => {
    const res = await localRequest(`/config/${approval_code}`, { method: 'GET' });
    if (res.retcode !== HTTP_SERVICE_CODE.Success) {
      messageApi.error(res.error);
      return;
    }
    form.setFieldsValue(res.resp);
  };

  // 提交处理
  const handleFinish = (value: IFormField) => {
    if (!value.check.is_open) {
      value.check.url = '';
      value.check.call_type = 'sync';
    }
    if (!value.execute.is_open) {
      value.execute.url = '';
      value.execute.call_type = 'sync';
    }
    if (!value.field.data || !value.field.data.length) {
      value.field.data = [];
    }
    if (!value.relation.data || !value.relation.data.length) {
      value.relation.data = [];
    }
    if (!approval_code) {
      return handleCreate(value);
    }
    if (type === 'edit') {
      return handleUpdate(value);
    }
  };

  // 更新
  const handleUpdate = async (data: IFormField) => {
    const response = await localRequest(`/config`, {
      method: 'PUT',
      data,
      headers: {
        'Content-Type': 'application/json',
      },
    });
    if (response.retcode !== HTTP_SERVICE_CODE.Success) {
      messageApi.error(response.error);
      return;
    }
    messageApi.success('更新成功');
    navigate('/home');
  };

  // 新增
  const handleCreate = async (data: IFormField) => {
    const response = await localRequest('/config', {
      method: 'POST',
      data,
      headers: {
        'Content-Type': 'application/json',
      },
    });
    if (response.retcode !== HTTP_SERVICE_CODE.Success) {
      messageApi.error(response.error);
      return;
    }
    messageApi.success('新增成功');
    navigate('/home');
  };

  useEffect(() => {
    if (approval_code) {
      getDetail();
      getFieldsList(approval_code);
    }
  }, []);
  return (
    <Form
      wrapperCol={{ span: 24 }}
      layout="vertical"
      form={form}
      onFinish={handleFinish}
      initialValues={{
        check: { is_open: false },
        execute: { is_open: false },
        field: { is_open: false },
        relation: { is_open: false },
      }}
      disabled={disabled}
    >
      {contextHandler}
      <Form.Item label="审批定义 code" name="approval_code" rules={[{ required: true }]}>
        <Input placeholder="请输入名称" onBlur={e => getFieldsList(e.target.value)} />
      </Form.Item>
      <Form.Item label="审批配置名称" name="name" rules={[{ required: true }]}>
        <Input placeholder="请输入名称" />
      </Form.Item>
      <Divider>检查节点</Divider>
      <Form.Item
        name={['check', 'is_open']}
        label="开关"
        rules={[{ required: true, message: 'Please input is_open!' }]}
      >
        <Radio.Group>
          <Radio value={true}>打开</Radio>
          <Radio value={false}>关闭</Radio>
        </Radio.Group>
      </Form.Item>
      {checkOpen && (
        <>
          <Form.Item
            name={['check', 'call_type']}
            label="回调类型"
            rules={[{ required: true, message: 'Please input call_type!' }]}
          >
            <Radio.Group>
              <Radio value="sync">同步</Radio>
              <Radio value="async">异步</Radio>
            </Radio.Group>
          </Form.Item>
          <Form.Item
            name={['check', 'url']}
            label="URL"
            rules={[{ required: true, message: 'Please input url!' }]}
          >
            <Input placeholder="请输入url地址" />
          </Form.Item>
        </>
      )}

      <Divider>执行节点</Divider>
      <Form.Item
        name={['execute', 'is_open']}
        label="开关"
        rules={[{ required: true, message: 'Please input is_open!' }]}
      >
        <Radio.Group>
          <Radio value={true}>打开</Radio>
          <Radio value={false}>关闭</Radio>
        </Radio.Group>
      </Form.Item>
      {executeOpen && (
        <>
          <Form.Item
            name={['execute', 'call_type']}
            label="回调类型"
            rules={[{ required: true, message: 'Please input call_type!' }]}
          >
            <Radio.Group>
              <Radio value="sync">同步</Radio>
              <Radio value="async">异步</Radio>
            </Radio.Group>
          </Form.Item>
          <Form.Item
            name={['execute', 'url']}
            label="URL"
            rules={[{ required: true, message: 'Please input url!' }]}
          >
            <Input placeholder="请输入url地址" />
          </Form.Item>
        </>
      )}

      <Divider>外部字段</Divider>
      <Form.Item
        name={['field', 'is_open']}
        label="开关"
        rules={[{ required: true, message: 'Please input is_open!' }]}
      >
        <Radio.Group>
          <Radio value={true}>打开</Radio>
          <Radio value={false}>关闭</Radio>
        </Radio.Group>
      </Form.Item>
      {fieldOpen && (
        <Form.List name={['field', 'data']}>
          {(fields, { add, remove }) => (
            <>
              {fields.map(({ key, name, ...restField }) => (
                <Space key={key} style={{ display: 'flex', marginBottom: 8 }} align="baseline">
                  <Form.Item
                    {...restField}
                    name={[name, 'code']}
                    rules={[{ required: true, message: 'Missing code' }]}
                  >
                    <Select placeholder="code" style={{ width: '200px' }}>
                      {fieldList.map(item => (
                        <Select.Option value={item.value}>{item.label}</Select.Option>
                      ))}
                    </Select>
                  </Form.Item>
                  <Form.Item
                    {...restField}
                    name={[name, 'url']}
                    rules={[{ required: true, message: 'Missing url' }]}
                  >
                    <Input placeholder="url" />
                  </Form.Item>
                  <span className="ml-4">
                    uri: {approvalCode + '/' + (showList[key]?.code || '')}
                  </span>
                  {!disabled && <MinusCircleOutlined onClick={() => remove(name)} />}
                </Space>
              ))}
              <Form.Item>
                <Button type="dashed" onClick={() => add()} block icon={<PlusOutlined />}>
                  添加字段
                </Button>
              </Form.Item>
            </>
          )}
        </Form.List>
      )}

      <Divider>关联字段</Divider>
      <Form.Item
        name={['relation', 'is_open']}
        label="开关"
        rules={[{ required: true, message: 'Please input is_open!' }]}
      >
        <Radio.Group>
          <Radio value={true}>打开</Radio>
          <Radio value={false}>关闭</Radio>
        </Radio.Group>
      </Form.Item>
      {relationOpen && (
        <Form.List name={['relation', 'data']}>
          {(fields, { add, remove }) => (
            <>
              {fields.map(({ key, name, ...restField }) => (
                <Space key={key} style={{ display: 'flex', marginBottom: 8 }} align="baseline">
                  <Form.Item
                    {...restField}
                    name={[name, 'code']}
                    rules={[{ required: true, message: 'Missing code' }]}
                  >
                    <Select placeholder="code" style={{ width: '200px' }}>
                      {fieldList.map(item => (
                        <Select.Option value={item.value}>{item.label}</Select.Option>
                      ))}
                    </Select>
                  </Form.Item>
                  <Form.Item
                    {...restField}
                    name={[name, 'api_key']}
                    rules={[{ required: true, message: 'Missing api_key' }]}
                  >
                    <Input placeholder="api_key" />
                  </Form.Item>
                  {!disabled && <MinusCircleOutlined onClick={() => remove(name)} />}
                </Space>
              ))}
              <Form.Item>
                <Button type="dashed" onClick={() => add()} block icon={<PlusOutlined />}>
                  添加字段
                </Button>
              </Form.Item>
            </>
          )}
        </Form.List>
      )}

      <Form.Item>
        <Button type="primary" htmlType="submit">
          提交
        </Button>
      </Form.Item>
    </Form>
  );
};

export default Index;
