const { ipcRenderer } = require('electron')
const fs = require('fs');
const path = require('path')
const {dialog} = require("electron")
var myappPath = 'default';
var exec = require('child_process').exec;
var execSync = require('child_process').execSync;
const ipc = require('electron').ipcRenderer

function load_js() {
    var head= document.getElementsByTagName('head')[0];
    // console.log(head)
    var script= document.createElement('script');
    script.src= 'script.js';
    head.appendChild(script);
}

function clickButton1(){
    document.getElementById('tab3').click();
}

const path_to_verify = __dirname

function openNail(evt, nailName) {
    var i, tabcontent, tablinks;

    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
        try {change_image_9()} catch (err) {}
        try {change_mask_9()} catch (err) {}
        try {change_attention_9()} catch (err) {}
        try {change_nondetection_9()} catch (err) {}
        try {change_neeroset_9()} catch (err) {}

    }

    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    document.getElementById(nailName).style.display = "block";
    evt.currentTarget.className += " active";

    load_js();
    setTimeout(change_image_0, 300)
    setTimeout(change_mask_0, 300)
    setTimeout(change_attention_0, 300)
    setTimeout(change_nondetection_0, 300)
    setTimeout(change_neeroset_0, 300)
}

var dict_of_statii = {
    '1': 'Корректируем размер изображений...',
    '2': 'Минимизируем погрешность смещения...',
    '3': 'Вычисляем расположение различий с оригиналом...',
    '4': 'Вычисляем расположение различий с маской...',
    '5': 'Визуализируем карту сравнений для новых элементов...',
    '6': 'Визуализируем карту сравнений для отсутствующих элементов...',
    '7': 'Вычисляем расположение существенных отличий...',
    '8': ''
};

let text = document.getElementById("progress_text");
line.style.width = 0 + '%';

function create_calc() {
    console.log('creating image')
    var res = exec('python main.pyc')
    document.getElementById('tab1').click();
    $('#tab2').prop('disabled', true);
    $('#tab3').prop('disabled', true);
    $('#tab4').prop('disabled', true);
    $('#tab5').prop('disabled', true);
    $('#make_calk').prop('disabled', true);
    res.stdout.on('data', function(data) {
        // console.log(`${data}`);
        // console.log(dict_of_statii[`${data}`.trim()]);
        text.innerHTML = "<p>" + `${dict_of_statii[`${data}`.trim()]}` + "</p>"
        line.style.width = (12.5*data) + '%';
        number.innerHTML = (12.5*data) + '%';
        // load_js();
        if (`${data}`.trim() === '8')
        {
            setTimeout(attention_image, 500)
            setTimeout(load_js, 1000)
            nondetection()
            setTimeout(change_attention_0, 1100)
            $('#tab2').prop('disabled', false);
            $('#tab3').prop('disabled', false);
            $('#tab4').prop('disabled', false);
            $('#tab5').prop('disabled', false);
            $('#make_calk').prop('disabled', false);
            // document.getElementById('target_attention').style.marginLeft = '0px';
        }
    })
}

function create_neeroset() {
    var res2 = exec('python ROI_detect.pyc')
    document.getElementById('tab5').click();
    document.getElementById('floatingCirclesG').style.display = "block";
    document.getElementById('neeroset_analysis').style.backgroundColor = "#d5d5d3";
    document.getElementById('neeroset_analysis').style.color = "#f67519";
    $('#tab1').prop('disabled', true);
    $('#tab2').prop('disabled', true);
    $('#tab3').prop('disabled', true);
    $('#tab4').prop('disabled', true);
    $('#neeroset_analysis').prop('disabled', true);
    res2.stdout.on('data', function(data) {
        console.log(`${data}`);
        if (`${data}`.trim() == '9')
        {
            neeroset_image()
            setTimeout(load_js, 1000)
            setTimeout(change_neeroset_0, 1100)
            document.getElementById('floatingCirclesG').style.display = "none";
            document.getElementById('neeroset_analysis').style.backgroundColor = "#252525";
            document.getElementById('neeroset_analysis').style.color = "#d5d5d3";
            $('#tab1').prop('disabled', false);
            $('#tab2').prop('disabled', false);
            $('#tab3').prop('disabled', false);
            $('#tab4').prop('disabled', false);
            $('#neeroset_analysis').prop('disabled', false);
            // $('#teh_def_number').html('<p>10</p>')
            function onHoverIn() {
                $(this).css('background-color', '#d5d5d3');
                $(this).css('color', '#f67519');
            }
            function onHoverOut() {
                $(this).css('background-color', '#252525');
                $(this).css('color', '#d5d5d3');
            }
            $("#neeroset_analysis").hover(onHoverIn, onHoverOut);

            // document.getElementById('neeroset_attention').style.marginLeft = '0px';
        }
    })
}

function neeroset_image() {
    let neeroset = document.getElementById("vk5");
    // load_js()
    neeroset.innerHTML = "<img id='neeroset_attention' src=\"" + path_to_verify + "\\COMPARISON_ATT_FILTERED.bmp\"  data-elem=\"pinchzoomer\" data-options=\"scaleMode:proportionalInside\" style=\"cursor: grab;\"\"/>"
    change_neeroset_9()
}
function attention_image(){
    let attention = document.getElementById("vk1");
    // load_js()
    attention.innerHTML = "<img id='target_attention' src=\"" + path_to_verify + "\\COMPARISON_ATTENTION.bmp\"  data-elem=\"pinchzoomer\" data-options=\"scaleMode:proportionalInside\" style=\"cursor: grab;\"\"/>"
    change_attention_9()
}

function nondetection() {
    let nondetectionImage = document.getElementById("vk2");
    nondetectionImage.innerHTML = "<img id='nondetection' src=\"" + path_to_verify + "\\COMPARISON_MASK_ATTENTION.bmp\" data-elem=\"pinchzoomer\" data-options=\"scaleMode:proportionalInside\"  style=\"cursor: grab;\"\"/>"
}


function create_image(){
    ipc.send('open-file-dialog-image')
    document.getElementById('tab3').click();
}

ipc.on('make_image', function (event, path) {
    // console.log(`${path}`);
    image_path = `${path}`
    console.log(image_path)
    fs.writeFileSync("path_to_image.txt", image_path)
    function chImage() {
        let chImageImage = document.getElementById("vk3");
        // load_js()
        chImageImage.innerHTML = "<img id='target_image' src=\"" + image_path + "\" data-elem=\"pinchzoomer\" data-options=\"scaleMode:proportionalInside\" style=\"cursor: grab;\"\"/>"
        load_js()
    }
    chImage()
});


function create_mask() {
    ipc.send('open-file-dialog-mask')
    document.getElementById('tab4').click();
}

ipc.on('make_mask', function (event, path) {
    // console.log(`${path}`);
    mask_path = `${path}`
    console.log(mask_path)
    fs.writeFileSync("path_to_mask.txt", mask_path)
    function chMask() {
        let chMaskImage = document.getElementById("vk4");
        // load_js()
        chMaskImage.innerHTML = "<img id='target_mask' src=\"" + mask_path + "\" data-elem=\"pinchzoomer\" data-options=\"scaleMode:proportionalInside\" style=\"cursor: grab;\"\"/>"
        load_js()
    }
    chMask()
});

// function click_mask() {
//     document.getElementById('tab4').click();
// }

function change_image_0() {
    document.getElementById('target_image').style.marginLeft = '0px';
}
function change_image_9() {
    document.getElementById('target_image').style.marginLeft = '9999px';
}

function change_mask_0() {
    document.getElementById('target_mask').style.marginLeft = '0px';
}
function change_mask_9() {
    document.getElementById('target_mask').style.marginLeft = '9999px';
}

function change_attention_0() {
    document.getElementById('target_attention').style.marginLeft = '0px';
}
function change_attention_9() {
    document.getElementById('target_attention').style.marginLeft = '9999px';
}

function change_nondetection_0() {
    document.getElementById('nondetection').style.marginLeft = '0px';
}
function change_nondetection_9() {
    document.getElementById('nondetection').style.marginLeft = '9999px';
}

function change_neeroset_0() {
    document.getElementById('neeroset_attention').style.marginLeft = '0px';
}
function change_neeroset_9() {
    document.getElementById('neeroset_attention').style.marginLeft = '9999px';
}
// function chImage() {
//     let chImageImage = document.getElementById("vk3");
//     // load_js()
//     chImageImage.innerHTML = "<img src=\"" + path_to_verify + "\\PAN.jpg\" data-elem=\"pinchzoomer\" data-options=\"scaleMode:proportionalInside\" style=\"cursor: grab;\"\"/>"
// }
