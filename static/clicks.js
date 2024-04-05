var clicks = 0;

//Captures number of clicks
window.addEventListener('click', (e) => {

clicks = clicks +1;

})


window.addEventListener('beforeunload', (e)=>{

    console.log("Page is unloading!"+clicks);
})
