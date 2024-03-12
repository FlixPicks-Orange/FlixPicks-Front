const processList = document.querySelector('.processList');
import { props } from '/main.js';

var userArray = []; // Array to store user input
window.addEventListener('click', (e) => {
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
    convertToLabel();
    wheelInit;
  }
});

export var labeling = [{ label: 'boop' }];
var items = [{ items: labeling }];
function convertToLabel() {
  let i = 0;
  for (i in userArray) {
    labeling[i] = { label: userArray[i] };
    i = i + 1;
  }
}

async function wheelInit(){
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
    items: labeling,
  };
  const container = document.querySelector('.wheel-wrapper');

  window.wheel = new Wheel(container, props);
}