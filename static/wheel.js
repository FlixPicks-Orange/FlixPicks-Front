import { Wheel } from 'https://cdn.jsdelivr.net/npm/spin-wheel@4.3.1/dist/spin-wheel-esm.js';
const processList = document.querySelector('.processList');
import { AlignText } from './constants';
const btnSpin = document.querySelector('.btn-spin');
const max_input_size = 13;

window.onload = () => {
  wheelInit();
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
  console.log(userArray[wheel.getCurrentIndex()]);
}
var userArray = []; // Array to store user input

window.addEventListener('click', (e) => {
  if (props.items.length > 0 || userArray.length > 0) {
    props.items.length = 0;
    userArray.length = 0;
  }
  console.log(userArray.length);
  console.log(props.items.length);
  // Listen for click event on spin button:
  if (e.target === processList) {
    // Get the input value from the user
    var userInput = document.getElementById('listInput').value;

    // Split the input into an array using newline characters as separators
    var itemList = userInput.split('\n');

    // Remove any empty items
    itemList = itemList.filter((item) => item.trim() !== '');

    // Store the array in the userArray variable
    userArray = itemList.map((item) => item.trim());

    if (userArray.length > max_input_size) {
      userArray.length = max_input_size;
    }
    for (let i = 0; i < userArray.length; i++) {
      props.items.push({ label: userArray[i] });
      console.log(userArray[i]);
    }
    if (props.items.length == 0) {
      props.items.push({ label: '' });
    }
    wheel.remove;
    wheel.init(props);
  }
});
const props = {
  isInteractive: false,
  itemLabelRadius: 0.85,
  itemLabelRadiusMax: 0.4,
  itemLabelRotation: 0,
  itemLabelAlign: AlignText.right,
  itemLabelBaselineOffset: -0.13,
  itemBackgroundColors: ['#ff7e00', '#d34f00', '#f49939', '#fcba70', '#df7234'],
  itemLabelColors: ['#000'],
  rotationSpeedMax: 1000,
  rotationResistance: -150,
  lineWidth: 0,
  overlayImage: './images/example-2-overlay.svg',
  onRest: outputWheel,
  items: [{ label: '' }],
};

function wheelInit() {
  const container = document.querySelector('.wheel-wrapper');
  window.wheel = new Wheel(container, props);
}
