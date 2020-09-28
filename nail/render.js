const { ipcRenderer } = require('electron')
const fs = require('fs');
const path = require('path')
const {dialog} = require("electron")
var myappPath = 'default';
var exec = require('child_process').exec;

ipcRenderer.on('appPath', ((event, msg) => {
    myappPath = msg
    // console.log(myappPath)
}));

ipcRenderer.on('errorImage', (event, msg ) => {
    console.log(msg)
});

function refreshScreen() {
    window.location.reload()
}

// const { ipcRenderer } = require('electron')

function copyNail1() {
    ipcRenderer.send('shotNail1', 'copyimage')
}

function copyNail2() {
    ipcRenderer.send('shotNail2', 'copyimage')
}

function copyNail3() {
    ipcRenderer.send('shotNail3', 'copyimage')
}

function copyNail4() {
    ipcRenderer.send('shotNail4', 'copyimage')
}

function copyNail5() {
    ipcRenderer.send('shotNail5', 'copyimage')
}


function getWindowWidth() {
    return window.innerWidth || document.body.clientWidth;
}







// ВКЛЮЧЕНИЕ ВИДЕОПОТОКА

var Gstream;

function enableCamera() {
    ipcRenderer.send('giveMePath', 'pathToImage')
    // Grab elements, create settings, etc.
    var video = document.getElementById('video');
    // Get access to the camera!
    if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        // Not adding `{ audio: true }` since we only want video now
        navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
            //video.src = window.URL.createObjectURL(stream);
            Gstream = stream;
            console.log(Gstream);
            video.srcObject = stream;
            video.play();
        });
    }
}


// ФОТОГРАФИРОВАНИЕ НОГТЕЙ
const ipc = require('electron').ipcRenderer
const selectDirBtn = document.getElementById('nail1')

selectDirBtn.addEventListener('click', function (event) {
    ipc.send('open-file-dialog')
});

//Getting back the information after selecting the file

const delay = ms => {
    return new Promise(r => setTimeout(() => r(), ms))
}

ipc.on('nail1', function (event, path) {

//do what you want with the path/file selected, for example:
    console.log(`${path}`);
    fs.copyFile(`${path}`, 'images\\current1.jpg', (err) => {
        if (err) throw err;
        console.log('Image was copy');
    });
    setTimeout(copy1, 300);
    // setTimeout(ch1, 1500)

    async function delay_image() {
        var flag = true;
        let picture1 = document.getElementById("nailPicture1");
        while (flag){
            try {
                await delay(500);
                ch1();
            } catch (err) {
                // console.log(err);
                flag = false
            }
        }
    }
    delay_image()
});

function copy1() {
    var res = exec('python crop.py');
    // console.log(myappPath)
    res.stdout.on('data', function(data) {
        console.log(`${data}`);
    })
}
// function ch2() {
//     setTimeout(ch1, 200)
// }
function ch1(){
    let picture1 = document.getElementById("nailPicture1");
    picture1.innerHTML = "<img src=\"" + myappPath + "\\images\\resize1.jpg\"  style='background-size: 100%; width: 100%; height: 100%; border-radius: 2px;' onerror=\"this.src='image1.png'; this.style='border-radius: 2px;'\"/>"
}

// function shotNail1() {
//
//
//     var res = exec('python crop.py');
//     // console.log(myappPath)
//     res.stdout.on('data', function(data) {
//         console.log(`${data}`);
//     })
//
//
//     function ch1(){
//         let picture1 = document.getElementById("nailPicture1");
//         picture1.innerHTML = "<img src=\"" + myappPath + "\\images\\resize1.jpg\" style='background-size: 100%; width: 100%; height: 100%; border-radius: 2px;' />"
//         // if(getWindowWidth() <= 1900){
//         //     picture1.innerHTML = "<img src=\"" + myappPath + "\\images\\resize1.jpg\" width='95' height='70' style='border-radius: 5px;' />"
//         // }else{
//         //     picture1.innerHTML = "<img src=\"" + myappPath + "\\images\\resize1.jpg\" width='140' height='105' style='border-radius: 5px;' />"
//         // }
//     }
//     setTimeout(ch1, 1000)
//
//
//
//     // var video = document.getElementById('video');
//     // video.srcObject = null;
//     // Gstream.getTracks().forEach(track => track.stop());
//     // setTimeout(copyNail1,100);
//     // setTimeout(enableCamera,3000);
//     // let pathToNail1 = myappPath + "\\images\\nail1.jpg";
//     // console.log(pathToNail1);
//     // // document.getElementById("nailPicture1").src = pathToNail1
//     // function p1(){
//     //     let picture1 = document.getElementById("nailPicture1");
//     //     picture1.innerHTML = "<img src=\"" + myappPath + "\\images\\nail1.jpg\" width='95' height='70' style='border-radius: 5px;' />"
//     //     // picture1.innerHTML = <img src="images/nail1.jpg" alt="">
//     //     // console.log(a)
//     // }
//     // setTimeout(p1,3110)
// }

function shotNail2() {
    var video = document.getElementById('video');
    video.srcObject = null;
    Gstream.getTracks().forEach(track => track.stop());
    setTimeout(copyNail2,300);
    setTimeout(enableCamera,3000);
    function p2() {
        let picture2 = document.getElementById("nailPicture2");
        picture2.innerHTML = "<img src=\"" + myappPath + "\\images\\resize1.jpg\" style='background-size: 100%; width: 100%; height: 100%; border-radius: 2px;' />"
    }
    setTimeout(p2,3400)

}

function shotNail3() {
    var video = document.getElementById('video');
    video.srcObject = null;
    Gstream.getTracks().forEach(track => track.stop());
    setTimeout(copyNail3,100);
    setTimeout(enableCamera,3000);
    function p3() {
        let picture3 = document.getElementById("nailPicture3");
        picture3.innerHTML = "<img src=\"" + myappPath + "\\images\\nail3.jpg\" style='background-size: 100%; width: 100%; height: 100%; border-radius: 2px;' />"
    }
    setTimeout(p3,3110)
}

function shotNail4() {
    var video = document.getElementById('video');
    video.srcObject = null;
    Gstream.getTracks().forEach(track => track.stop());
    setTimeout(copyNail4,100);
    setTimeout(enableCamera,3000);
    function p4() {
        let picture4 = document.getElementById("nailPicture4");
        picture4.innerHTML = "<img src=\"" + myappPath + "\\images\\nail4.jpg\" style='background-size: 100%; width: 100%; height: 100%; border-radius: 2px;' />"
    }
    setTimeout(p4,3110)
}

function shotNail5() {
    var video = document.getElementById('video');
    video.srcObject = null;
    Gstream.getTracks().forEach(track => track.stop());
    setTimeout(copyNail5,100);
    setTimeout(enableCamera,3000);
    function p5() {
        let picture5 = document.getElementById("nailPicture5");
        picture5.innerHTML = "<img src=\"" + myappPath + "\\images\\nail5.jpg\" style='background-size: 100%; width: 100%; height: 100%; border-radius: 2px;' />"
    }
    setTimeout(p5,3110)
}




// БЛОК БОЛЬШОЙ КАРТИНКИ

var distrofia = 0, gribok = 0, normal = 0



function createBigPicture() {
    let bigPicture = document.getElementById("big_nail");
    let bolezni = fs.readFileSync("bolezni.txt", "utf8");

    let folderPath = myappPath + '\\images'
    // let path_to_image = fs.readdirSync(folderPath)
    // console.log(path_to_image[2])
    // let numbers = path_to_image[2].split("[")
    let numbers = bolezni.split("[")

    distrofia = numbers[1].split(']').slice(0,1)*100
    console.log(distrofia)
    gribok = numbers[2].split(']').slice(0,1)*100
    console.log(gribok)
    normal = numbers[3].split("]").slice(0,1)*100
    console.log(normal)
    //
    let text = 'Дистрофия: ' + distrofia + '%   Грибок: ' + gribok + '%' + '  Здоров: ' + normal + '%'



    // bigPicture.innerHTML = "<div style='position: absolute; background: rgba(238,238,238,0.5); width: 240px; border-radius: 7px; border-right: 1px solid #a9a9a9; border-bottom: 1px solid #a9a9a9;  padding-left: 40px; color: #555555; font-size: 30px; font-style: italic;'></div> <img src=\"" + myappPath + "\\images\\relize.jpg\"/ style='background-size: 100%; width: 100%; height: 100%; background-color: #fff; border-radius: 6px;'  alt=\"обрезок\">"
    // bigPicture.innerHTML = "<div style='position: absolute; top: 600px; background: rgba(238,238,238,0.5); height: 48px; width: 648px; margin-left: -3px; border-radius: 7px; border: 3px solid #333;text-align: center; color: #333; font-size: 16px;'><p>" + text +" </p></div> <img src=\"" + myappPath + "\\images\\relize.jpg\"/ style='background-size: 100%; width: 100%; height: 100%; background-color: #fff; border-radius: 3px;'  alt=\"обрезок\">"
    bigPicture.innerHTML = "<div style='position: absolute; bottom: -3px; background: rgba(238,238,238,0.5); height: 48px; width: 100%; margin-left: -3px; border-radius: 7px; border: 3px solid #333;text-align: center; color: #333; font-size: 16px;'><p>" + text +" </p></div> <img src=\"" + myappPath + "\\images\\relize.jpg\"/ style='background-size: 100%; width: 100%; height: 100%; background-color: #fff; border-radius: 3px;'  alt=\"обрезок\">"

}

function wait() {
    let bigPicture = document.getElementById("big_nail");
    bigPicture.innerHTML = "<img src=\"images\\animation.gif\" style='background-size: 100%; height: 100%;  width: 100%; background-color: #fff; border-radius: 6px; '  alt=\"обрезок\">";


}

function analysis() {
    wait()
    var res2 = exec('python nails\\infer.py');

    res2.stdout.on('data', function(data) {
        console.log(`${data}`);
        if (data == 6) {
            setTimeout(createBigPicture, 100)
        }
    })
    // var res = exec('C:\\Users\\Admin\\AppData\\Local\\Programs\\Python\\Python37-32\\python.exe C:\\Users\\Admin\\Desktop\\RightVersion\\Electron\\nails\\nail\\crop.py');
    // setTimeout(createBigPicture, 3000)
}


// ОКНО ИНФОРМАЦИИ

function getInfo() {
    // console.log(myappPath)
    if (distrofia > 50 ){
        information = window.open("distrofia.html","information","height=1032,width=768")
    }
    else if (gribok > 50){
        information = window.open("gribok.html","information","height=1032,width=768")
    }
    else{
        information = window.open("normal.html","information","height=1032,width=768")
    }
}



// ОЧИСТКА

function clearImages() {
    // let bigPicture = document.getElementById("big_nail");
    // bigPicture.innerHTML = "";
    // let picture1 = document.getElementById("nailPicture1");
    // picture1.innerHTML = "";
    // let picture2 = document.getElementById("nailPicture2");
    // picture2.innerHTML = "";
    // let picture3 = document.getElementById("nailPicture3");
    // picture3.innerHTML = "";
    // let picture4 = document.getElementById("nailPicture4");
    // picture4.innerHTML = "";
    // let picture5 = document.getElementById("nailPicture5");
    // picture5.innerHTML = "";
    const directory = myappPath + "\\images";
    console.log(directory)

    fs.readdir(directory, (err, files) => {
        if (err) throw err;

        for (const file of files) {
            fs.unlink(path.join(directory, file), err => {
                if (err) throw err;
            });
        }
    });

    // fs.unlinkSync(myappPath + "\\images\\nail1.jpg");
    // fs.unlinkSync(myappPath + "\\images\\nail2.jpg");
    // fs.unlinkSync(myappPath + "\\images\\nail3.jpg");
    // fs.unlinkSync(myappPath + "\\images\\nail4.jpg");
    // fs.unlinkSync(myappPath + "\\images\\nail5.jpg");
    refreshScreen()
}

function openNail(evt, nailName) {
    var i, tabcontent, tablinks;

    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    document.getElementById(nailName).style.display = "block";
    evt.currentTarget.className += " active";
}

function clickButton1(){
    document.getElementById('bigNailButton1').click();
}


