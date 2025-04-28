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

    const author = document.createElement('div');
    author.classList.add('comment-author');
    author.textContent = `${comment.user.nickname}`;

    const content = document.createElement('div');
    content.classList.add('comment-content');
    content.textContent = comment.content;

    const meta = document.createElement('div');
    meta.classList.add('comment-meta');
    meta.textContent = `Лайков: ${comment.likes} / Дизлайков: ${comment.dislikes}`;

    commentElement.appendChild(author);
    commentElement.appendChild(content);
    commentElement.appendChild(meta);

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
