import './style.css';
import { Wheel } from 'https://cdn.jsdelivr.net/npm/spin-wheel@4.3.1/dist/spin-wheel-esm.js';
import { AlignText } from '/constants.js';
import { labeling } from '/data.js';
const btnSpin = document.querySelector('.btn-spin');
export var props;
import { fakeDB } from '/data.js';
window.onload = () => {
  props = {
    isInteractive: false,
    itemLabelRadius: 0.85,
    itemLabelRadiusMax: 0.4,
    itemLabelRotation: 0,
    itemLabelAlign: AlignText.right,
    itemLabelBaselineOffset: -0.13,
    itemBackgroundColors: [
      '#ff7e00',
      '#d34f00',
      '#f49939',
      '#fcba70',
      '#df7234',
    ],
    itemLabelColors: ['#000'],
    rotationSpeedMax: 1000,
    rotationResistance: -150,
    lineWidth: 0,
    overlayImage: './imgs/example-2-overlay.svg',
    onRest: outputWheel,
    items: fakeDB,
  };

  const container = document.querySelector('.wheel-wrapper');

  window.wheel = new Wheel(container, props);
};

window.addEventListener('click', (e) => {
  // Listen for click event on spin button:
  if (e.target === btnSpin) {
    wheel.spin(Math.floor(Math.random() * 1000) + 500);
  }
});

window.addEventListener('keyup', (e) => {
  if (e.target && e.target.matches('#pointerAngle')) {
    wheel.pointerAngle = parseInt(0);
  }
});

function outputWheel() {
  console.log(labeling[wheel.getCurrentIndex()]);
}
