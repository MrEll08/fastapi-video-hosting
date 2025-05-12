commentsSection = document.getElementById("comments-section");
const commentForm = document.createElement('form');
commentForm.id = 'comment-form';

const commentTextarea = document.createElement('textarea');
commentTextarea.id = 'comment';
commentTextarea.placeholder = 'Оставьте комментарий';
commentTextarea.required = true;

const submitButton = document.createElement('button');
submitButton.type = 'submit';
submitButton.textContent = 'Отправить';

commentForm.appendChild(commentTextarea);
commentForm.appendChild(submitButton);
commentsSection.appendChild(commentForm);

const commentsList = document.createElement('div');
commentsList.id = 'comments-list';
commentsSection.appendChild(commentsList);

function createCommentElement(comment) {
    const commentElement = document.createElement('div');
    commentElement.classList.add('comment');

    const layout = document.createElement('div');
    layout.classList.add('comment-layout');

    const author_avatar = document.createElement('a');
    author_avatar.href = `/profile/${comment.user.nickname}`;

    const author_avatar_pic = document.createElement('img');
    author_avatar_pic.src = `/uploads/avatars/${comment.user.avatar_filename || 'default.png'}`;
    author_avatar_pic.alt = comment.user.nickname;
    author_avatar_pic.classList.add('comment-author-avatar');

    author_avatar.appendChild(author_avatar_pic);

    const comment_body = document.createElement('div');

    const author = document.createElement('a');
    author.href = `/profile/${comment.user.nickname}`;
    author.textContent = `${comment.user.nickname}`;
    author.classList.add('comment-author');

    const content = document.createElement('div');
    content.classList.add('comment-content');
    content.textContent = comment.content;

    const meta = document.createElement('div');
    meta.classList.add('comment-meta');
    meta.textContent = `Лайков: ${comment.likes} / Дизлайков: ${comment.dislikes}`;

    comment_body.appendChild(author);
    comment_body.appendChild(content);
    comment_body.appendChild(meta);

    layout.appendChild(author_avatar);
    layout.appendChild(comment_body);

    commentElement.appendChild(layout);

    return commentElement;
}

async function load_comments() {
    const comments_field = document.getElementById("comments-list");

    response = await fetch(`/comments/video/${video_data.id}`);
    comments = await response.json();
    console.log("comments:", comments);

    comments.forEach(comment => {
        commentsList.appendChild(createCommentElement(comment));
    });
}

load_comments();

document.getElementById('comment-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const commentText = document.getElementById('comment').value;
    // const commentText = "hey";
    response = await fetch(`/comments/video/${video_data.id}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({content: commentText}),
    });
    if (response.ok) {
        const scrollPosition = window.scrollY;
        window.location.reload();
        window.addEventListener('load', () => {
            window.scrollTo(0, scrollPosition);
        });
    } else {
        console.error("An error occured during posting the comment");
    }
});
