// // note that the fs package does not exist on a normal browser
// //a dialog box module from electron
// const { dialog } = require('electron').remote;
// const {ipcRenderer} = require('electron');
//
// // Also note that document does not exist in a normal node environment
// // button click event
// document.getElementById("mybutton").addEventListener("click", () => {
//     const data = "Successfully wrote to the desktop"; // the data we want to save to the desktop
//     console.log("dialog was opened")
//     //launch save dialog window
//
//         var path = dialog.showOpenDialogSync({
//             defaultPath : "C:\\Users\\Admin\\Desktop\\nails",
//             filters :[
//                 {name: 'Images', extensions: ['jpg', 'png', 'gif']},
//                 {name: 'All files', extensions: ['*'] }
//             ]
//         });
//
//         ipcRenderer.send('filechanged', path[0]);
// });
//
// ipcRenderer.on('changer', (e, args) => {
//     console.log('from renderer: ' + args.toString())
//     const docbody = document.getElementById("bodyback");
//     docbody.source = args.toString();
//     window.location.reload()
// })






