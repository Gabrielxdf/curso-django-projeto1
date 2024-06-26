(async function() {
    console.clear();
    const headers = {
        'Content-Type': 'application/json',
    };
    const body = JSON.stringify({
    	"username": "julhera",
    	"password": "Abc@12345678"
    });
    const config = {
        method: 'POST',
        headers: headers,
        body: body
    };
    const response = await fetch(
        'http://127.0.0.1:8000/recipes/api/token/',
        config
    );
    
    const json = await response.json();

    console.log('STATUS', response.status);
    console.log(json.access);
})();