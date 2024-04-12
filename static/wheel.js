import { Wheel } from 'https://cdn.jsdelivr.net/npm/spin-wheel@4.3.1/dist/spin-wheel-esm.js';
const processList = document.querySelector('.processList');
import { AlignText } from './constants.js';
const btnSpin = document.querySelector('.btn-spin');
const openbtn = document.querySelector('.openModal');
const closeBTN = document.querySelector('.closeBTN');
const modal = document.getElementById("modal");
const max_input_size = 13;

// Initializes wheel
window.onload = () => {
  wheelInit();
};

// Checks pointer angle on wheel
window.addEventListener('keyup', (e) => {
  if (e.target && e.target.matches('#pointerAngle')) {
    wheel.pointerAngle = parseInt(0);
  }
});

//Post request to backend WIP
function outputWheel() {
  const postData = {

    title : userArray[wheel.getCurrentIndex()]
  }

  fetch('/wheelresult', {
    method: 'POST',
    headers: {
      'Content-Type' : 'application/json'
    },
    body: JSON.stringify(postData)
  })
  .then(response => {

    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {

    console.log('Response:', data);
})
.catch(error => {

    console.error('Error:', error);
});
}





var userArray = []; // Array to store user input

//Event listener to check if buttons have been pressed
window.addEventListener('click', (e) => {

  if(e.target == openbtn)
  modal.classList.add("open");

 if(e.target == closeBTN)
  modal.classList.remove("open");


    // Listen for click event on spin button:
    if (e.target === btnSpin) {
      wheel.spin(Math.floor(Math.random() * 1000) + 500);
    }

    // Listen for click event on Submit button
  if (e.target == processList) {
    if (props.items.length > 0 || userArray.length > 0) {
      props.items.length = 0;
      userArray.length = 0;
    }
    // If you want to see the array lengths
    // console.log(userArray.length);
    // console.log(props.items.length);

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

      // Purge any array greater than 13
      if (userArray.length > max_input_size) {
        userArray.length = max_input_size;
      }
      for (let i = 0; i < userArray.length; i++) {
        props.items.push({ label: userArray[i] });
        // console.log(userArray[i]);
      }
      if (props.items.length == 0) {
        props.items.push({ label: '' });
      }
      // Re-initialize the wheel with new labels.
      wheel.remove;
      wheel.init(props);
    }
  }
});

// This is the wheel settings
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
  overlayImage: '../static/images/Lights.svg',
  onRest: outputWheel,
  items: [{ label: '' }],
};

// Wheel initializer
function wheelInit() {
  const container = document.querySelector('.wheel-wrapper');
  window.wheel = new Wheel(container, props);
}
