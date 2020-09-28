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
        show: false,
        width: 1600,
        height: 944,

        // resizable: false,
        // frame: false,
        minWidth: 830,
        // minHeight: 944,


// Скрыть меню
        autoHideMenuBar: true,

        webPreferences: {
            nodeIntegration: true
        }
    })

    // mainWindow.maximize();
    mainWindow.show()
    // and load the index.html of the app.
    mainWindow.loadFile('index.html')

    // Отображаем средства разработчика.
    // mainWindow.webContents.openDevTools()



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
            label: 'info',
            click() {
                createInfo();
            //     // shell.openExternal('C:\\Users\\Admin\\Desktop\\electron\\program2\\info.html')
            }
        }
    ])


    Menu.setApplicationMenu(menu);
}


// function createInfo(){
//     info = new BrowserWindow({
//         width: 500,
//         height: 400,
//
//         webPreferences: {
//             nodeIntegration: true
//         }
//     })
//
//     // and load the index.html of the app.
//     info.loadFile('info.html')
//
//     // Отображаем средства разработчика.
//     // mainWindow.webContents.openDevTools()
//
//     // Будет вызвано, когда окно будет закрыто.
//     info.on('closed', () => {
//         // Разбирает объект окна, обычно вы можете хранить окна
//         // в массиве, если ваше приложение поддерживает несколько окон в это время,
//         // тогда вы должны удалить соответствующий элемент.
//         info = null
//
//     })
// }



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
const ipc = require('electron').ipcMain
const dialog = require('electron').dialog
ipc.on('open-file-dialog-image', function (event) {
    dialog.showOpenDialog({
        properties: ['openFile'],
        // defaultPath : "images\\nailImages",
        filters :[
            {name: 'Images', extensions: ['jpg', 'png', 'gif']},
            {name: 'All files', extensions: ['*'] }
        ]

    }, function (files) {
        if (files) event.sender.send('make_image', files)
    })
})

ipc.on('open-file-dialog-mask', function (event) {
    dialog.showOpenDialog({
        properties: ['openFile'],
        // defaultPath : "images\\nailImages",
        filters :[
            {name: 'Images', extensions: ['jpg', 'png', 'gif']},
            {name: 'All files', extensions: ['*'] }
        ]

    }, function (files) {
        if (files) event.sender.send('make_mask', files)
    })
})

    // mainWindow.webContents.session.clearCache()

// В этом файле вы можете включить код другого основного процесса
// вашего приложения. Можно также поместить их в отдельные файлы и применить к ним require.