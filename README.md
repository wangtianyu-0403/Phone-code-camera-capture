手机与电脑局域网拍照采集工具。电脑端和手机端可以同步修改编号，手机拍照后自动上传到电脑，并按当前编号同时保存为 PNG、BMP、JPG 三种格式。

## GitHub Repository Name

```text
phone-code-camera-capture
```

## GitHub Description

```text
A LAN-based Flask tool for syncing photo IDs between PC and phone and saving each capture as PNG, BMP, and JPG.
```

## 项目简介

本项目用于解决手机拍照采集时的文件命名和格式保存问题。

电脑端运行一个本地 Flask 服务，手机和电脑连接同一个 Wi-Fi 后，手机通过浏览器访问拍照页面。用户可以在电脑端或手机端输入编号，两端会自动同步当前编号。手机拍照上传后，电脑端会自动在 `photos` 文件夹中保存三份图片文件：

```text
当前编号.png
当前编号.bmp
当前编号.jpg
```

例如当前编号为 `A00123`，拍照上传后会生成：

```text
photos/A00123.png
photos/A00123.bmp
photos/A00123.jpg
```

## 功能特点

- 电脑端输入编号
- 手机端输入编号
- 电脑端和手机端编号自动同步
- 手机浏览器调用摄像头拍照
- 拍照后自动上传到电脑
- 同一张照片自动保存为三种格式：
  - PNG
  - BMP
  - JPG
- 文件名自动使用当前编号
- 自动修正手机照片方向
- 自动过滤 Windows 文件名非法字符
- 支持手机端 `/phone` 和 `/photo` 两个访问路径
- 右下角显示作者和版本号
- 无需开发手机 App

## 使用场景

本项目适合以下场景：

- 产品图片采集
- 样品图片采集
- 标签编号拍照
- 设备编号拍照
- 实验样本拍照
- 仓库物料拍照
- 质检图片留档
- 需要按照编号批量保存图片的工作流

## 技术栈

- Python
- Flask
- Pillow
- HTML
- CSS
- JavaScript

## 系统要求

电脑端需要安装：

- Python 3+
- Flask
- Pillow

手机端需要：

- 与电脑连接同一个 Wi-Fi
- 使用支持拍照上传的浏览器

推荐浏览器：

- Chrome
- Edge
- Safari
- 手机系统自带浏览器

## 安装步骤

### 1. 克隆项目

```bash
git clone https://github.com/your-username/phone-code-camera-capture.git
cd phone-code-camera-capture
```

如果你是直接下载代码，也可以进入项目文件夹后继续下面步骤。

### 2. 安装依赖

Windows：

```bash
py -m pip install flask pillow
```

macOS / Linux：

```bash
python3 -m pip install flask pillow
```

## 运行方式

Windows：

```bash
python app.py
```

或：

```bash
py app.py
```

macOS / Linux：

```bash
python3 app.py
```

启动成功后，终端会显示类似信息：

```text
服务已启动
电脑端地址：http://192.168.1.23:5000
局域网地址：http://192.168.1.23:5000
手机端地址：http://192.168.1.23:5000/phone
```

## 操作流程

### 1. 打开电脑端页面

在电脑浏览器中打开：

```text
http://127.0.0.1:5000
```

或打开终端中显示的局域网地址：

```text
http://电脑IP:5000
```

### 2. 设置编号

在电脑端或手机端输入编号，例如：

```text
A00123
```

然后点击：

```text
同步编号
```

电脑端和手机端都会自动显示最新编号。

### 3. 打开手机端页面

手机和电脑连接同一个 Wi-Fi 后，在手机浏览器中打开：

```text
http://电脑IP:5000/phone
```

备用地址：

```text
http://电脑IP:5000/photo
```

### 4. 手机拍照上传

在手机端点击拍照上传按钮。

拍照完成并上传后，电脑项目目录下会自动生成：

```text
photos/A00123.png
photos/A00123.bmp
photos/A00123.jpg
```

## 项目结构

```text
phone-code-camera-capture
├── app.py
├── photos/
└── README.md
```

说明：

```text
app.py      主程序文件
photos/     图片保存目录，程序启动时会自动创建
README.md   项目说明文件
```

## 文件命名规则

上传成功后，文件会使用当前同步编号作为文件名。

例如当前编号为：

```text
SAMPLE_001
```

保存结果为：

```text
SAMPLE_001.png
SAMPLE_001.bmp
SAMPLE_001.jpg
```

如果输入编号中包含 Windows 文件名非法字符，例如：

```text
A/001:23
```

程序会自动转换为安全文件名：

```text
A_001_23
```

## 注意事项

### 同名文件会覆盖

如果多次使用同一个编号拍照，旧文件会被新文件覆盖。

例如已经存在：

```text
A00123.png
A00123.bmp
A00123.jpg
```

再次用 `A00123` 上传照片后，这三个文件会被覆盖。

### 手机打不开页面时

请检查：

- 手机和电脑是否连接同一个 Wi-Fi
- 手机访问的 IP 是否正确
- Windows 防火墙是否允许 Python 访问网络
- 当前网络是否禁止设备之间互相访问
- 公司、学校、公共 Wi-Fi 可能会限制局域网访问

### 浏览器没有直接打开相机时

部分手机浏览器可能不会直接打开相机，而是弹出“拍照”或“选择图片”的菜单。请选择“拍照”。

## 版本信息

当前版本：

```text
v1.2.0
```

版本功能：

- 支持电脑端和手机端同步修改编号
- 支持手机端拍照上传
- 支持拍照后同时保存 PNG、BMP、JPG
- 支持移动端适配 UI
- 支持作者和版本号展示

## 作者

```text
Tianyu Wang
```

## License

This project is released under the MIT License.

你可以根据自己的需要修改、分发和二次开发本项目。
