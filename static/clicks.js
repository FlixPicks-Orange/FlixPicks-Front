
function add_click(num_clicks, page_url) {
    
    const postData = {
        num_clicks: num_clicks,
        page_url: page_url
    };

    
    fetch('/add_click', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
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


var clicks = 0;


window.addEventListener('click', () => {
    clicks++;
});


window.addEventListener('beforeunload', () => {

    add_click(clicks, window.location.href);
    console.log("Page is unloading! Number of clicks:", clicks);
});
