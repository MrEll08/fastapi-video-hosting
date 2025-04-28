const like_button = document.getElementById('like-btn');
const dislike_button = document.getElementById('dislike-btn');

const like_counter = document.getElementById('like-count');
const dislike_counter = document.getElementById('dislike-count');
const video_id = video_data.id

document.getElementById('like-btn').addEventListener('click', async () => {
    response = await fetch(`/video/${video_id}?value=1`, {
        method: "POST"
    });
    if (response.ok) {
        let data = await response.json();
        let new_likes = data.likes;
        let new_dislikes = data.dislikes;
        like_counter.textContent = new_likes;
        dislike_counter.textContent = new_dislikes;
    } else {
        console.error("An error occured during like operation");
    }
});

document.getElementById('dislike-btn').addEventListener('click', async () => {
    response = await fetch(`/video/${video_id}?value=-1`, {
        method: "POST"
    });
    if (response.ok) {
        let data = await response.json();
        let new_likes = data.likes;
        let new_dislikes = data.dislikes;
        like_counter.textContent = new_likes;
        dislike_counter.textContent = new_dislikes;
    } else {
        console.error("An error occured during like operation");
    }
});