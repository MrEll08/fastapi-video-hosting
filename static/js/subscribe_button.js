const subscribeBtn = document.getElementById("subscribe-btn");
const author_id = video_data.author.id;
console.log(user_id, author_id);
let subscribed = false;

async function check_subscription_status() {
    if (user_id === author_id) {
        console.log(user_id, author_id);
        subscribeBtn.disabled = true;
        return;
    }
    try {
        const response = await fetch(`/subscriptions/check?follower_id=${user_id}&followed_id=${author_id}`);
        if (response.ok) {
            let data = await response.json();
            subscribed = data.status;
            update_button(subscribed);
        } else {
            console.error("An error occurred while checking your subscription status:",
                response.error | "unidentified");
            subscribeBtn.disabled = true;
        }
    } catch {
        console.error("Check subscription status failed");
        subscribeBtn.disabled = true;
    }
}

function update_button(subscribed) {
    if (subscribed) {
        subscribeBtn.textContent = 'Отписаться';
        subscribeBtn.classList.remove('not-subscribed');
        subscribeBtn.classList.add('subscribed');
    } else {
        subscribeBtn.textContent = 'Подписаться';
        subscribeBtn.classList.remove('subscribed');
        subscribeBtn.classList.add('not-subscribed');
    }
}

subscribeBtn.addEventListener('click', async () => {
    try {
        let url = "/subscriptions/" + (subscribed ? "unsubscribe" : "subscribe") + `?follower_id=${user_id}&followed_id=${author_id}`;
        const response = await fetch(url, {
            method: "POST"
        });
        if (response.ok) {
            subscribed = !subscribed;
            update_button(subscribed);
        } else {
            console.error("An error occurred while changing your subscription status:",
                response.error | "unidentified");
        }
    } catch {
        console.error("Changing subscription status failed");
    }
});

check_subscription_status();