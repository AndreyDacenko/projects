const { app, BrowserWindow, Menu } = require('electron')
app.commandLine.appendSwitch ("disable-http-cache");
const url = require('url')
const path = require('path')
const shell = require('electron').shell
const { webContents } = require('electron')
const fs = require("fs");
const nodeWebCam = require("node-webcam");

// Храните глобальную ссылку на объект окна, если вы этого не сделаете, окно будет
// автоматически закрываться, когда объект JavaScript собирает мусор.
let mainWindow;
let info;
function createWindow () {
    // Создаём окно браузера.
    mainWindow = new BrowserWindow({
        width: 1470,
        height: 910,
        // resizable: false,
        // frame: false,
        // minHeight: 738,
        // minWidth: 1232,

// Скрыть меню
        autoHideMenuBar: true,

        webPreferences: {
            nodeIntegration: true
        }
    })

    // and load the index.html of the app.
    mainWindow.loadFile('index.html')

    // Отображаем средства разработчика.
    mainWindow.webContents.openDevTools()



    // Будет вызвано, когда окно будет закрыто.
    mainWindow.on('closed', () => {
        // Разбирает объект окна, обычно вы можете хранить окна
        // в массиве, если ваше приложение поддерживает несколько окон в это время,
        // тогда вы должны удалить соответствующий элемент.
        mainWindow = null

    })

    var menu = Menu.buildFromTemplate([
        {
            label: 'Menu',
            submenu: [

                {type: 'separator'},
                {
                    label: 'Exit',
                    click() {
                        app.quit()
                    }
                }
            ]
        },
        {
            label: 'Parameters',
            click() {
                createInfo();
                // shell.openExternal('C:\\Users\\Admin\\Desktop\\electron\\program2\\info.html')
            }
        }
    ])


    Menu.setApplicationMenu(menu);
}


function createInfo(){
    info = new BrowserWindow({
        width: 392,
        height: 490,
        resizable: false,
        autoHideMenuBar: true,
        webPreferences: {
            nodeIntegration: true
        }
    })


    // and load the index.html of the app.
    info.loadFile('tochnost.html')

    // Отображаем средства разработчика.
    // mainWindow.webContents.openDevTools()

    // Будет вызвано, когда окно будет закрыто.
    info.on('closed', () => {
        // Разбирает объект окна, обычно вы можете хранить окна
        // в массиве, если ваше приложение поддерживает несколько окон в это время,
        // тогда вы должны удалить соответствующий элемент.
        info = null

    })
}



// Этот метод будет вызываться, когда Electron закончит
// инициализацию и готов к созданию окон браузера.
// Некоторые API могут использоваться только после возникновения этого события.
app.on('ready', createWindow)

// Выходим, когда все окна будут закрыты.
app.on('window-all-closed', () => {
    // Для приложений и строки меню в macOS является обычным делом оставаться
    // активными до тех пор, пока пользователь не выйдет окончательно используя Cmd + Q
    if (process.platform !== 'darwin') {
        app.quit()
    }
})

app.on('activate', () => {
    // На MacOS обычно пересоздают окно в приложении,
    // после того, как на иконку в доке нажали и других открытых окон нету.
    if (mainWindow === null) {
        createWindow()
    }
})






const { ipcMain } = require('electron');

var options = {
    width: 1280,
    height: 720,
    quality: 100,
    delay: 0,
    saveShots: true,
    output: "jpg",
    device: false,
    callbackReturn: "location"
};
var webcam = nodeWebCam.create(options);
var myappPath = app.getPath('userData');



// ipc = electron.ipcMain;

// ipc.on('hello', (event, args) => {
//     mainWindow.webContents.send('appPath', myappPath)
//     console.log(myappPath)
//     event.sender.send('appPath',myappPath);
// });
ipcMain.on('giveMePath', (event, data) => {

    mainWindow.webContents.send('appPath', myappPath);

});

ipcMain.on('shotNail1', (event, data) => {

            var captureShot1 = () => {
                var path = (myappPath + "\\images");
                if (!fs.existsSync(path)) {
                    fs.mkdirSync(path);
                }

                webcam.capture(myappPath + "\\images\\nail1.jpg", (err) => {
                    if (!err) {
                        console.log('Image created')
                        mainWindow.webContents.send('errorImage', 'Image created');
                    }
                    console.log(err);
                    mainWindow.webContents.send('errorImage', err);
                });
            };
            captureShot1();
});

ipcMain.on('shotNail2', (event, data) => {

    var captureShot2 = () => {
        webcam.capture(myappPath + "\\images\\resize1.jpg", (err) => {
            if (!err) {
                console.log('Image created')
                mainWindow.webContents.send('errorImage', 'Image created');
            }
            console.log(err);
            mainWindow.webContents.send('errorImage', err);
        });
    };
    captureShot2();
});

ipcMain.on('shotNail3', (event, data) => {

    var captureShot3 = () => {
        webcam.capture(myappPath + "\\images\\nail3.jpg", (err) => {
            if (!err) {
                console.log('Image created')
                mainWindow.webContents.send('errorImage', 'Image created');
            }
            console.log(err);
            mainWindow.webContents.send('errorImage', err);
        });
    };
    captureShot3();
});

ipcMain.on('shotNail4', (event, data) => {

    var captureShot4 = () => {
        webcam.capture(myappPath + "\\images\\nail4.jpg", (err) => {
            if (!err) {
                console.log('Image created')
                mainWindow.webContents.send('errorImage', 'Image created');
            }
            console.log(err);
            mainWindow.webContents.send('errorImage', err);
        });
    };
    captureShot4();
});

ipcMain.on('shotNail5', (event, data) => {

    var captureShot5 = () => {
        webcam.capture(myappPath + "\\images\\nail5.jpg", (err) => {
            if (!err) {
                console.log('Image created')
                mainWindow.webContents.send('errorImage', 'Image created');
            }
            console.log(err);
            mainWindow.webContents.send('errorImage', err);
        });
    };
    captureShot5();
});


const ipc = require('electron').ipcMain
const dialog = require('electron').dialog
ipc.on('open-file-dialog', function (event) {
    dialog.showOpenDialog({
        properties: ['openFile'],
        defaultPath : "images\\nailImages",
        filters :[
            {name: 'Images', extensions: ['jpg', 'png', 'gif']},
            {name: 'All files', extensions: ['*'] }
        ]

    }, function (files) {
        if (files) event.sender.send('nail1', files)
    })
})

// mainWindow.webContents.session.clearCache()

// В этом файле вы можете включить код другого основного процесса
// вашего приложения. Можно также поместить их в отдельные файлы и применить к ним require.