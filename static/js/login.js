document.getElementById('login-form').addEventListener('submit', async function (event) {
    event.preventDefault();

    const login = document.getElementById('login').value;
    const password = document.getElementById('password').value;
    document.getElementById('error-message').style.display = 'none';

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({login, password})
        });

        const data = await response.json();

        if (response.ok && data.success) {
            localStorage.setItem('login', data.login);
            window.location.href = '/welcome';
        } else {
            document.getElementById('error-message').textContent = data.message || 'Ошибка при входе.';
            document.getElementById('error-message').style.display = 'block';
        }
    } catch (error) {
        document.getElementById('error-message').textContent = 'Ошибка при входе. Пожалуйста, попробуйте снова.';
        document.getElementById('error-message').style.display = 'block';
        console.error('Ошибка при входе:', error);
    }
});