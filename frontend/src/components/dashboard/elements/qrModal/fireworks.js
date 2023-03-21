// Adapted from the tutorial: https://medium.com/front-end-weekly/how-to-add-some-fireworks-to-your-website-18b594b06cca

var container = document.createElement("DIV");
document.body.insertBefore(container, document.querySelector('.pageContainer'));

let particles = [];
const fwkPtcIniV = 0.5;
const fwkPtcIniT = 400;
const a = 0.0005;
const g = 0.0005;

function newFireworkParticle(x, y, angle) {
    var fwkPtc = document.createElement("DIV");
    fwkPtc.setAttribute('class', 'fireWorkParticle');
    container.appendChild(fwkPtc);
    fwkPtc.time = fwkPtcIniT;
    while (angle > 360)
    angle -= 360;
    while(angle < 0)
    angle += 360;
    fwkPtc.velocity = [];
    if (angle > 270) {
        fwkPtc.velocity.x = fwkPtcIniV * Math.sin(angle * Math.PI / 180);
        fwkPtc.velocity.y = fwkPtcIniV * Math.cos(angle * Math.PI / 180);
    } else if (angle > 180) {
        fwkPtc.velocity.x = fwkPtcIniV * Math.sin(angle * Math.PI / 180);
        fwkPtc.velocity.y = fwkPtcIniV * Math.cos(angle * Math.PI / 180);
    } else if(angle > 90) {
        fwkPtc.velocity.x = fwkPtcIniV * Math.sin(angle * Math.PI / 180);
        fwkPtc.velocity.y = fwkPtcIniV * Math.cos(angle * Math.PI / 180);
    } else {
        fwkPtc.velocity.x = fwkPtcIniV * Math.sin(angle * Math.PI / 180);
        fwkPtc.velocity.y = fwkPtcIniV * Math.cos(angle * Math.PI / 180);
    }

    fwkPtc.position = [];
    fwkPtc.position.x = x;
    fwkPtc.position.y = y;
    fwkPtc.style.left = fwkPtc.position.x + 'px';
    fwkPtc.style.top = fwkPtc.position.y + 'px';

    if(particles == null)  {
        particles = [];
    }
    particles.push(fwkPtc);
    return fwkPtc;
}

var before = Date.now();
var id = setInterval(frame, 5);
function frame() {
   var current = Date.now();
   var deltaTime = current - before;
   before = current;
   for (let i in particles) {
       var fwkPtc = particles[i];
       fwkPtc.time -= deltaTime;
       if(fwkPtc.time > 0) {
           fwkPtc.velocity.x -= fwkPtc.velocity.x * a * deltaTime;
           fwkPtc.velocity.y -= g * deltaTime + fwkPtc.velocity.y * a * deltaTime;
           fwkPtc.position.x += fwkPtc.velocity.x * deltaTime;
           fwkPtc.position.y -= fwkPtc.velocity.y * deltaTime;
           fwkPtc.style.left = fwkPtc.position.x + 'px';
           fwkPtc.style.top = fwkPtc.position.y + 'px';
       } else {
           fwkPtc.parentNode.removeChild(fwkPtc);
           particles.splice(i, 1);
       }
   }
}

export function newFireWorkStar(x, y) {
    var a = 0;
    while (a < 360) {
        newFireworkParticle(x, y, a);
        a += 15;
    }
}