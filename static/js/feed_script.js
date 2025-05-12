document.addEventListener("DOMContentLoaded", async () => {
    const feedContainer = document.getElementById("feed");

    try {
        const response = await fetch("/video/get-feed");
        const videos = await response.json();

        videos.forEach(video => {
            const videoBlock = document.createElement("div");
            videoBlock.classList.add("video-block");

            const videoLink = document.createElement("a");
            videoLink.href = `/video/${video.id}`;

            const videoEl = document.createElement("video");
            videoEl.src = video.path;
            videoEl.muted = true;
            videoEl.preload = "metadata";
            videoEl.playsInline = true;
            videoEl.classList.add("video-preview");

            videoEl.addEventListener("mouseenter", () => {
                videoEl.currentTime = 0;
                videoEl.play();
            });
            videoEl.addEventListener("mouseleave", () => {
                videoEl.pause();
                videoEl.currentTime = 0;
            });

            videoLink.appendChild(videoEl);
            videoBlock.appendChild(videoLink);

            const videoInfo = document.createElement("div");
            videoInfo.classList.add("video-info");

            const avatar = document.createElement("a");
            avatar.href = `/profile/${video.author.nickname}`

            const avatarImg = document.createElement("img");
            avatarImg.src = `/uploads/avatars/${video.author.avatar_filename || 'default.png'}`;
            avatarImg.alt = video.author.nickname;
            avatarImg.classList.add("author-avatar");

            avatar.appendChild(avatarImg);

            const videoText = document.createElement("div");
            videoText.classList.add("video-text");

            const titleEl = document.createElement("a");
            titleEl.textContent = video.title;
            titleEl.href = `/video/${video.id}`;
            titleEl.classList.add("video-title");

            const authorLink = document.createElement("a");
            authorLink.href = `/profile/${video.author.nickname}`;
            authorLink.textContent = video.author.nickname;
            authorLink.classList.add("author-link");

            videoText.appendChild(titleEl);
            videoText.appendChild(authorLink);

            videoInfo.appendChild(avatar);
            videoInfo.appendChild(videoText);

            videoBlock.appendChild(videoInfo);

            feedContainer.appendChild(videoBlock);
        });
    } catch (error) {
        console.error("Ошибка при загрузке видео:", error);
    }
});
