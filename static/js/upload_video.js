document.getElementById('upload-form').addEventListener('submit', async function (e) {
    e.preventDefault();

    const formData = new FormData(this);
    const status = document.getElementById('status');
    status.textContent = 'Загрузка...';

    try {
        const response = await fetch('/video/upload', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const data = await response.json()
            alert(data.message)
            status.textContent = '✅ Видео успешно загружено!';
            window.location.href = `/video/${data.video_id}`
        } else {
            status.textContent = response.message || '❌ Ошибка при загрузке';
        }
    } catch (err) {
        console.error(err);
        status.textContent = '⚠️ Произошла ошибка';
    }
});