from flask import Flask, request, jsonify, render_template_string
from pathlib import Path
from PIL import Image, ImageOps
from datetime import datetime
import re
import socket

app = Flask(__name__)

SAVE_DIR = Path("photos")
SAVE_DIR.mkdir(exist_ok=True)

current_code = ""
last_updated = ""

APP_AUTHOR = "Tianyu Wang"
APP_VERSION = "v1.2.0"


def safe_filename(text):
    # 防止文件名里出现 / \\ : * ? " < > | 等非法字符
    text = text.strip()
    text = re.sub(r'[\\/:*?"<>|\s]+', "_", text)
    text = text.strip("._")
    return text


def get_local_ip():
    """
    获取电脑局域网 IP，方便页面提示手机访问地址。
    如果获取失败，则返回 127.0.0.1。
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


COMMON_STYLE = """
<style>
    * {
        box-sizing: border-box;
    }

    body {
        font-family: Arial, "Microsoft YaHei", sans-serif;
        margin: 0;
        padding: 24px;
        padding-bottom: 70px;
        background: #f7f7f7;
        color: #222;
    }

    .container {
        max-width: 760px;
        margin: 0 auto;
    }

    h1 {
        font-size: 26px;
        margin: 0 0 20px 0;
    }

    h2 {
        font-size: 21px;
        margin: 0 0 14px 0;
    }

    .card {
        background: #ffffff;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 18px;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.10);
    }

    .current-code-box {
        background: #eef4ff;
        border: 2px solid #c9ddff;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 18px;
    }

    .label {
        font-size: 17px;
        color: #444;
        margin-bottom: 8px;
    }

    .current-code {
        font-size: 32px;
        font-weight: bold;
        color: #003b8e;
        word-break: break-all;
    }

    .updated-time {
        font-size: 14px;
        color: #666;
        margin-top: 8px;
    }

    input[type="text"] {
        width: 100%;
        font-size: 23px;
        padding: 15px 16px;
        border-radius: 11px;
        border: 2px solid #bbb;
        outline: none;
        margin-bottom: 14px;
    }

    input[type="text"]:focus {
        border-color: #0066cc;
        box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.15);
    }

    input[type="file"] {
        width: 100%;
        font-size: 19px;
        padding: 15px;
        border-radius: 11px;
        border: 2px dashed #999;
        background: #fafafa;
        margin-bottom: 15px;
    }

    button {
        width: 100%;
        font-size: 22px;
        font-weight: bold;
        padding: 16px;
        border: none;
        border-radius: 12px;
        background: #0066cc;
        color: white;
        cursor: pointer;
    }

    button:active {
        transform: scale(0.99);
    }

    .secondary-button {
        background: #333;
    }

    .status {
        margin-top: 12px;
        font-size: 16px;
        min-height: 22px;
        color: #0b6b0b;
    }

    .hint {
        font-size: 16px;
        line-height: 1.6;
        color: #444;
    }

    .hint strong {
        color: #000;
    }

    .footer-info {
        position: fixed;
        right: 12px;
        bottom: 10px;
        font-size: 12px;
        color: #666;
        background: rgba(255, 255, 255, 0.92);
        padding: 7px 10px;
        border-radius: 8px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.18);
        z-index: 999;
    }

    .success-title {
        font-size: 28px;
        color: #0b6b0b;
        margin-bottom: 15px;
    }

    .file-name {
        font-size: 23px;
        font-weight: bold;
        word-break: break-all;
        margin-bottom: 8px;
    }

    .file-list {
        font-size: 18px;
        line-height: 1.7;
        margin: 0;
        padding-left: 22px;
        word-break: break-all;
    }

    a.big-link {
        display: block;
        text-align: center;
        text-decoration: none;
        font-size: 21px;
        font-weight: bold;
        color: white;
        background: #0066cc;
        padding: 16px;
        border-radius: 12px;
        margin-top: 18px;
    }

    @media (max-width: 700px) {
        body {
            padding: 16px;
            padding-bottom: 70px;
        }

        h1 {
            font-size: 24px;
        }

        h2 {
            font-size: 20px;
        }

        .card {
            padding: 16px;
            border-radius: 12px;
            margin-bottom: 15px;
        }

        .current-code-box {
            padding: 16px;
            border-radius: 12px;
            margin-bottom: 15px;
        }

        .current-code {
            font-size: 28px;
        }

        input[type="text"] {
            font-size: 21px;
            padding: 14px;
        }

        input[type="file"] {
            font-size: 17px;
            padding: 14px;
        }

        button {
            font-size: 20px;
            padding: 15px;
        }

        .hint {
            font-size: 15px;
        }

        .label {
            font-size: 16px;
        }

        .updated-time {
            font-size: 13px;
        }

        .file-list {
            font-size: 16px;
        }
    }
</style>
"""


SYNC_SCRIPT = """
<script>
    const codeInput = document.getElementById("codeInput");
    const currentCode = document.getElementById("currentCode");
    const updatedTime = document.getElementById("updatedTime");
    const statusText = document.getElementById("statusText");
    const setCodeButton = document.getElementById("setCodeButton");

    let localEditing = false;

    codeInput.addEventListener("focus", function() {
        localEditing = true;
    });

    codeInput.addEventListener("blur", function() {
        localEditing = false;
    });

    codeInput.addEventListener("keydown", function(e) {
        if (e.key === "Enter") {
            setCode();
        }
    });

    setCodeButton.addEventListener("click", setCode);

    function showStatus(text, isError = false) {
        statusText.innerText = text;
        statusText.style.color = isError ? "#b00020" : "#0b6b0b";
    }

    async function setCode() {
        const code = codeInput.value.trim();

        if (!code) {
            showStatus("编号不能为空。", true);
            return;
        }

        try {
            const res = await fetch("/set_code", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ code: code })
            });

            const data = await res.json();

            if (data.ok) {
                currentCode.innerText = data.code || "未设置";
                updatedTime.innerText = data.last_updated || "";
                codeInput.value = data.code || "";
                showStatus("编号已同步：" + data.code);
            } else {
                showStatus(data.error || "设置失败。", true);
            }
        } catch (err) {
            showStatus("网络错误，无法设置编号。", true);
        }
    }

    async function refreshCode() {
        try {
            const res = await fetch("/current_code?_=" + Date.now());
            const data = await res.json();

            const newCode = data.code || "";
            const newTime = data.last_updated || "";

            currentCode.innerText = newCode || "未设置";
            updatedTime.innerText = newTime;

            if (!localEditing) {
                codeInput.value = newCode;
            }
        } catch (err) {
            // 同步失败时不打断当前操作
        }
    }

    setInterval(refreshCode, 800);
    refreshCode();
</script>
"""


PC_PAGE = """
<!doctype html>
<html lang="zh-CN">
<head>
    <meta charset="utf-8">
    <title>电脑端 - 编号控制</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    {{ common_style|safe }}
</head>
<body>
    <div class="container">
        <h1>电脑端：编号控制</h1>

        <div class="current-code-box">
            <div class="label">当前同步编号</div>
            <div class="current-code" id="currentCode">{{ current_code or "未设置" }}</div>
            <div class="updated-time" id="updatedTime">{{ last_updated }}</div>
        </div>

        <div class="card">
            <h2>修改编号</h2>
            <input
                id="codeInput"
                type="text"
                placeholder="请输入编号，例如 A00123"
                value="{{ current_code }}"
                autocomplete="off"
            >
            <button id="setCodeButton" type="button">同步编号</button>
            <div class="status" id="statusText"></div>
        </div>

        <div class="card">
            <h2>手机访问地址</h2>
            <div class="hint">
                <p>手机和电脑需要连接同一个 Wi-Fi。</p>
                <p>手机端访问：</p>
                <p><strong>http://{{ local_ip }}:5000/phone</strong></p>
                <p>备用地址：</p>
                <p><strong>http://{{ local_ip }}:5000/photo</strong></p>
            </div>
        </div>
    </div>

    <div class="footer-info">
        by: {{ author }} | {{ version }}
    </div>

    {{ sync_script|safe }}
</body>
</html>
"""


PHONE_PAGE = """
<!doctype html>
<html lang="zh-CN">
<head>
    <meta charset="utf-8">
    <title>手机端 - 拍照上传</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    {{ common_style|safe }}
</head>
<body>
    <div class="container">
        <h1>手机端：拍照上传</h1>

        <div class="current-code-box">
            <div class="label">当前同步编号</div>
            <div class="current-code" id="currentCode">{{ current_code or "未设置" }}</div>
            <div class="updated-time" id="updatedTime">{{ last_updated }}</div>
        </div>

        <div class="card">
            <h2>修改编号</h2>
            <input
                id="codeInput"
                type="text"
                placeholder="请输入编号，例如 A00123"
                value="{{ current_code }}"
                autocomplete="off"
            >
            <button id="setCodeButton" type="button">同步编号</button>
            <div class="status" id="statusText"></div>
        </div>

        <div class="card">
            <h2>拍照上传</h2>
            <form action="/upload" method="post" enctype="multipart/form-data">
                <input
                    type="file"
                    name="photo"
                    accept="image/*"
                    capture="environment"
                    required
                >
                <button type="submit" class="secondary-button">拍照后上传保存</button>
            </form>
            <div class="hint">
                <p>拍一张照片后，会自动保存 3 个文件：</p>
                <p><strong>当前编号.png</strong></p>
                <p><strong>当前编号.bmp</strong></p>
                <p><strong>当前编号.jpg</strong></p>
            </div>
        </div>
    </div>

    <div class="footer-info">
        by: {{ author }} | {{ version }}
    </div>

    {{ sync_script|safe }}
</body>
</html>
"""


SUCCESS_PAGE = """
<!doctype html>
<html lang="zh-CN">
<head>
    <meta charset="utf-8">
    <title>保存成功</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    {{ common_style|safe }}
</head>
<body>
    <div class="container">
        <div class="card">
            <div class="success-title">保存成功</div>

            <div class="label">已保存文件</div>
            <ul class="file-list">
                {% for filename in filenames %}
                    <li>{{ filename }}</li>
                {% endfor %}
            </ul>

            <br>

            <div class="label">保存位置</div>
            <div class="hint">
                <strong>{{ save_dir }}</strong>
            </div>

            <a class="big-link" href="/phone">继续拍下一张</a>
        </div>
    </div>

    <div class="footer-info">
        by: {{ author }} | {{ version }}
    </div>
</body>
</html>
"""


ERROR_PAGE = """
<!doctype html>
<html lang="zh-CN">
<head>
    <meta charset="utf-8">
    <title>操作失败</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    {{ common_style|safe }}
</head>
<body>
    <div class="container">
        <div class="card">
            <h1>操作失败</h1>
            <div class="hint">
                <strong>{{ message }}</strong>
            </div>
            <a class="big-link" href="/phone">返回手机端</a>
        </div>
    </div>

    <div class="footer-info">
        by: {{ author }} | {{ version }}
    </div>
</body>
</html>
"""


@app.route("/")
@app.route("/pc")
def index():
    return render_template_string(
        PC_PAGE,
        current_code=current_code,
        last_updated=last_updated,
        local_ip=get_local_ip(),
        author=APP_AUTHOR,
        version=APP_VERSION,
        common_style=COMMON_STYLE,
        sync_script=SYNC_SCRIPT
    )


@app.route("/phone")
@app.route("/photo")
def phone():
    return render_template_string(
        PHONE_PAGE,
        current_code=current_code,
        last_updated=last_updated,
        author=APP_AUTHOR,
        version=APP_VERSION,
        common_style=COMMON_STYLE,
        sync_script=SYNC_SCRIPT
    )


@app.route("/set_code", methods=["POST"])
def set_code():
    global current_code, last_updated

    data = request.get_json()
    code = data.get("code", "") if data else ""
    code = safe_filename(code)

    if not code:
        return jsonify({
            "ok": False,
            "error": "编号不能为空，且不能只包含非法文件名字符。"
        })

    current_code = code
    last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return jsonify({
        "ok": True,
        "code": current_code,
        "last_updated": last_updated
    })


@app.route("/current_code")
def get_current_code():
    return jsonify({
        "code": current_code,
        "last_updated": last_updated
    })


@app.route("/upload", methods=["POST"])
def upload():
    if not current_code:
        return render_template_string(
            ERROR_PAGE,
            message="电脑端或手机端还没有设置编号，请先输入编号并点击“同步编号”。",
            author=APP_AUTHOR,
            version=APP_VERSION,
            common_style=COMMON_STYLE
        )

    file = request.files.get("photo")

    if not file:
        return render_template_string(
            ERROR_PAGE,
            message="没有收到照片，请重新拍照上传。",
            author=APP_AUTHOR,
            version=APP_VERSION,
            common_style=COMMON_STYLE
        )

    try:
        img = Image.open(file.stream)

        # 修正手机照片方向
        img = ImageOps.exif_transpose(img)

        # PNG 可以保存 RGB/RGBA；JPG 和 BMP 统一使用 RGB，避免透明通道导致保存失败
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGB")

        rgb_img = img.convert("RGB")

        png_filename = f"{current_code}.png"
        bmp_filename = f"{current_code}.bmp"
        jpg_filename = f"{current_code}.jpg"

        png_path = SAVE_DIR / png_filename
        bmp_path = SAVE_DIR / bmp_filename
        jpg_path = SAVE_DIR / jpg_filename

        # 同名文件会覆盖
        img.save(png_path, "PNG")
        rgb_img.save(bmp_path, "BMP")
        rgb_img.save(jpg_path, "JPEG", quality=95, subsampling=0)

        return render_template_string(
            SUCCESS_PAGE,
            filenames=[png_filename, bmp_filename, jpg_filename],
            save_dir=SAVE_DIR,
            author=APP_AUTHOR,
            version=APP_VERSION,
            common_style=COMMON_STYLE
        )

    except Exception as e:
        return render_template_string(
            ERROR_PAGE,
            message=f"保存失败：{e}",
            author=APP_AUTHOR,
            version=APP_VERSION,
            common_style=COMMON_STYLE
        )


if __name__ == "__main__":
    local_ip = get_local_ip()

    print("服务已启动")
    print(f"电脑端地址：http://{local_ip}:5000")
    print(f"局域网地址：http://{local_ip}:5000")
    print(f"手机端地址：http://{local_ip}:5000/phone")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        use_reloader=False
    )
