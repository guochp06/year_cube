# 人生格子 (YearCube)

一个记录人生时间的手机 App。把 75 年（900 个月）画成 900 个格子，填上你已经走过的月份。

## 功能
- 输入出生年月
- 展示 30×30 的 900 个月格子
- 年龄越小颜色越鲜绿，越老越偏灰暗

## 技术方案
- 前端：纯 HTML + CSS + JavaScript
- 打包：[Capacitor](https://capacitorjs.com) 封装成 Android APK / iOS App

## 目录结构
```
year_cube/
├── www/
│   └── index.html          # 应用页面
├── android/                # Android 原生工程
├── ios/                    # iOS 原生工程
├── assets/
│   └── icon-512.png        # 应用商店图标
├── .github/workflows/      # GitHub Actions 自动构建
├── capacitor.config.json   # Capacitor 配置
├── generate_icons.py       # 图标生成脚本
├── generate_keystore.sh    # Android 签名证书生成脚本
└── package.json
```

---

## 方式一：GitHub Actions 自动构建 APK（推荐）

### 构建 Debug 包（自己用）
1. 把整个 `year_cube` 文件夹上传到 GitHub 仓库。
2. 进入仓库的 **Actions** 页面，找到 `Build Android APK` 工作流。
3. 点击 **Run workflow**，选择 `debug`。
4. 等待几分钟后，下载 `yearcube-debug-apk` artifact，里面就是 `app-debug.apk`。
5. 把 APK 传到手机里安装即可。

### 构建 Release 包（上架应用商店）
Release 包需要签名证书，步骤如下：

#### 1. 本地生成签名证书
```bash
./generate_keystore.sh
```
这会在当前目录生成 `release.keystore` 文件。请**妥善保管**此文件和密码，丢失后将无法更新已上架的 App！

#### 2. 对证书进行 Base64 编码
```bash
# macOS
base64 -i release.keystore | pbcopy

# Linux
base64 -i release.keystore

# Windows (PowerShell)
[Convert]::ToBase64String([IO.File]::ReadAllBytes("release.keystore")) | Set-Clipboard
```

#### 3. 在 GitHub 仓库添加 Secrets
进入仓库 **Settings → Secrets and variables → Actions → New repository secret**，添加以下 4 个 Secrets：

| Secret 名称 | 内容 |
|------------|------|
| `ANDROID_KEYSTORE_BASE64` | 上面 Base64 编码后的字符串 |
| `ANDROID_KEYSTORE_PASSWORD` | 你的 keystore 密码 |
| `ANDROID_KEY_ALIAS` | 你的 key 别名（默认是 `yearcube`）|
| `ANDROID_KEY_PASSWORD` | 你的 key 密码 |

#### 4. 运行 Release 构建
1. 进入仓库 **Actions** 页面，找到 `Build Android APK`。
2. 点击 **Run workflow**，选择 `release`。
3. 等待构建完成后，下载 `yearcube-release-apk` artifact，里面就是签名后的 `app-release.apk`。

---

## 方式二：本地 Android Studio 构建

需要安装：
- Node.js 18+
- Android Studio（带 Android SDK）

### Debug 包
```bash
# 1. 安装依赖
npm install

# 2. 同步资源到 Android 工程
npx cap sync android

# 3. 用 Android Studio 打开 android 文件夹
npx cap open android

# 4. 在 Android Studio 里点击 Build → Build Bundle(s) / APK(s) → Build APK(s)
```
生成的 APK 路径：
```
android/app/build/outputs/apk/debug/app-debug.apk
```

### Release 包（带签名）
```bash
# 1. 生成签名证书（只需做一次）
./generate_keystore.sh

# 2. 设置环境变量并构建
export ANDROID_KEYSTORE_FILE=$(pwd)/release.keystore
export ANDROID_KEYSTORE_PASSWORD=yearcube123
export ANDROID_KEY_ALIAS=yearcube
export ANDROID_KEY_PASSWORD=yearcube123

cd android
./gradlew assembleRelease
```
生成的 APK 路径：
```
android/app/build/outputs/apk/release/app-release.apk
```

---

## 方式三：命令行构建（需配置 JDK + Android SDK）

```bash
npm install
npx cap sync android
cd android
chmod +x gradlew
./gradlew assembleDebug      # Debug 包
./gradlew assembleRelease    # Release 包（需先配置签名）
```

---

## iOS 版本构建

### 方式一：本地 Xcode 构建（推荐）

需要：
- macOS 电脑
- 安装 Xcode（从 Mac App Store 下载）
- Node.js 18+

#### 构建步骤
```bash
# 1. 安装依赖
npm install

# 2. 同步资源到 iOS 工程
npx cap sync ios

# 3. 用 Xcode 打开 iOS 工程
npx cap open ios
```

然后在 Xcode 中：
1. 左侧选中 `App` 项目
2. 在 `Signing & Capabilities` 中选择你的 Apple ID Team（个人 Apple ID 可免费用于真机调试）
3. 顶部选择你的 iPhone 或某个 iOS Simulator
4. 点击 ▶️ 运行按钮

#### 关于 iOS 分发
- **自己用 / 给朋友用**：用 Xcode 连上 iPhone 直接运行即可（免费 Apple ID，7 天需重签）
- **上架 App Store**：需要 Apple Developer 账号（$99/年），并在 App Store Connect 创建应用记录

### 方式二：GitHub Actions 自动构建

仓库里已经配置了 `Build iOS App` 工作流，使用 macOS runner 运行：
1. 构建 iOS Simulator 版本（验证编译通过）
2. 尝试打包 Archive（供后续分发使用）

**注意**：GitHub Actions 无法直接生成可安装的 `.ipa` 文件给真机用，因为 iOS 真机分发必须配置 Apple 开发者证书和 Provisioning Profile。如果你需要自动分发到 TestFlight 或 App Store，建议结合 [fastlane](https://fastlane.tools) 使用。

---

## 上架应用商店 checklist

如果你要把 App 上传到华为应用市场、小米应用商店、Google Play 等，还需要准备以下内容：

- [x] **App 名称**：人生格子 / YearCube
- [x] **应用图标**：已生成各尺寸 PNG 和 512x512 商店图标（`assets/icon-512.png`）
- [x] **应用截图**：手动截取 3~5 张手机界面截图
- [x] **应用简介**：
  > 人生不过 900 个月。输入你的出生年月，看看已经走过了多少格子。每一个小格子代表一个月，颜色会随着岁月渐深。愿你珍惜时间，活在当下。
- [x] **隐私政策**：需要一份简单的隐私政策网页（说明本 App 不收集用户数据）
- [ ] **软件著作权**：国内部分市场可能需要
- [x] **Release 签名 APK**：按上面步骤生成

### 隐私政策示例
你可以把以下内容放到 GitHub Pages 或任意网页上：

```
隐私政策

人生格子（YearCube）尊重用户隐私。
本应用不会在未经用户同意的情况下收集、存储或分享任何个人信息。
应用仅在本地设备上运行，不需要网络权限来传输个人数据。

如有问题，请联系：your-email@example.com
```

---

## 修改图标

如果需要重新生成应用图标，可以修改 `generate_icons.py` 中的颜色和图案，然后运行：

```bash
python3 generate_icons.py
```

这会自动更新 Android 和 iOS 的应用图标。

---

## 常见问题

**Q: 安装时提示「安装包解析失败」？**
A: 请确保 APK 完整下载，且手机允许安装「未知来源」应用。

**Q: 图标没有变化？**
A: Android 系统可能会缓存图标。卸载旧 App 或清除桌面启动器缓存后重试。

**Q: 月份计算不准确？**
A: 算法按「已经完整度过的月份」计算，不包含当前正在进行的月份。例如 25 年 12 月出生，到 26 年 4 月，已完整度过 12、1、2、3 月，共 4 个月。
