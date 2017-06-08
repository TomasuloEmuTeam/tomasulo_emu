const electron = require('electron');
const app = electron.app;
const BrowserWindow = electron.BrowserWindow;
const path = require('path');
const { spawn } = require('child_process');

const PY_WIN_DIST_FOLDER = 'dist';
const PY_FOLDER = 'dist';
const PY_MODULE = 'emulator'; // without .py suffix

// const guessPackaged = () => {
//     const fullPath = path.join(__dirname, PY_DIST_FOLDER);
//     return require('fs').existsSync(fullPath)
// };
//
// const getScriptPath = () => {
//     if (!guessPackaged()) {
//         return path.join(__dirname, PY_FOLDER, PY_MODULE + '.py')
//     }
//     if (process.platform === 'win32') {
//         return path.join(__dirname, PY_WIN_DIST_FOLDER, PY_MODULE, PY_MODULE + '.exe')
//     }
//     return path.join(__dirname, PY_LINUX_DIST_FOLDER, PY_MODULE, PY_MODULE)
// };

const emulator = spawn(path.join(__dirname, 'dist/emulator/emulator'));
emulator.stdout.on('data', (data) => {
    console.log(`stdout: ${data}`);
});
emulator.stderr.on('data', (data) => {
    console.log(`stderr: ${data}`);
});
emulator.on('close', (code) => {
    console.log(`child process exited with code ${code}`);
});

let mainWindow = null;
const createWindow = () => {
  mainWindow = new BrowserWindow({width: 1920, height: 1080});
  console.log(__dirname);
  mainWindow.loadURL(require('url').format({
      pathname: path.join(__dirname, '/static/index.html'),
      protocol: 'file:',
      slashes: true
  }));
  // mainWindow.webContents.openDevTools();
  mainWindow.on('closed', () => {
      mainWindow = null;
  })
};
app.on('ready', createWindow);
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
      app.quit()
    }
});
app.on('activate', () => {
  if (mainWindow === null) {
      createWindow()
    }
});
