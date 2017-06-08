# Tomasulo 模拟器

### 基本信息

- 项目地址 https://github.com/TomasuloEmuTeam/tomasulo_emu
- 实验报告 在项目根目录下 Tomasulo调度算法实验报告.docx
- 可执行文件(For Linux, 在 Ubuntu 16.04 x64 下测试通过): https://pan.baidu.com/s/1dEWK9Ex 解压后, 运行 tomasulo_emu-linux-x64/tomasulo_emu

- 组队信息:
    - 王奥丞 2014011367
    - 武伟轩 2014011375
    - 冯瑜林 2014011365

### 代码架构

- 后端为 Python 编写的模拟器部分, 通过 emulator.py 中的 Flask 启动的 Web Server 提供一套 API
- 前端为 Web 界面, 通过 AJAX 与后端通信, 将模拟器的当前状态演示出来.
- Python 部分用 pyinstaller 打包成 Native App 当做 assets, 和前端一起用 Electron 打包成一个 Native App
- Electron 启动时会先 fork 生成子进程启动 Python 的 Web Server, 并且不断尝试与其建立连接, 当确认后端已经启动后, 前端做出提示, 用户可以开始运行程序.

### 使用说明

- 启动程序后, 可以编辑汇编代码, 编辑完之后可以点击 Load 将代码加载到内存
- 点击 Run, 自动逐行执行汇编代码, 可以点击 Stop 停止
- 点击 Step, 执行一个 cycle
- 可以点击内存表格中的数值从而修改内存单元的数值, 注意, 为十六进制

