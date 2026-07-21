# Legacy IDS/InfraD 组件 API 参考

> This file is legacy sample material from the original IDS/InfraD project. Replace it with API notes for your own component library before running the generic component documentation workflow.

> 所有示例代码均遵循 react-live 规范：通过 `Infrad`、`Icons`、`InfradPro`、`SpaceBiz` 命名空间访问组件，使用 `React.useState` 等 hooks，不写 import/export/TypeScript。

---

## Infrad 基础组件

### Button 按钮

```jsx
const { Button } = Infrad;
// type: 'primary' | 'dashed' | 'text' | 'link' | 默认不传
// size: 'large' | 'middle' | 'small'
// danger: boolean        - 危险按钮（红色）
// ghost: boolean         - 幽灵按钮（透明背景）
// disabled: boolean
// loading: boolean
// block: boolean         - 撑满父宽度
// shape: 'circle' | 'round' | 'default'
// icon: ReactNode        - 图标
// iconPosition: 'start' | 'end'
// onClick: () => void
// href: string           - 作为链接
// htmlType: 'submit' | 'reset' | 'button'  - 表单中使用

<Button type="primary">Primary</Button>
<Button type="primary" icon={<SearchOutlined />}>Search</Button>
<Button type="primary" loading>Loading</Button>
<Button danger>Delete</Button>
```

### Input 输入框

```jsx
const { Input } = Infrad;
// value / defaultValue: string
// onChange: (e) => void     - e.target.value 获取值
// placeholder: string
// disabled: boolean
// allowClear: boolean
// prefix / suffix: ReactNode
// size: 'large' | 'middle' | 'small'
// maxLength: number
// showCount: boolean

<Input placeholder="Basic usage" />
<Input.Search placeholder="Search" onSearch={value => console.log(value)} enterButton />
<Input.TextArea rows={4} placeholder="Multi-line" />
<Input.Password placeholder="Password" />
<Input prefix={<UserOutlined />} placeholder="Username" />
```

### InputNumber 数字输入

```jsx
const { InputNumber } = Infrad;
// min / max: number
// step: number
// precision: number
// defaultValue: number
// onChange: (value) => void

<InputNumber min={1} max={10} defaultValue={3} onChange={v => console.log(v)} />
```

### Select 选择器

```jsx
const { Select } = Infrad;
// options: Array<{ value, label, disabled? }>
// defaultValue / value: string | string[]
// onChange: (value) => void
// placeholder: string
// allowClear: boolean
// disabled: boolean
// loading: boolean
// mode: 'multiple' | 'tags'    - 多选/标签模式
// style: { width: number }     - 建议设宽度
// showSearch: boolean
// filterOption: (input, option) => boolean

<Select
  defaultValue="lucy"
  style={{ width: 120 }}
  options={[
    { value: 'jack', label: 'Jack' },
    { value: 'lucy', label: 'Lucy' },
    { value: 'disabled', label: 'Disabled', disabled: true },
  ]}
/>

// 多选
<Select
  mode="multiple"
  allowClear
  style={{ width: '100%' }}
  placeholder="Please select"
  defaultValue={['a', 'b']}
  options={[{ value: 'a', label: 'A' }, { value: 'b', label: 'B' }, { value: 'c', label: 'C' }]}
/>
```

### Checkbox 复选框

```jsx
const { Checkbox } = Infrad;
// checked: boolean
// onChange: (e) => void    - e.target.checked
// disabled: boolean

<Checkbox onChange={e => console.log(e.target.checked)}>Checkbox</Checkbox>

// 复选框组
<Checkbox.Group
  options={['Apple', 'Pear', 'Orange']}
  defaultValue={['Apple']}
  onChange={checkedValues => console.log(checkedValues)}
/>
```

### Radio 单选框

```jsx
const { Radio } = Infrad;
// value: any
// onChange: (e) => void    - e.target.value

<Radio.Group defaultValue="a">
  <Radio value="a">A</Radio>
  <Radio value="b">B</Radio>
  <Radio value="c">C</Radio>
</Radio.Group>

// 按钮样式
<Radio.Group defaultValue="a" buttonStyle="solid">
  <Radio.Button value="a">Hangzhou</Radio.Button>
  <Radio.Button value="b">Shanghai</Radio.Button>
  <Radio.Button value="c">Beijing</Radio.Button>
</Radio.Group>
```

### Switch 开关

```jsx
const { Switch } = Infrad;
// checked / defaultChecked: boolean
// onChange: (checked) => void
// checkedChildren / unCheckedChildren: ReactNode
// size: 'default' | 'small'
// disabled: boolean
// loading: boolean

<Switch defaultChecked onChange={checked => console.log(checked)} />
<Switch checkedChildren="ON" unCheckedChildren="OFF" defaultChecked />
```

### DatePicker 日期选择

```jsx
const { DatePicker } = Infrad;
// onChange: (date, dateString) => void
// picker: 'date' | 'week' | 'month' | 'quarter' | 'year'
// showTime: boolean     - 日期时间选择
// format: string        - 如 'YYYY-MM-DD'

<DatePicker onChange={(date, dateString) => console.log(dateString)} />
<DatePicker picker="month" />
<DatePicker.RangePicker />
```

### TimePicker 时间选择

```jsx
const { TimePicker } = Infrad;
<TimePicker onChange={(time, timeString) => console.log(timeString)} />
```

### Rate 评分

```jsx
const { Rate } = Infrad;
// defaultValue: number
// allowHalf: boolean
// count: number
// disabled: boolean

<Rate allowHalf defaultValue={2.5} />
```

### Slider 滑动输入

```jsx
const { Slider } = Infrad;
// defaultValue: number | [number, number]
// range: boolean     - 双滑块模式
// min / max: number
// step: number
// marks: object

<Slider defaultValue={30} />
<Slider range defaultValue={[20, 50]} />
```

### Upload 上传

```jsx
const { Upload, Button } = Infrad;
const { UploadOutlined } = Icons;
// action: string          - 上传地址
// listType: 'text' | 'picture' | 'picture-card'
// multiple: boolean
// accept: string

<Upload action="/upload">
  <Button icon={<UploadOutlined />}>Click to Upload</Button>
</Upload>
```

### Transfer 穿梭框

```jsx
const { Transfer } = Infrad;
// dataSource: Array<{ key, title, description? }>
// targetKeys: string[]
// onChange: (targetKeys) => void
// titles: [string, string]

<Transfer
  dataSource={[
    { key: '1', title: 'Item 1' },
    { key: '2', title: 'Item 2' },
    { key: '3', title: 'Item 3' },
  ]}
  targetKeys={['2']}
  render={item => item.title}
/>
```

### Cascader 级联选择

```jsx
const { Cascader } = Infrad;
// options: 嵌套数组 { value, label, children? }
// onChange: (value) => void
// placeholder: string

<Cascader
  options={[{
    value: 'zhejiang', label: 'Zhejiang',
    children: [{ value: 'hangzhou', label: 'Hangzhou' }],
  }]}
  placeholder="Please select"
/>
```

### TreeSelect 树选择

```jsx
const { TreeSelect } = Infrad;
<TreeSelect
  style={{ width: '100%' }}
  treeData={[{
    title: 'Parent', value: 'parent',
    children: [
      { title: 'Child 1', value: 'child1' },
      { title: 'Child 2', value: 'child2' },
    ],
  }]}
  placeholder="Please select"
/>
```

### AutoComplete 自动完成

```jsx
const { AutoComplete } = Infrad;
<AutoComplete
  style={{ width: 200 }}
  options={[{ value: 'Option 1' }, { value: 'Option 2' }]}
  placeholder="Type here"
  filterOption={(input, option) => option.value.toLowerCase().includes(input.toLowerCase())}
/>
```

### ColorPicker 颜色选择

```jsx
const { ColorPicker } = Infrad;
<ColorPicker defaultValue="#1677ff" />
```

---

### Table 表格

```jsx
const { Table, Tag, Space } = Infrad;
// columns: Array<{ title, dataIndex, key, render?, sorter?, filters?, width? }>
// dataSource: Array<object>
// rowKey: string | function
// pagination: false | { pageSize, total, current, onChange }
// loading: boolean
// bordered: boolean
// size: 'default' | 'middle' | 'small'
// scroll: { x: number, y: number }
// rowSelection: { type: 'checkbox'|'radio', selectedRowKeys, onChange }
// expandable: { expandedRowRender }
// onChange: (pagination, filters, sorter) => void

const columns = [
  { title: 'Name', dataIndex: 'name', key: 'name' },
  { title: 'Age', dataIndex: 'age', key: 'age', sorter: (a, b) => a.age - b.age },
  { title: 'Address', dataIndex: 'address', key: 'address' },
  {
    title: 'Tags', dataIndex: 'tags', key: 'tags',
    render: (tags) => tags.map(tag => <Tag color="blue" key={tag}>{tag}</Tag>),
  },
  {
    title: 'Action', key: 'action',
    render: (_, record) => (
      <Space size="middle">
        <a>Edit</a>
        <a>Delete</a>
      </Space>
    ),
  },
];

const data = [
  { key: '1', name: 'John Brown', age: 32, address: 'New York', tags: ['developer'] },
  { key: '2', name: 'Jim Green', age: 42, address: 'London', tags: ['designer'] },
];

<Table columns={columns} dataSource={data} />
```

### Tag 标签

```jsx
const { Tag } = Infrad;
// color: 预设颜色 'success'|'processing'|'error'|'warning'|'default'
//        或具体颜色 'blue'|'red'|'green'|'orange'|'cyan'|'purple'|'gold'|'magenta' 等
//        或自定义 hex
// closable: boolean
// onClose: (e) => void
// icon: ReactNode
// bordered: boolean

<Tag>Default</Tag>
<Tag color="success">Success</Tag>
<Tag color="blue">Blue</Tag>
<Tag color="#f50">#f50</Tag>
<Tag closable onClose={e => e.preventDefault()}>Closable</Tag>

// 可选标签
const { Tag } = Infrad;
<Tag.CheckableTag checked={true}>Checked</Tag.CheckableTag>
```

### Badge 徽标

```jsx
const { Badge, Avatar } = Infrad;
// count: number | ReactNode
// dot: boolean
// overflowCount: number     - 默认 99
// status: 'success'|'processing'|'default'|'error'|'warning'
// color: string
// size: 'default' | 'small'
// offset: [number, number]

<Badge count={5}><Avatar shape="square" size="large" /></Badge>
<Badge dot><Avatar shape="square" size="large" /></Badge>
<Badge count={0} showZero><Avatar shape="square" size="large" /></Badge>
<Badge status="success" text="Success" />
```

### Avatar 头像

```jsx
const { Avatar } = Infrad;
const { UserOutlined } = Icons;
// size: number | 'large' | 'small' | 'default'
// shape: 'circle' | 'square'
// src: string           - 图片地址
// icon: ReactNode

<Avatar icon={<UserOutlined />} />
<Avatar size={64} src="https://api.dicebear.com/7.x/miniavs/svg?seed=1" />

// 头像组
const { Avatar } = Infrad;
<Avatar.Group maxCount={3}>
  <Avatar src="https://api.dicebear.com/7.x/miniavs/svg?seed=1" />
  <Avatar src="https://api.dicebear.com/7.x/miniavs/svg?seed=2" />
  <Avatar src="https://api.dicebear.com/7.x/miniavs/svg?seed=3" />
  <Avatar src="https://api.dicebear.com/7.x/miniavs/svg?seed=4" />
</Avatar.Group>
```

### Card 卡片

```jsx
const { Card, Button } = Infrad;
// title: ReactNode
// extra: ReactNode       - 右上角操作区
// bordered: boolean
// size: 'default' | 'small'
// hoverable: boolean     - 鼠标悬停浮起
// cover: ReactNode       - 封面图
// actions: ReactNode[]   - 底部操作栏
// loading: boolean

<Card title="Card title" extra={<a>More</a>} style={{ width: 300 }}>
  <p>Card content</p>
</Card>

// 网格卡片
const { Card, Col, Row } = Infrad;
<Row gutter={16}>
  <Col span={8}><Card title="Card 1">Content</Card></Col>
  <Col span={8}><Card title="Card 2">Content</Card></Col>
  <Col span={8}><Card title="Card 3">Content</Card></Col>
</Row>
```

### Carousel 走马灯

```jsx
const { Carousel } = Infrad;
// autoplay: boolean
// dots: boolean
// effect: 'scrollx' | 'fade'

<Carousel autoplay>
  <div><h3>Slide 1</h3></div>
  <div><h3>Slide 2</h3></div>
  <div><h3>Slide 3</h3></div>
</Carousel>
```

### Collapse 折叠面板

```jsx
const { Collapse } = Infrad;
// items: Array<{ key, label, children, extra? }>
// defaultActiveKey: string[]
// accordion: boolean     - 手风琴模式

<Collapse
  defaultActiveKey={['1']}
  items={[
    { key: '1', label: 'Panel 1', children: <p>Content 1</p> },
    { key: '2', label: 'Panel 2', children: <p>Content 2</p> },
    { key: '3', label: 'Panel 3', children: <p>Content 3</p> },
  ]}
/>
```

### Descriptions 描述列表

```jsx
const { Descriptions } = Infrad;
// title: ReactNode
// bordered: boolean
// column: number | { xs, sm, md, lg }
// size: 'default' | 'middle' | 'small'
// layout: 'horizontal' | 'vertical'
// items: Array<{ key, label, children, span? }>

<Descriptions title="User Info" bordered>
  items={[
    { key: '1', label: 'UserName', children: 'John' },
    { key: '2', label: 'Phone', children: '18100000000' },
    { key: '3', label: 'Address', children: 'New York No. 1 Lake Park' },
  ]}
/>
```

### List 列表

```jsx
const { List, Avatar } = Infrad;
// dataSource: any[]
// renderItem: (item, index) => ReactNode
// header / footer: ReactNode
// bordered: boolean
// size: 'default' | 'small' | 'large'
// pagination: false | object
// grid: { gutter, column }

<List
  bordered
  dataSource={['Item 1', 'Item 2', 'Item 3']}
  renderItem={item => <List.Item>{item}</List.Item>}
/>

// 带头像的列表
<List
  itemLayout="horizontal"
  dataSource={data}
  renderItem={item => (
    <List.Item>
      <List.Item.Meta
        avatar={<Avatar src={item.avatar} />}
        title={item.title}
        description={item.description}
      />
    </List.Item>
  )}
/>
```

### Statistic 统计数值

```jsx
const { Statistic, Row, Col } = Infrad;
// title: ReactNode
// value: number | string
// precision: number
// prefix / suffix: ReactNode
// valueStyle: CSSProperties
// groupSeparator: string

<Row gutter={16}>
  <Col span={12}>
    <Statistic title="Active Users" value={112893} />
  </Col>
  <Col span={12}>
    <Statistic title="Account Balance" value={112893} precision={2} prefix="$" />
  </Col>
</Row>

// 倒计时
const { Statistic } = Infrad;
<Statistic.Countdown title="Deadline" value={Date.now() + 1000 * 60 * 60 * 24} />
```

### Timeline 时间轴

```jsx
const { Timeline } = Infrad;
// items: Array<{ children, color?, dot?, label? }>
// mode: 'left' | 'alternate' | 'right'
// pending: ReactNode | boolean

<Timeline
  items={[
    { children: 'Create 2015-09-01' },
    { children: 'Solve 2015-09-01', color: 'green' },
    { children: 'Testing 2015-09-01', color: 'red' },
    { children: 'Deploy 2015-09-01' },
  ]}
/>
```

### Tree 树形控件

```jsx
const { Tree } = Infrad;
// treeData: Array<{ title, key, children? }>
// defaultExpandedKeys: string[]
// checkable: boolean
// selectable: boolean

<Tree
  checkable
  defaultExpandedKeys={['0-0']}
  treeData={[{
    title: 'Parent', key: '0-0',
    children: [
      { title: 'Child 1', key: '0-0-0' },
      { title: 'Child 2', key: '0-0-1' },
    ],
  }]}
/>
```

### Image 图片

```jsx
const { Image } = Infrad;
// src: string
// width: number
// preview: boolean | object
// fallback: string

<Image width={200} src="https://via.placeholder.com/200" />

// 图片组预览
<Image.PreviewGroup>
  <Image width={200} src="https://via.placeholder.com/200" />
  <Image width={200} src="https://via.placeholder.com/200" />
</Image.PreviewGroup>
```

### Typography 排版

```jsx
const { Typography } = Infrad;
const { Title, Paragraph, Text, Link } = Typography;

<Title level={2}>h2 Title</Title>
<Paragraph>Content paragraph</Paragraph>
<Text>Inline text</Text>
<Text type="secondary">Secondary</Text>
<Text type="success">Success</Text>
<Text type="warning">Warning</Text>
<Text type="danger">Danger</Text>
<Text strong>Bold</Text>
<Text italic>Italic</Text>
<Text underline>Underline</Text>
<Text delete>Deleted</Text>
<Text code>Code</Text>
<Text copyable>Copy me</Text>
<Link href="https://example.com">Link</Link>
```

### Empty 空状态

```jsx
const { Empty } = Infrad;
<Empty />
<Empty description="No Data" />
<Empty image={Empty.PRESENTED_IMAGE_SIMPLE} />
```

### QRCode 二维码

```jsx
const { QRCode } = Infrad;
<QRCode value="https://infrad.shopee.io" />
```

### Segmented 分段控制

```jsx
const { Segmented } = Infrad;
<Segmented options={['Daily', 'Weekly', 'Monthly', 'Quarterly', 'Yearly']} />
<Segmented
  options={[
    { label: 'List', value: 'list', icon: <BarsOutlined /> },
    { label: 'Kanban', value: 'kanban', icon: <AppstoreOutlined /> },
  ]}
/>
```

### Tour 漫游式引导

```jsx
const { Tour, Button, Divider, Space } = Infrad;
// open: boolean
// onClose: () => void
// steps: Array<{ title, description, cover?, target: () => ref.current }>
// type: 'default' | 'primary'
// mask: boolean | { style, color }
// placement: 'top' | 'bottom' | 'left' | 'right' | ...

function App() {
  const ref1 = React.useRef(null);
  const ref2 = React.useRef(null);
  const ref3 = React.useRef(null);
  const [open, setOpen] = React.useState(false);

  const steps = [
    { title: 'Upload File', description: 'Put your files here.', target: () => ref1.current },
    { title: 'Save', description: 'Save your changes.', target: () => ref2.current },
    { title: 'More', description: 'Click for more actions.', target: () => ref3.current },
  ];

  return (
    <>
      <Button type="primary" onClick={() => setOpen(true)}>Begin Tour</Button>
      <Divider />
      <Space>
        <Button ref={ref1}>Upload</Button>
        <Button ref={ref2} type="primary">Save</Button>
        <Button ref={ref3}>More</Button>
      </Space>
      <Tour open={open} onClose={() => setOpen(false)} steps={steps} />
    </>
  );
}
```

### Affix 固钉

```jsx
const { Affix, Button } = Infrad;
// offsetTop: number       - 距离窗口顶部达到指定偏移量后触发固定
// offsetBottom: number    - 距离窗口底部达到指定偏移量后触发固定
// target: () => HTMLElement  - 指定滚动容器

function App() {
  const [top, setTop] = React.useState(100);
  return (
    <>
      <Affix offsetTop={top}>
        <Button type="primary" onClick={() => setTop(top + 10)}>
          Affix top ({top})
        </Button>
      </Affix>
      <br />
      <Affix offsetBottom={100}>
        <Button type="primary">Affix bottom</Button>
      </Affix>
    </>
  );
}
```

### Anchor 锚点

```jsx
const { Anchor, Row, Col } = Infrad;
// items: Array<{ key, href, title, children? }>
// affix: boolean           - 是否固定
// offsetTop: number
// targetOffset: number
// direction: 'vertical' | 'horizontal'
// getCurrentAnchor: (activeLink) => string

<Anchor
  items={[
    { key: 'part-1', href: '#part-1', title: 'Part 1' },
    { key: 'part-2', href: '#part-2', title: 'Part 2' },
    { key: 'part-3', href: '#part-3', title: 'Part 3',
      children: [
        { key: 'part-3-1', href: '#part-3-1', title: 'Part 3-1' },
      ],
    },
  ]}
/>
```

### App 包裹组件

```jsx
const { App, Button, Space } = Infrad;
// 提供 message / modal / notification 的 context 注入
// 使用 App.useApp() 获取静态方法的 hook 版本

function MyPage() {
  const { message, modal, notification } = App.useApp();
  return (
    <Space>
      <Button onClick={() => message.success('Success!')}>Message</Button>
      <Button onClick={() => modal.warning({ title: 'Warning', content: 'Details...' })}>Modal</Button>
      <Button onClick={() => notification.info({ message: 'Notification', description: 'Content' })}>
        Notification
      </Button>
    </Space>
  );
}

function App() {
  const { App: InfradApp } = Infrad;
  return (
    <InfradApp>
      <MyPage />
    </InfradApp>
  );
}
```

### Calendar 日历

```jsx
const { Calendar } = Infrad;
// mode: 'month' | 'year'
// value / defaultValue: Dayjs
// fullscreen: boolean      - false 为卡片模式
// onPanelChange: (date, mode) => void
// onSelect: (date) => void
// cellRender: (current, info) => ReactNode  - 自定义日期单元格

<Calendar />
<Calendar fullscreen={false} />
```

### Mentions 提及

```jsx
const { Mentions } = Infrad;
// options: Array<{ value, label }>
// prefix: string | string[]    - 触发字符，默认 '@'
// defaultValue: string
// onChange: (value) => void
// onSelect: (option) => void
// placement: 'top' | 'bottom'
// split: string

<Mentions
  style={{ width: '100%' }}
  defaultValue="@afc163"
  options={[
    { value: 'afc163', label: 'afc163' },
    { value: 'zombieJ', label: 'zombieJ' },
    { value: 'yesmeck', label: 'yesmeck' },
  ]}
/>
```

### Splitter 分割面板

```jsx
const { Splitter, Typography, Flex } = Infrad;
// layout: 'horizontal' | 'vertical'
// Splitter.Panel:
//   defaultSize: number | string     - 初始尺寸
//   min: number | string             - 最小尺寸
//   max: number | string             - 最大尺寸
//   collapsible: boolean | { start, end }
//   resizable: boolean

function Desc({ text }) {
  return (
    <Flex justify="center" align="center" style={{ height: '100%' }}>
      <Typography.Title type="secondary" level={5}>{text}</Typography.Title>
    </Flex>
  );
}

function App() {
  return (
    <Splitter style={{ height: 300, boxShadow: '0 0 10px rgba(0,0,0,0.1)' }}>
      <Splitter.Panel collapsible>
        <Desc text="Left" />
      </Splitter.Panel>
      <Splitter.Panel>
        <Splitter layout="vertical">
          <Splitter.Panel><Desc text="Top" /></Splitter.Panel>
          <Splitter.Panel><Desc text="Bottom" /></Splitter.Panel>
        </Splitter>
      </Splitter.Panel>
    </Splitter>
  );
}
```

---

### Tabs 标签页

```jsx
const { Tabs } = Infrad;
// defaultActiveKey: string
// items: Array<{ key, label, children, disabled?, icon?, closable? }>
// onChange: (activeKey) => void
// type: 'line' | 'card' | 'editable-card'
// tabPosition: 'top' | 'right' | 'bottom' | 'left'
// size: 'large' | 'middle' | 'small'
// centered: boolean

<Tabs
  defaultActiveKey="1"
  items={[
    { key: '1', label: 'Tab 1', children: 'Content of Tab 1' },
    { key: '2', label: 'Tab 2', children: 'Content of Tab 2' },
    { key: '3', label: 'Tab 3', children: 'Content of Tab 3' },
  ]}
/>
```

### Steps 步骤条

```jsx
const { Steps } = Infrad;
// current: number          - 当前步骤（从 0 开始）
// items: Array<{ title, description?, subTitle?, icon?, status? }>
// direction: 'horizontal' | 'vertical'
// size: 'default' | 'small'
// status: 'wait' | 'process' | 'finish' | 'error'
// progressDot: boolean

<Steps
  current={1}
  items={[
    { title: 'Finished', description: 'Step 1 done' },
    { title: 'In Progress', description: 'Step 2 working' },
    { title: 'Waiting', description: 'Step 3 pending' },
  ]}
/>
```

### Pagination 分页

```jsx
const { Pagination } = Infrad;
// current: number
// total: number
// pageSize: number
// onChange: (page, pageSize) => void
// showSizeChanger: boolean
// showQuickJumper: boolean
// showTotal: (total) => string
// size: 'default' | 'small'
// simple: boolean

<Pagination defaultCurrent={1} total={50} />
<Pagination total={500} showSizeChanger showQuickJumper showTotal={total => `Total ${total}`} />
```

### Breadcrumb 面包屑

```jsx
const { Breadcrumb } = Infrad;
// items: Array<{ title, href?, path?, menu? }>

<Breadcrumb items={[
  { title: 'Home' },
  { title: 'App Center', href: '' },
  { title: 'App' },
]} />
```

### Dropdown 下拉菜单

```jsx
const { Dropdown, Button, Space } = Infrad;
const { DownOutlined } = Icons;
// menu: { items: Array<{ key, label, icon?, danger?, disabled? }>, onClick }
// trigger: Array<'hover' | 'click' | 'contextMenu'>
// placement: 'bottom' | 'bottomLeft' | 'bottomRight' | 'top' | 'topLeft' | 'topRight'

<Dropdown menu={{
  items: [
    { key: '1', label: 'Item 1' },
    { key: '2', label: 'Item 2' },
    { key: '3', label: 'Item 3', danger: true },
  ],
  onClick: ({ key }) => console.log(key),
}}>
  <a onClick={e => e.preventDefault()}>
    <Space>Hover me<DownOutlined /></Space>
  </a>
</Dropdown>

// 按钮下拉
<Dropdown.Button menu={{ items }}>Actions</Dropdown.Button>
```

### Menu 菜单

```jsx
const { Menu } = Infrad;
// items: Array<{ key, label, icon?, children?, type?, danger? }>
// mode: 'horizontal' | 'vertical' | 'inline'
// defaultSelectedKeys: string[]
// defaultOpenKeys: string[]
// onClick: ({ key }) => void

<Menu
  mode="horizontal"
  defaultSelectedKeys={['mail']}
  items={[
    { key: 'mail', label: 'Navigation One', icon: <MailOutlined /> },
    { key: 'app', label: 'Navigation Two', icon: <AppstoreOutlined /> },
    {
      key: 'sub', label: 'Navigation Three', icon: <SettingOutlined />,
      children: [
        { key: 'sub1', label: 'Option 1' },
        { key: 'sub2', label: 'Option 2' },
      ],
    },
  ]}
/>
```

---

### Form 表单

```jsx
const { Form, Input, Button, Checkbox, Select, Radio, DatePicker, InputNumber, Switch } = Infrad;
// Form props:
//   name: string
//   layout: 'horizontal' | 'vertical' | 'inline'
//   labelCol: { span: number }
//   wrapperCol: { span: number }
//   initialValues: object
//   onFinish: (values) => void
//   onFinishFailed: (errorInfo) => void
//   form: Form.useForm() 返回值
//   size: 'large' | 'middle' | 'small'

// Form.Item props:
//   label: string
//   name: string            - 字段名（与 initialValues 的 key 对应）
//   rules: Array<{ required?, message?, type?, min?, max?, pattern? }>
//   valuePropName: string   - 如 Checkbox 用 'checked'

<Form
  name="basic"
  labelCol={{ span: 8 }}
  wrapperCol={{ span: 16 }}
  style={{ maxWidth: 600 }}
  initialValues={{ remember: true }}
  onFinish={values => console.log(values)}
>
  <Form.Item label="Username" name="username" rules={[{ required: true, message: 'Required!' }]}>
    <Input />
  </Form.Item>
  <Form.Item label="Password" name="password" rules={[{ required: true, message: 'Required!' }]}>
    <Input.Password />
  </Form.Item>
  <Form.Item name="remember" valuePropName="checked" label={null}>
    <Checkbox>Remember me</Checkbox>
  </Form.Item>
  <Form.Item label={null}>
    <Button type="primary" htmlType="submit">Submit</Button>
  </Form.Item>
</Form>
```

---

### Alert 警告提示

```jsx
const { Alert } = Infrad;
// message: ReactNode       - 标题
// description: ReactNode   - 详细描述
// type: 'success' | 'info' | 'warning' | 'error'
// showIcon: boolean
// closable: boolean
// action: ReactNode        - 右侧操作区
// banner: boolean          - 顶部公告模式

<Alert message="Success" type="success" showIcon />
<Alert message="Info" description="Detailed description" type="info" showIcon closable />
<Alert
  message="Warning"
  type="warning"
  action={<Button size="small" type="text">UNDO</Button>}
  closable
/>
```

### Modal 对话框

```jsx
const { Modal, Button } = Infrad;
// title: ReactNode
// open: boolean
// onOk: () => void
// onCancel: () => void
// footer: ReactNode | null     - null 隐藏底部按钮
// width: number | string
// centered: boolean
// closable: boolean
// confirmLoading: boolean
// destroyOnClose: boolean
// maskClosable: boolean

function App() {
  const [open, setOpen] = React.useState(false);
  return (
    <>
      <Button type="primary" onClick={() => setOpen(true)}>Open Modal</Button>
      <Modal title="Title" open={open} onOk={() => setOpen(false)} onCancel={() => setOpen(false)}>
        <p>Some contents...</p>
      </Modal>
    </>
  );
}

// 快捷方法（静态调用，不需要状态管理）
// Modal.confirm({ title, content, onOk, onCancel })
// Modal.info({ title, content })
// Modal.success / Modal.error / Modal.warning
```

### Drawer 抽屉

```jsx
const { Drawer, Button } = Infrad;
// title: ReactNode
// open: boolean
// onClose: () => void
// placement: 'top' | 'right' | 'bottom' | 'left'
// width: number | string       - 左右方向时
// height: number | string      - 上下方向时
// closable: boolean
// extra: ReactNode             - 标题栏右侧操作
// footer: ReactNode

function App() {
  const [open, setOpen] = React.useState(false);
  return (
    <>
      <Button type="primary" onClick={() => setOpen(true)}>Open</Button>
      <Drawer title="Drawer" onClose={() => setOpen(false)} open={open}>
        <p>Content...</p>
      </Drawer>
    </>
  );
}
```

### message 全局提示

```jsx
const { message, Button, Space } = Infrad;
// message.success(content, duration?)
// message.error(content)
// message.info(content)
// message.warning(content)
// message.loading(content)

function App() {
  const [messageApi, contextHolder] = message.useMessage();
  return (
    <>
      {contextHolder}
      <Space>
        <Button onClick={() => messageApi.success('Success!')}>Success</Button>
        <Button onClick={() => messageApi.error('Error!')}>Error</Button>
        <Button onClick={() => messageApi.warning('Warning!')}>Warning</Button>
      </Space>
    </>
  );
}
```

### notification 通知提醒

```jsx
const { notification, Button, Space } = Infrad;
// notification.success({ message, description, placement? })
// notification.error / info / warning

function App() {
  const [api, contextHolder] = notification.useNotification();
  return (
    <>
      {contextHolder}
      <Button onClick={() => api.info({
        message: 'Notification Title',
        description: 'This is the content of the notification.',
      })}>
        Open Notification
      </Button>
    </>
  );
}
```

### Popconfirm 气泡确认框

```jsx
const { Popconfirm, Button } = Infrad;
// title: ReactNode
// description: ReactNode
// onConfirm: () => void
// onCancel: () => void
// okText / cancelText: string

<Popconfirm title="Delete?" description="Are you sure?" onConfirm={() => console.log('confirmed')}>
  <Button danger>Delete</Button>
</Popconfirm>
```

### Tooltip 文字提示

```jsx
const { Tooltip, Button } = Infrad;
// title: ReactNode
// placement: 'top' | 'bottom' | 'left' | 'right' | ... (12 种)
// color: string

<Tooltip title="Prompt text">
  <Button>Hover me</Button>
</Tooltip>
```

### Popover 气泡卡片

```jsx
const { Popover, Button } = Infrad;
// title: ReactNode
// content: ReactNode
// trigger: 'hover' | 'focus' | 'click'

<Popover title="Title" content={<div>Content</div>}>
  <Button>Hover me</Button>
</Popover>
```

### Progress 进度条

```jsx
const { Progress } = Infrad;
// percent: number
// status: 'success' | 'exception' | 'normal' | 'active'
// type: 'line' | 'circle' | 'dashboard'
// showInfo: boolean
// strokeColor: string | object

<Progress percent={30} />
<Progress percent={70} status="exception" />
<Progress percent={100} />
<Progress type="circle" percent={75} />
<Progress type="dashboard" percent={75} />
```

### Result 结果页

```jsx
const { Result, Button } = Infrad;
// status: 'success' | 'error' | 'info' | 'warning' | '404' | '403' | '500'
// title: string
// subTitle: string
// extra: ReactNode

<Result
  status="success"
  title="Successfully Purchased!"
  subTitle="Order number: 2017182818828182881."
  extra={[
    <Button type="primary" key="console">Go Console</Button>,
    <Button key="buy">Buy Again</Button>,
  ]}
/>
```

### Skeleton 骨架屏

```jsx
const { Skeleton } = Infrad;
// active: boolean
// avatar: boolean | object
// paragraph: boolean | { rows, width }
// title: boolean | { width }
// loading: boolean       - 配合 children 使用

<Skeleton active />
<Skeleton avatar paragraph={{ rows: 4 }} />
```

### Spin 加载中

```jsx
const { Spin, Alert } = Infrad;
// size: 'small' | 'default' | 'large'
// tip: string
// spinning: boolean      - 包裹内容时控制是否显示

<Spin />
<Spin tip="Loading...">
  <Alert message="Content" description="Loading content..." type="info" />
</Spin>
```

### Watermark 水印

```jsx
const { Watermark } = Infrad;
<Watermark content="Infra Design">
  <div style={{ height: 300 }} />
</Watermark>
```

### FloatButton 悬浮按钮

```jsx
const { FloatButton } = Infrad;
const { QuestionCircleOutlined } = Icons;
<FloatButton icon={<QuestionCircleOutlined />} />
<FloatButton.BackTop />
<FloatButton.Group shape="circle">
  <FloatButton icon={<QuestionCircleOutlined />} />
  <FloatButton />
  <FloatButton.BackTop />
</FloatButton.Group>
```

---

### Layout 布局

```jsx
const { Layout, Menu } = Infrad;
const { Header, Content, Footer, Sider } = Layout;

<Layout>
  <Header>Header</Header>
  <Layout>
    <Sider width={200}>Sider</Sider>
    <Content>Content</Content>
  </Layout>
  <Footer>Footer</Footer>
</Layout>
```

### Space 间距

```jsx
const { Space, Button } = Infrad;
// size: 'small' | 'middle' | 'large' | number
// direction: 'horizontal' | 'vertical'
// align: 'start' | 'end' | 'center' | 'baseline'
// wrap: boolean

<Space>
  <Button>Button 1</Button>
  <Button>Button 2</Button>
  <Button>Button 3</Button>
</Space>
<Space direction="vertical" style={{ width: '100%' }}>...</Space>

// Space.Compact - 紧凑排列
<Space.Compact>
  <Input style={{ width: '80%' }} defaultValue="Search" />
  <Button type="primary">Submit</Button>
</Space.Compact>
```

### Flex 弹性布局

```jsx
const { Flex, Button } = Infrad;
// gap: 'small' | 'middle' | 'large' | number
// wrap: boolean | 'wrap' | 'nowrap'
// justify: 'flex-start' | 'center' | 'flex-end' | 'space-between' | 'space-around'
// align: 'flex-start' | 'center' | 'flex-end' | 'stretch'
// vertical: boolean

<Flex gap="small" wrap>
  <Button type="primary">Primary</Button>
  <Button>Default</Button>
</Flex>
<Flex vertical gap="middle">...</Flex>
```

### Grid 栅格

```jsx
const { Row, Col } = Infrad;
// Row: gutter (间距), justify, align, wrap
// Col: span (0-24), offset, push, pull, xs/sm/md/lg/xl/xxl (响应式)

<Row gutter={16}>
  <Col span={6}><div>col-6</div></Col>
  <Col span={6}><div>col-6</div></Col>
  <Col span={6}><div>col-6</div></Col>
  <Col span={6}><div>col-6</div></Col>
</Row>

// 响应式
<Row gutter={[16, 16]}>
  <Col xs={24} sm={12} md={8} lg={6}><div>Responsive</div></Col>
</Row>
```

### Divider 分割线

```jsx
const { Divider } = Infrad;
// type: 'horizontal' | 'vertical'
// orientation: 'left' | 'right' | 'center'
// dashed: boolean
// plain: boolean

<Divider />
<Divider orientation="left">Title</Divider>
<Divider type="vertical" />
<Divider dashed />
```

---

## InfradPro 高级组件

### ProTable 高级表格

```jsx
const { ProTable } = InfradPro;
const { Button } = Infrad;
// columns: Array<ProColumns>  - 扩展了 valueType, valueEnum, hideInSearch, hideInTable 等
// dataSource: Array<object>   - 静态数据
// request: (params, sorter, filter) => Promise<{ data, success, total }>  - 异步请求
// rowKey: string
// search: false | object      - false 隐藏搜索栏
// toolBarRender: false | () => ReactNode[]
// pagination: false | object
// headerTitle: ReactNode
// dateFormatter: 'string' | 'number' | false

// ProColumns 扩展字段:
//   valueType: 'text'|'money'|'date'|'dateTime'|'option'|'index'|'progress'|'digit'|'percent' 等
//   valueEnum: { [key]: { text, status? } }  - 枚举映射
//   hideInSearch: boolean
//   hideInTable: boolean
//   copyable: boolean
//   ellipsis: boolean

const columns = [
  { title: 'Name', dataIndex: 'name' },
  { title: 'Status', dataIndex: 'status', valueEnum: {
    0: { text: 'Closed', status: 'Default' },
    1: { text: 'Running', status: 'Processing' },
    2: { text: 'Error', status: 'Error' },
  }},
  { title: 'Created', dataIndex: 'createdAt', valueType: 'dateTime' },
  { title: 'Action', valueType: 'option', render: () => [<a key="edit">Edit</a>] },
];

<ProTable
  columns={columns}
  dataSource={[
    { id: 1, name: 'App 1', status: 1, createdAt: Date.now() },
    { id: 2, name: 'App 2', status: 0, createdAt: Date.now() },
  ]}
  rowKey="id"
  search={false}
  toolBarRender={() => [<Button key="add" type="primary">New</Button>]}
/>
```

### ProForm 高级表单

```jsx
const { ProForm, ProFormText, ProFormSelect, ProFormDigit, ProFormDatePicker,
        ProFormRadio, ProFormCheckbox, ProFormSwitch, ProFormTextArea,
        ProFormGroup } = InfradPro;

<ProForm onFinish={async (values) => console.log(values)}>
  <ProFormText name="name" label="Name" placeholder="Enter name" rules={[{ required: true }]} />
  <ProFormText.Password name="password" label="Password" />
  <ProFormSelect name="gender" label="Gender" options={[
    { value: 'male', label: 'Male' },
    { value: 'female', label: 'Female' },
  ]} />
  <ProFormDigit name="age" label="Age" min={1} max={100} />
  <ProFormDatePicker name="birthday" label="Birthday" />
  <ProFormRadio.Group name="type" label="Type" options={['A', 'B', 'C']} />
  <ProFormSwitch name="enabled" label="Enabled" />
  <ProFormTextArea name="remark" label="Remark" />
</ProForm>
```

### ModalForm / DrawerForm

```jsx
const { ModalForm, ProFormText } = InfradPro;
const { Button } = Infrad;

<ModalForm
  title="New Item"
  trigger={<Button type="primary">New</Button>}
  onFinish={async (values) => { console.log(values); return true; }}
>
  <ProFormText name="name" label="Name" rules={[{ required: true }]} />
</ModalForm>
```

### QueryFilter / LightFilter

```jsx
const { QueryFilter, ProFormText, ProFormSelect, ProFormDatePicker } = InfradPro;

<QueryFilter onFinish={async (values) => console.log(values)}>
  <ProFormText name="name" label="Name" />
  <ProFormSelect name="status" label="Status" options={['Active', 'Inactive']} />
  <ProFormDatePicker name="date" label="Date" />
</QueryFilter>
```

### StepsForm 分步表单

```jsx
const { StepsForm, ProFormText, ProFormSelect } = InfradPro;

<StepsForm onFinish={async (values) => console.log(values)}>
  <StepsForm.StepForm name="base" title="Basic Info">
    <ProFormText name="name" label="Name" rules={[{ required: true }]} />
  </StepsForm.StepForm>
  <StepsForm.StepForm name="config" title="Configuration">
    <ProFormSelect name="type" label="Type" options={['A', 'B']} />
  </StepsForm.StepForm>
</StepsForm>
```

### ProDescriptions

```jsx
const { ProDescriptions } = InfradPro;

<ProDescriptions
  title="Details"
  dataSource={{ name: 'John', status: 'active', date: '2024-01-01' }}
  columns={[
    { title: 'Name', dataIndex: 'name' },
    { title: 'Status', dataIndex: 'status', valueEnum: {
      active: { text: 'Active', status: 'Success' },
      inactive: { text: 'Inactive', status: 'Default' },
    }},
    { title: 'Date', dataIndex: 'date', valueType: 'date' },
  ]}
/>
```

### ProCard

```jsx
const { ProCard } = InfradPro;

<ProCard title="Card Title" bordered headerBordered>
  Content
</ProCard>

// 分栏
<ProCard split="vertical">
  <ProCard title="Left" colSpan="30%">Left content</ProCard>
  <ProCard title="Right">Right content</ProCard>
</ProCard>

// 标签页卡片
<ProCard tabs={{ type: 'card' }}>
  <ProCard.TabPane key="tab1" tab="Tab 1">Content 1</ProCard.TabPane>
  <ProCard.TabPane key="tab2" tab="Tab 2">Content 2</ProCard.TabPane>
</ProCard>
```

### StatisticCard

```jsx
const { StatisticCard } = InfradPro;
const { Statistic } = StatisticCard;

<StatisticCard.Group>
  <StatisticCard statistic={{ title: 'Total', value: 5846 }} />
  <StatisticCard.Divider />
  <StatisticCard statistic={{ title: 'Active', value: 3456, status: 'processing' }} />
  <StatisticCard.Divider />
  <StatisticCard statistic={{ title: 'Error', value: 234, status: 'error' }} />
</StatisticCard.Group>
```

### CheckCard 多选卡片

```jsx
const { CheckCard } = InfradPro;

<CheckCard.Group defaultValue="A" onChange={value => console.log(value)}>
  <CheckCard title="Card A" description="Description A" value="A" />
  <CheckCard title="Card B" description="Description B" value="B" />
  <CheckCard title="Card C" description="Description C" value="C" />
</CheckCard.Group>
```

### PageContainer 页面容器

```jsx
const { PageContainer } = InfradPro;
const { Button } = Infrad;

<PageContainer
  header={{ title: 'Page Title', subTitle: 'Subtitle' }}
  extra={[<Button key="1">Secondary</Button>, <Button key="2" type="primary">Primary</Button>]}
>
  Page content here
</PageContainer>
```

### ProList

```jsx
const { ProList } = InfradPro;
const { Tag } = Infrad;

<ProList
  rowKey="id"
  dataSource={[
    { id: 1, title: 'Item 1', description: 'Description 1' },
    { id: 2, title: 'Item 2', description: 'Description 2' },
  ]}
  metas={{
    title: { dataIndex: 'title' },
    description: { dataIndex: 'description' },
    actions: { render: () => [<a key="edit">Edit</a>] },
  }}
/>
```

### EditableProTable 可编辑表格

```jsx
const { EditableProTable } = InfradPro;
const { Button } = Infrad;
// 基于 ProTable，支持行内编辑
// rowKey: string
// value / onChange: 受控数据源
// editable: {
//   type: 'single' | 'multiple',
//   editableKeys: React.Key[],
//   onChange: (keys) => void,
//   onSave: (key, data, row) => Promise,
//   onDelete: (key) => Promise,
//   actionRender: (row, config, defaultDom) => ReactNode[],
// }
// recordCreatorProps: false | { position: 'top'|'bottom', record: () => object }
// maxLength: number          - 最大行数
// columns: ProColumns[]      - 支持 editable: boolean/function、readonly: boolean

const columns = [
  { title: 'Name', dataIndex: 'name', formItemProps: { rules: [{ required: true }] } },
  { title: 'Status', dataIndex: 'state', valueType: 'select', valueEnum: {
    open: { text: 'Open', status: 'Error' },
    closed: { text: 'Closed', status: 'Success' },
  }},
  { title: 'Description', dataIndex: 'desc' },
  { title: 'Action', valueType: 'option', render: (_, record, __, action) => [
    <a key="edit" onClick={() => action?.startEditable?.(record.id)}>Edit</a>,
  ]},
];

function App() {
  const [editableKeys, setEditableKeys] = React.useState([]);
  const [dataSource, setDataSource] = React.useState([
    { id: 1, name: 'Item 1', state: 'open', desc: 'Description 1' },
    { id: 2, name: 'Item 2', state: 'closed', desc: 'Description 2' },
  ]);
  return (
    <EditableProTable
      rowKey="id"
      headerTitle="Editable Table"
      columns={columns}
      value={dataSource}
      onChange={setDataSource}
      recordCreatorProps={{ position: 'bottom', record: () => ({ id: Date.now() }) }}
      editable={{
        type: 'multiple',
        editableKeys,
        onChange: setEditableKeys,
        onSave: async (key, data) => console.log('saved', key, data),
      }}
    />
  );
}
```

### DragSortTable 拖拽排序表格

```jsx
const { DragSortTable } = InfradPro;
// 基于 ProTable，支持行拖拽排序
// dragSortKey: string         - 用于排序的字段名
// onDragSortEnd: (beforeIndex, afterIndex, newDataSource) => void
// dataSource / columns: 与 ProTable 一致

const columns = [
  { title: 'Sort', dataIndex: 'sort', width: 60, className: 'drag-visible' },
  { title: 'Name', dataIndex: 'name', className: 'drag-visible' },
  { title: 'Age', dataIndex: 'age' },
  { title: 'Address', dataIndex: 'address' },
];

<DragSortTable
  headerTitle="Drag Sort"
  columns={columns}
  rowKey="key"
  dragSortKey="sort"
  dataSource={[
    { key: '1', name: 'John', age: 32, address: 'New York' },
    { key: '2', name: 'Jim', age: 42, address: 'London' },
    { key: '3', name: 'Joe', age: 28, address: 'Sydney' },
  ]}
  onDragSortEnd={(beforeIndex, afterIndex, newData) => console.log(newData)}
/>
```

### ProLayout 布局框架

```jsx
const { ProLayout, PageContainer, ProCard } = InfradPro;
const { Button } = Infrad;
// title: string               - 应用名称
// logo: ReactNode | false
// layout: 'side' | 'top' | 'mix'
// fixSiderbar: boolean
// splitMenus: boolean          - mix 布局时拆分菜单
// siderMenuType: 'group' | 'sub'
// route: { path, routes: Array<{ path, name, icon?, component?, routes? }> }
// location: { pathname }       - 当前路径
// menuItemRender: (item, dom) => ReactNode
// avatarProps: { src, size, title, render }
// actionsRender: (props) => ReactNode[]
// token: { sider: { colorMenuBackground }, header: {...} }
// collapsedButtonRender: false | function
// menuFooterRender: (props) => ReactNode

<ProLayout
  title="My App"
  layout="mix"
  fixSiderbar
  route={{
    path: '/',
    routes: [
      { path: '/welcome', name: 'Welcome' },
      { path: '/admin', name: 'Admin',
        routes: [
          { path: '/admin/settings', name: 'Settings' },
          { path: '/admin/users', name: 'Users' },
        ],
      },
      { path: '/list', name: 'List' },
    ],
  }}
  location={{ pathname: '/welcome' }}
>
  <PageContainer header={{ title: 'Page Title' }}>
    <ProCard>Content</ProCard>
  </PageContainer>
</ProLayout>
```

### LoginForm 登录表单

```jsx
const { LoginForm, ProFormText, ProFormCheckbox } = InfradPro;
const { Space } = Infrad;
const { UserOutlined, LockOutlined } = Icons;
// logo: string | ReactNode
// title: string
// subTitle: string
// actions: ReactNode          - 其他登录方式
// onFinish: (values) => Promise
// children: ProForm 表单项

<LoginForm
  logo="https://example.com/logo.png"
  title="My App"
  subTitle="Welcome back"
  actions={<Space>Other login methods</Space>}
  onFinish={async (values) => console.log(values)}
>
  <ProFormText
    name="username"
    fieldProps={{ size: 'large', prefix: <UserOutlined /> }}
    placeholder="Username"
    rules={[{ required: true, message: 'Please enter username!' }]}
  />
  <ProFormText.Password
    name="password"
    fieldProps={{ size: 'large', prefix: <LockOutlined /> }}
    placeholder="Password"
    rules={[{ required: true, message: 'Please enter password!' }]}
  />
  <div style={{ marginBlockEnd: 24 }}>
    <ProFormCheckbox noStyle name="autoLogin">Remember me</ProFormCheckbox>
    <a style={{ float: 'right' }}>Forgot password?</a>
  </div>
</LoginForm>
```

### BetaSchemaForm JSON Schema 表单

```jsx
const { BetaSchemaForm } = InfradPro;
// 通过 JSON columns 配置生成表单，无需手写 JSX
// layoutType: 'Form' | 'ModalForm' | 'DrawerForm' | 'QueryFilter' | 'LightFilter' | 'StepsForm'
// columns: Array<ProFormColumnsType>
// onFinish: (values) => Promise
// trigger: ReactNode         - ModalForm/DrawerForm 时的触发按钮

// ProFormColumnsType:
//   title: string
//   dataIndex: string
//   valueType: 'text' | 'select' | 'date' | 'dateRange' | 'switch' | 'digit' | 'money' | ...
//   valueEnum: object
//   formItemProps: { rules, ... }
//   fieldProps: object
//   width: 'xs' | 'sm' | 'md' | 'lg' | 'xl'
//   colProps: { span }
//   initialValue: any
//   columns: ProFormColumnsType[]  - 用于 group/formList/formSet

<BetaSchemaForm
  layoutType="Form"
  onFinish={async (values) => console.log(values)}
  columns={[
    { title: 'Title', dataIndex: 'title', formItemProps: { rules: [{ required: true }] } },
    { title: 'Status', dataIndex: 'state', valueType: 'select', valueEnum: {
      open: { text: 'Open' },
      closed: { text: 'Closed' },
    }},
    { title: 'Label', dataIndex: 'label' },
    { title: 'Created', dataIndex: 'created_at', valueType: 'date' },
  ]}
/>
```

### ProFormList 动态表单列表

```jsx
const { ProForm, ProFormList, ProFormText, ProFormGroup } = InfradPro;
// ProFormList:
//   name: string | string[]     - 字段名
//   label: string
//   initialValue: Array<object>
//   creatorButtonProps: { creatorButtonText, position }
//   min / max: number            - 最小/最大行数
//   copyIconProps / deleteIconProps: false | object
//   itemContainerRender: (doms) => ReactNode
//   alwaysShowItemLabel: boolean

<ProForm onFinish={async (values) => console.log(values)}>
  <ProFormList
    name="users"
    label="User List"
    initialValue={[{ name: 'John' }]}
  >
    <ProFormGroup>
      <ProFormText name="name" label="Name" rules={[{ required: true }]} />
      <ProFormText name="email" label="Email" />
    </ProFormGroup>
  </ProFormList>
</ProForm>
```

### ProFormFieldSet 表单字段集

```jsx
const { ProFormFieldSet, ProFormText, ProFormSelect, LightFilter } = InfradPro;
// name: string | string[]
// label: string
// transform: (value) => object   - 提交时转换值
// children: 多个 ProForm 子组件（值以数组形式合并）

<LightFilter>
  <ProFormFieldSet
    label="Filter"
    name="filter"
    lightProps={{ labelFormatter: (value) => value.join(' ') }}
  >
    <ProFormSelect valueEnum={{ Like: 'Contains', Eq: 'Equals' }} />
    <ProFormText placeholder="Enter value" />
  </ProFormFieldSet>
</LightFilter>
```

### ProSkeleton 骨架屏

```jsx
const { ProSkeleton } = InfradPro;
// type: 'list' | 'result' | 'descriptions'
// active: boolean

<ProSkeleton type="list" />
<ProSkeleton type="result" />
<ProSkeleton type="descriptions" />
```

### ProField 通用字段

```jsx
const { ProFormField } = InfradPro;
// mode: 'read' | 'edit'
// valueType: 全部 valueType 类型
// text: any                 - read 模式下的值
// fieldProps: object

// 常用 valueType:
// 'text', 'password', 'money', 'index', 'indexBorder',
// 'option', 'textarea', 'date', 'dateWeek', 'dateMonth', 'dateQuarter', 'dateYear',
// 'dateRange', 'dateTime', 'dateTimeRange', 'time', 'timeRange',
// 'select', 'checkbox', 'rate', 'radio', 'radioButton', 'switch',
// 'progress', 'percent', 'digit', 'digitRange', 'second',
// 'code', 'jsonCode', 'avatar', 'image', 'color',
// 'cascader', 'treeSelect', 'fromNow', 'segmented'

<ProFormField mode="read" valueType="money" text={1234.56} />
<ProFormField mode="read" valueType="date" text={Date.now()} />
<ProFormField mode="read" valueType="progress" text={60} />
```

---

## Icons 图标

```jsx
// 用法统一为：从 Icons 解构后作为 JSX 组件使用
const { SearchOutlined, PlusOutlined, DeleteOutlined, EditOutlined } = Icons;

<SearchOutlined />
<PlusOutlined style={{ fontSize: 24, color: '#1677ff' }} />

// 自定义样式
<EditOutlined style={{ fontSize: 20, color: '#52c41a' }} />
<DeleteOutlined style={{ fontSize: 20, color: '#ff4d4f' }} />

// 常用图标列表：
// 方向类：UpOutlined, DownOutlined, LeftOutlined, RightOutlined, ArrowLeftOutlined, ArrowRightOutlined
// 操作类：SearchOutlined, PlusOutlined, DeleteOutlined, EditOutlined, CopyOutlined, DownloadOutlined, UploadOutlined, SyncOutlined, ReloadOutlined, SettingOutlined, FilterOutlined, ExportOutlined, ImportOutlined, SaveOutlined, CloseOutlined, CheckOutlined
// 状态类：InfoCircleOutlined, WarningOutlined, CheckCircleOutlined, CloseCircleOutlined, ExclamationCircleOutlined, QuestionCircleOutlined, LoadingOutlined
// 展示类：EyeOutlined, EyeInvisibleOutlined, StarOutlined, StarFilled, HeartOutlined, HeartFilled, LikeOutlined, LikeFilled, UserOutlined, TeamOutlined, HomeOutlined, MailOutlined, PhoneOutlined, CalendarOutlined, ClockCircleOutlined, FileOutlined, FolderOutlined, PictureOutlined, LinkOutlined, BellOutlined, LockOutlined, UnlockOutlined, CloudOutlined, DatabaseOutlined, ApiOutlined, CodeOutlined, BugOutlined, RocketOutlined, ThunderboltOutlined, FireOutlined, GlobalOutlined
// 后缀规则：Outlined（线框）、Filled（实心）、TwoTone（双色）
```

---

## SpaceBiz 业务组件

> SpaceBiz 组件通过 `SpaceBiz` 命名空间访问。组件分为三个子命名空间：
> - `SpaceBiz.ProductComponentPage`（页面级组件）：PageContainer, Table (SpaceProTable), Navigation, ActionButtons, MetaInfo
> - `SpaceBiz.CommonOperation`（通用操作组件）：DeleteButton, FormModal, StepsFormModal, FormPage, StepsFormPage, TagDiff, TableDiff, DescriptionsDiff, SideBySideDiff, CodeDiff
> - `SpaceBiz.AIExperience`（AI 体验组件）：AIAlert, AIButton, AICard, AIContentIndicator, AIToolCalling, AIIcons, AIColorTokens
>
> 也可以直接使用顶级导出如 `SpaceBiz.SpaceProTable`、`SpaceBiz.SpaceDeleteButton` 等。

### SpacePageContainer 页面容器

```jsx
const { ProductComponentPage } = SpaceBiz;
const { PageContainer, ActionButtons } = ProductComponentPage;
// 基于 InfradPro PageContainer 封装，标题区布局优化
// Props 与 InfradPro PageContainer 一致
// header: { title, subTitle, extra, children }

<PageContainer
  header={{
    title: 'Page Title',
    subTitle: 'Description text',
    extra: (
      <ActionButtons
        primaryKey="create"
        buttonGroup={[
          { children: 'Settings', buttonKey: 'settings' },
          { children: 'Create', buttonKey: 'create' },
        ]}
      />
    ),
  }}
>
  Page content here
</PageContainer>
```

### SpaceNavigation 导航面包屑

```jsx
const { ProductComponentPage } = SpaceBiz;
const { Navigation } = ProductComponentPage;
// items: Array<{ title: ReactNode }>
// separator: ReactNode
// openInNewWindow: boolean

<Navigation
  items={[
    { title: 'Home' },
    { title: <a href="">Application Center</a> },
    { title: <a href="">Application List</a> },
    { title: 'Current App' },
  ]}
/>
```

### SpaceActionButtons 操作按钮组

```jsx
const { ProductComponentPage } = SpaceBiz;
const { ActionButtons } = ProductComponentPage;
// buttonGroup: Array<IButtonGroup>  - 按钮列表
// primaryKey: string                - 主按钮的 buttonKey，该按钮会渲染为 type="primary"
// buttonType: ButtonType            - 统一设置所有按钮的 type（如 'link'）
// buttonSize: SizeType              - 统一设置所有按钮的 size
// externalButtonNum: number         - 外部显示的按钮数量，超出的收入下拉菜单

// IButtonGroup 字段：
//   buttonKey: string               - 唯一标识
//   children: ReactNode             - 按钮文字
//   hidden: boolean                 - 是否隐藏
//   disabled: boolean
//   tooltipProps: { title }         - 禁用时的提示
//   renderButton: (open) => ReactNode  - 自定义渲染
//   onClick: () => void
//   + 继承 Infrad ButtonProps

// 页面标题栏按钮
<ActionButtons
  primaryKey="create"
  buttonGroup={[
    { children: 'Export', buttonKey: 'export' },
    { children: 'Settings', buttonKey: 'settings' },
    { children: 'Create', buttonKey: 'create' },
  ]}
/>

// 表格行内操作（链接样式、小尺寸）
<ActionButtons
  buttonType="link"
  buttonSize="small"
  buttonGroup={[
    { children: 'Detail', buttonKey: 'detail' },
    { children: 'Edit', buttonKey: 'edit' },
    { children: 'Delete', buttonKey: 'delete' },
  ]}
/>
```

### SpaceProTable 增强表格

```jsx
const { ProductComponentPage } = SpaceBiz;
const { Table, ActionButtons } = ProductComponentPage;
// 基于 InfradPro ProTable 封装，增加以下特有 Props：
// generalSearch: boolean            - 启用通用搜索框
// showRefreshIntervalSetting: boolean - 显示刷新间隔设置
// polling: number                   - 轮询间隔（ms），0 为不轮询
// showUpdateTime: boolean           - 显示最后更新时间
// defaultSortForDigit: boolean      - 数字列默认可排序
// defaultSortForDate: boolean       - 日期列默认可排序
// filterSetting: { onClick }        - 筛选设置
// addFilter: { render }             - 自定义添加筛选
// quickFilterState / aggregatedData / aggregatedDataGroup 等

// 其余 Props 与 InfradPro ProTable 一致

const columns = [
  { title: 'Instance', dataIndex: 'instance', copyable: true },
  { title: 'Status', dataIndex: 'status', valueEnum: {
    Success: { text: 'Success', status: 'Success' },
    Failed: { text: 'Failed', status: 'Error' },
  }},
  { title: 'Weight', dataIndex: 'weight', valueType: 'digit' },
  { title: 'Created', dataIndex: 'created', valueType: 'dateTime' },
  { title: 'Action', dataIndex: 'action', search: false,
    render: (_, record) => (
      <ActionButtons
        buttonType="link" buttonSize="small"
        buttonGroup={[
          { children: 'Detail', buttonKey: 'detail' },
          { children: 'Edit', buttonKey: 'edit' },
          { children: 'Delete', buttonKey: 'delete' },
        ]}
      />
    ),
  },
];

<Table
  columns={columns}
  rowKey="id"
  generalSearch
  showRefreshIntervalSetting
  showUpdateTime
  defaultSortForDigit
  defaultSortForDate
  toolbar={{
    title: 'Table Title',
    actions: [
      <ActionButtons
        primaryKey="create"
        buttonGroup={[
          { children: 'Export', buttonKey: 'export' },
          { children: 'Create', buttonKey: 'create' },
        ]}
      />,
    ],
  }}
  request={async (params) => {
    return { success: true, data: [...] };
  }}
/>
```

### SpaceMetaInfo 元信息面板

```jsx
const { ProductComponentPage } = SpaceBiz;
const { MetaInfo } = ProductComponentPage;
// items: Array<IMetaInfoGroup>
// overviewConfig: object            - 概览配置
// viewAllModalProps: object         - "查看全部"弹窗配置

// IMetaInfoGroup:
//   groupKey: string
//   groupTitle: ReactNode
//   groupItems: Array<IMetaInfoItem>

// IMetaInfoItem:
//   key: string
//   label: ReactNode
//   content: ReactNode
//   span: number                    - 占列数（1-3）
//   visible: boolean
//   visibleInOverview: boolean

<MetaInfo items={[
  {
    groupKey: 'basic',
    groupTitle: 'Basic Info',
    groupItems: [
      { key: 'name', label: 'Name', content: 'My Service', span: 3, visible: true, visibleInOverview: true },
      { key: 'env', label: 'ENV', content: 'Production', span: 1, visible: true, visibleInOverview: true },
      { key: 'region', label: 'Region', content: 'Singapore', span: 1, visible: true, visibleInOverview: true },
      { key: 'created', label: 'Created', content: '2024-01-15', span: 1, visible: true, visibleInOverview: true },
    ],
  },
]} />
```

### SpaceDeleteButton 删除按钮

```jsx
const { CommonOperation } = SpaceBiz;
const { DeleteButton } = CommonOperation;
// 继承 Infrad Button Props
// title: string                 - 确认弹窗标题
// description: string           - 确认弹窗描述
// onDelete: () => void | Promise  - 删除回调（返回 Promise 可延迟关闭）
// details: ReactNode            - 详情内容
// modalSize: 'small' | 'medium' | 'large'
// buttonRender: (open) => ReactNode  - 自定义触发按钮

<DeleteButton
  title="Delete the 5 Devices?"
  description="Permanently delete Device 1-5. You can't undo this action."
  onDelete={() => console.log('deleted')}
/>

// 链接按钮样式
<DeleteButton type="link" title="Delete?" description="Can't undo." />

// 自定义触发
<DeleteButton
  title="Delete?"
  description="Can't undo."
  buttonRender={(open) => <Tag color="processing" onClick={open}>Delete Tag</Tag>}
/>
```

### SpaceFormModal / SpaceStepsFormModal 表单弹窗

```jsx
const { CommonOperation } = SpaceBiz;
const { FormModal, StepsFormModal } = CommonOperation;
const { ProFormText, ProFormSelect } = InfradPro;
// 公共 Props：
// title: string
// trigger: ReactNode              - 触发按钮
// open / onOpenChange: 受控开关
// initialValues: object
// onFinish: (values) => Promise<boolean>  - 返回 true 关闭弹窗
// guideButtonProps: { guideLink }
// formProps: ProForm props
// modalProps: Modal props
// preventUnsavedExit: boolean     - 防止未保存退出
// width: number

// FormModal
<FormModal
  title="Add Domain"
  trigger={<Button type="primary">Add Domain</Button>}
  onFinish={async (values) => { console.log(values); return true; }}
  formProps={{ layout: 'vertical' }}
>
  <ProFormText name="name" label="Name" rules={[{ required: true }]} />
  <ProFormSelect name="type" label="Type" options={[
    { value: 'a', label: 'Type A' },
    { value: 'b', label: 'Type B' },
  ]} />
</FormModal>

// StepsFormModal（分步表单弹窗）
// StepsFormModal.StepForm: title（步骤标题）+ children（表单内容）
<StepsFormModal
  title="Create Workflow"
  trigger={<Button type="primary">Create</Button>}
  onFinish={async (values) => { console.log(values); return true; }}
>
  <StepsFormModal.StepForm title="Basic Info">
    <ProFormText name="name" label="Name" rules={[{ required: true }]} />
  </StepsFormModal.StepForm>
  <StepsFormModal.StepForm title="Configuration">
    <ProFormSelect name="env" label="Environment" options={['test', 'staging', 'production']} />
  </StepsFormModal.StepForm>
</StepsFormModal>
```

### SpaceFormPage / SpaceStepsFormPage 表单页

```jsx
const { CommonOperation } = SpaceBiz;
const { FormPage, StepsFormPage } = CommonOperation;
const { ProFormText, ProFormSelect } = InfradPro;
// Props 与 FormModal 类似，另有：
// navigationProps: { items }     - 面包屑
// pageContainerProps: object     - 页面容器配置

// FormPage
<FormPage
  title="Create Service"
  navigationProps={{ items: [{ title: 'Home' }, { title: 'Create' }] }}
  onFinish={async (values) => { console.log(values); return true; }}
>
  <ProFormText name="name" label="Service Name" rules={[{ required: true }]} />
</FormPage>

// StepsFormPage（分步表单页，同理）
<StepsFormPage
  title="Create Workflow"
  onFinish={async (values) => { console.log(values); return true; }}
>
  <StepsFormPage.StepForm title="Step 1">...</StepsFormPage.StepForm>
  <StepsFormPage.StepForm title="Step 2">...</StepsFormPage.StepForm>
</StepsFormPage>
```

### SpaceTagDiff 标签对比

```jsx
const { SpaceTagDiff } = SpaceBiz;
// 或 const { CommonOperation } = SpaceBiz; const { TagDiff } = CommonOperation;
// label: ReactNode              - 标签名
// before: any                   - 变更前值
// after: any                    - 变更后值
// render: (value) => ReactNode  - 自定义渲染
// isEqual: (a, b) => boolean    - 自定义相等判断
// bordered: boolean
// mode: 'side-by-side' | 'inline'
// separator: ReactNode

// 自动推断变更类型：
//   有 before + after 且不同 → 编辑（黄色）
//   仅 before → 删除（红色）
//   仅 after → 新增（绿色）
//   before === after → 未变

<SpaceTagDiff label="Name" before="old-name" after="new-name" />
<SpaceTagDiff label="Deleted Field" before="value" />
<SpaceTagDiff label="New Field" after="value" />
<SpaceTagDiff label="Unchanged" before="same" after="same" />
```

### SpaceTableDiff 表格对比

```jsx
const { SpaceTableDiff } = SpaceBiz;
// 基于 Infrad Table 封装
// diffData: { before: Array, after: Array }  - 前后数据，通过 rowKey 匹配行
// columns: Array<TableDiffColumn>            - 扩展了 isEqual 字段
// filters: object
// title: () => ReactNode

// TableDiffColumn 扩展字段：
//   isEqual: (val1, val2, record1?, record2?) => boolean  - 自定义字段相等判断

<SpaceTableDiff
  diffData={{
    before: [
      { key: 'a', name: 'Mike', age: 32 },
      { key: 'b', name: 'John', age: 42 },
    ],
    after: [
      { key: 'a', name: 'Mike', age: 33 },
    ],
  }}
  columns={[
    { title: 'Name', dataIndex: 'name', key: 'name' },
    { title: 'Age', dataIndex: 'age', key: 'age' },
  ]}
  title={() => 'Data Comparison'}
/>
```

### SpaceDescriptionsDiff 描述列表对比

```jsx
const { SpaceDescriptionsDiff } = SpaceBiz;
// 基于 Infrad Descriptions 封装
// title: ReactNode
// bordered: boolean
// column: number
// items: Array<DescriptionsDiffItem>

// DescriptionsDiffItem 扩展字段：
//   contentDiffProps: {
//     before: any,
//     after: any,
//     render: (value) => ReactNode,
//     isEqual: (a, b) => boolean,
//   }
// 无 contentDiffProps 的 item 渲染为普通静态字段

<SpaceDescriptionsDiff
  title="Configuration Changes"
  bordered
  items={[
    { key: 'product', label: 'Product', children: 'Cloud Database' },
    { key: 'mode', label: 'Billing Mode',
      contentDiffProps: { before: 'Prepaid', after: 'Postpaid' },
    },
    { key: 'renewal', label: 'Auto Renewal',
      contentDiffProps: {
        before: false, after: true,
        render: (v) => v ? 'Enabled' : 'Disabled',
      },
    },
    { key: 'amount', label: 'Amount',
      contentDiffProps: { before: '$80', after: '$120' },
    },
  ]}
/>
```

### SpaceSideBySideDiff 并排对比

```jsx
const { SpaceSideBySideDiff } = SpaceBiz;
// 将多种 Diff 组件组合在并排视图中
// header: { title }
// anchor: { onClick }               - 锚点导航
// items: Array<SideBySideDiffItem>

// SideBySideDiffItem:
//   title: string
//   key: string
//   type: 'tag' | 'table' | 'descriptions'  - 或不设 type 而用 children
//   props: object                             - 对应 Diff 组件的 Props
//   children: Array<SideBySideDiffItem>      - 嵌套子项

<SpaceSideBySideDiff
  header={{ title: 'Change Review' }}
  items={[
    {
      title: 'Basic Info', key: 'basic',
      children: [
        { type: 'tag', key: 'name', props: { label: 'Name', before: 'Old', after: 'New' } },
        { type: 'tag', key: 'age', props: { label: 'Age', before: 25, after: 26 } },
      ],
    },
    {
      type: 'descriptions', key: 'config', title: 'Config',
      props: {
        bordered: true,
        items: [
          { key: 'env', label: 'Environment', contentDiffProps: { before: 'test', after: 'prod' } },
        ],
      },
    },
  ]}
/>
```

### SpaceCodeDiff 代码对比

```jsx
const { SpaceCodeDiff } = SpaceBiz;
// before: string                - 变更前代码
// after: string                 - 变更后代码
// viewMode: 'split' | 'unified'
// hideUnchangedRegions: boolean
// height: number | string
// language: string              - 语法高亮语言

<SpaceCodeDiff
  before={`function hello() {\n  return "world";\n}`}
  after={`function hello() {\n  return "hello world";\n}`}
/>
```

### SpaceAIAlert AI 提示

```jsx
const { AIExperience } = SpaceBiz;
const { AIAlert } = AIExperience;
// 类似 Infrad Alert，带 AI 渐变样式
// message: ReactNode
// description: ReactNode
// showIcon: boolean
// closable: boolean
// icon: ReactNode
// onClose: () => void
// 注意：不支持 type / banner / action

<AIAlert message="AI-Powered Feature Enabled" />
<AIAlert
  message="AI Analysis Complete"
  description="The AI model has analyzed your data and generated recommendations."
  closable
/>
```

### SpaceAIButton AI 按钮

```jsx
const { AIExperience } = SpaceBiz;
const { AIButton } = AIExperience;
// type: 'primary' | 'default' | 'text'  - 带 AI 渐变样式
// children: ReactNode
// disabled: boolean
// loading: boolean
// onClick: () => void
// block: boolean
// size: SizeType

<AIButton type="primary">Generate with AI</AIButton>
<AIButton type="default">Analyze with AI</AIButton>
<AIButton type="text">AI Suggestions</AIButton>
<AIButton type="primary" loading>Generating...</AIButton>
```

### SpaceAICard AI 卡片

```jsx
const { AIExperience } = SpaceBiz;
const { AICard } = AIExperience;
// title: ReactNode
// showIcon: boolean             - 显示 AI 图标
// icon: ReactNode
// headerVariant: string
// moreButtonProps: { items, onClick }  - 右上角更多按钮
// extra: ReactNode
// loading: boolean
// children: ReactNode

<AICard title="AI Recommendations">
  <p>Content generated by AI model.</p>
</AICard>

<AICard title="Analysis" loading>
  Loading...
</AICard>
```

### SpaceAIContentIndicator AI 内容标识

```jsx
const { AIExperience } = SpaceBiz;
const { AIContentIndicator } = AIExperience;
// children: ReactNode
// icon: ReactNode
// iconColor: string
// iconPosition: 'start' | 'end'

<AIContentIndicator>
  Automatically generated based on service configuration.
</AIContentIndicator>
```

### SpaceAIToolCalling AI 工具调用

```jsx
const { AIExperience } = SpaceBiz;
const { AIToolCalling } = AIExperience;
// 用于展示 AI Agent 工具调用的状态和结果
// Context Props:
//   status: ExecutionStatus       - 'pending' | 'running' | 'completed' | 'failed' | 'aborted'
//   toolName: string
//   args: object
//   result: any
//   error: any
// 自定义 Props:
//   titleRender: (toolName) => ReactNode
//   contentRender: (args, result) => ReactNode
//   contentCollapsible: boolean
//   maxContentHeight: number
//   actionRender: () => ReactNode

<AIToolCalling
  status="completed"
  toolName="searchDatabase"
  args={{ query: 'user count' }}
  result={{ count: 1234 }}
/>
```

### SpaceAIIcons AI 图标

```jsx
const { AIExperience } = SpaceBiz;
const { AIIcons } = AIExperience;
// 渐变 AI 主题图标集合
// 每个图标 Props: size, style, spin

// 常用图标：
// AIIcons.JarvisGradient  - Jarvis 渐变图标
// 其余详见文档 all-icons 示例

<AIIcons.JarvisGradient size={24} />
```

### SpaceAIColorTokens AI 色彩 Token

```jsx
const { AIExperience } = SpaceBiz;
const { AIColorTokens } = AIExperience;
// 不是 React 组件，是 AI 主题色彩常量对象
// 用于自定义样式时保持与 AI 组件一致的色彩体系

// 类别：Fill / Background / Border / Text / Shadows
// 示例：
// AIColorTokens.colorBgPrimary    - AI 主背景色
// AIColorTokens.colorTextPrimary  - AI 主文字色
// AIColorTokens.colorBorderAI     - AI 边框色

<div style={{ background: AIColorTokens.colorBgPrimary, padding: 16 }}>
  AI Themed Content
</div>
```
