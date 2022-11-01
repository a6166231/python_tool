const {
  app,
  BrowserWindow
} = require('electron')

app.on('window-all-closed', function () {
  if (process.platform != 'darwin')
    app.quit();
});

app.on('ready', function () {
  mainWindow = new BrowserWindow({
    // width: 768,
    // height: 768,

    width: 1920,
    height: 1080,
    show: true,
    fullscreen: false,
    resizable: true,
    frame: true,
    title: "spinePreview"
  });

  mainWindow.removeMenu();

  mainWindow.on('closed', function () {
    mainWindow = null;
  });
  mainWindow.loadURL('file://' + __dirname + '/index.html').then(() => {});
});