const form = document.getElementById('loginForm');

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    if (email.trim() === "" || password.trim() === "") return;

    const response = await fetch('/api/login', {
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({email, password}),
        method: "POST"
    });

    const data = await response.json();
    console.log(data);
    localStorage.setItem('token', data.access)
    localStorage.setItem('refresh', data.refresh)
    
    if(response.status === 200) {
        console.log("Correto")
    }
})