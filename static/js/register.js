document.getElementById('register-form').addEventListener('submit', async function (event) {
    event.preventDefault();

    const login = document.getElementById('login').value;
    const nickname = document.getElementById('nickname').value;
    const password = document.getElementById('password').value;
    const errorMsg = document.getElementById('error-message');
    errorMsg.style.display = 'none';

    try {
        const response = await fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({login, nickname, password})
        });

        const data = await response.json();

        if (response.ok && data.success) {
            alert('Регистрация прошла успешно!');
            window.location.href = '/login';
        } else {
            const message = data.detail || 'Ошибка при регистрации.';
            errorMsg.textContent = message;
            errorMsg.style.display = 'block';
        }
    } catch (error) {
        errorMsg.textContent = 'Ошибка сети или сервера.';
        errorMsg.style.display = 'block';
        console.error('Ошибка при регистрации:', error);
    }
});