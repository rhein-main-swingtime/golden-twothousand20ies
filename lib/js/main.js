var log = document.getElementById('log');

var scrollPos = 0;

function logScroll(e) {
    if (e.pageY > 0) {
        console.log("Opfa!");
    }
    else {
    console.log("Spack!");
    }
    scrollPos = e.pageY;
}

document.onscroll = logScroll;
