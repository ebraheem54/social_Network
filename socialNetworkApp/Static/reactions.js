document.addEventListener('DOMContentLoaded', function () {

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const REACTION_EMOJI = { like: '👍', love: '❤️', haha: '😂', wow: '😮', sad: '😢' };
    const REACTION_LABEL = { like: 'Like', love: 'Love', haha: 'Haha', wow: 'Wow', sad: 'Sad' };

    function updateLikeBtn(postId, userReaction) {
        const btn = document.getElementById('like-btn-' + postId);
        if (!btn) return;
        const emojiEl = btn.querySelector('.like-btn-emoji');
        const labelEl = btn.querySelector('.like-btn-label');
        if (userReaction) {
            btn.classList.add('reacted');
            btn.dataset.current = userReaction;
            if (emojiEl) emojiEl.textContent = REACTION_EMOJI[userReaction] || '👍';
            if (labelEl) labelEl.textContent = REACTION_LABEL[userReaction] || 'Like';
        } else {
            btn.classList.remove('reacted');
            btn.dataset.current = '';
            if (emojiEl) emojiEl.textContent = '👍';
            if (labelEl) labelEl.textContent = 'Like';
        }
    }

    function updateReactionStats(postId, data) {
        const statsEl = document.getElementById('reaction-stats-' + postId);
        if (!statsEl) return;

        if (data.total > 0) {
            const emojis = data.top_reactions || [];
            let html = emojis.map(e => `<span class="stat-emoji">${e}</span>`).join('');
            html += `<span class="stat-count">${data.total}</span>`;
            statsEl.innerHTML = html;
            statsEl.style.display = '';
        } else {
            statsEl.innerHTML = '';
            statsEl.style.display = 'none';
        }
    }

    function sendReaction(postId, reactionType) {
        fetch('/react/' + postId + '/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'reaction_type=' + encodeURIComponent(reactionType),
        })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    updateLikeBtn(postId, data.user_reaction);
                    updateReactionStats(postId, data);

                    const popup = document.getElementById('reaction-popup-' + postId);
                    if (popup) {
                        popup.querySelectorAll('.popup-reaction-btn').forEach(b => {
                            b.classList.toggle('popup-active', b.dataset.reaction === data.user_reaction);
                        });
                        popup.classList.remove('popup-visible');
                    }
                }
            })
            .catch(err => console.error('Reaction error:', err));
    }

    document.querySelectorAll('.reaction-action-wrapper').forEach(wrapper => {
        const postId = wrapper.dataset.post;
        const popup = document.getElementById('reaction-popup-' + postId);
        const likeBtn = document.getElementById('like-btn-' + postId);
        let hoverTimer = null;
        let isPopupOpen = false;

        function showPopup() {
            if (popup) {
                popup.classList.add('popup-visible');
                isPopupOpen = true;
            }
        }

        function hidePopup() {
            if (popup) {
                popup.classList.remove('popup-visible');
                isPopupOpen = false;
            }
        }

        wrapper.addEventListener('mouseenter', () => {
            hoverTimer = setTimeout(showPopup, 400);
        });

        wrapper.addEventListener('mouseleave', () => {
            clearTimeout(hoverTimer);
            setTimeout(() => {
                if (!wrapper.matches(':hover')) {
                    hidePopup();
                }
            }, 300);
        });

        if (likeBtn) {
            likeBtn.addEventListener('click', function (e) {
                if (isPopupOpen) return;
                const current = this.dataset.current;
                sendReaction(postId, current ? current : 'like');
            });
        }

        if (popup) {
            popup.querySelectorAll('.popup-reaction-btn').forEach(btn => {
                btn.addEventListener('click', function (e) {
                    e.stopPropagation();
                    sendReaction(postId, this.dataset.reaction);
                });
            });
        }
    });

    document.querySelectorAll('.comment-action-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            const postId = this.dataset.post;
            toggleComments(postId, true);
        });
    });

    document.querySelectorAll('.comment-stat-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            const postId = this.dataset.post;
            toggleComments(postId, false);
        });
    });

    function toggleComments(postId, focusInput) {
        const section = document.getElementById('comments-' + postId);
        if (!section) return;
        const isHidden = section.style.display === 'none' || section.style.display === '';
        section.style.display = isHidden ? 'block' : 'none';
        if (isHidden && focusInput) {
            const input = document.getElementById('comment-input-' + postId);
            if (input) setTimeout(() => input.focus(), 100);
        }
    }

    document.querySelectorAll('.fb-reply-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            const commentId = this.dataset.comment;
            const postId = this.dataset.post;
            const username = this.dataset.username;
            const replyArea = document.getElementById('reply-area-' + commentId);
            if (!replyArea) return;

            const isHidden = replyArea.style.display === 'none' || replyArea.style.display === '';
            replyArea.style.display = isHidden ? 'flex' : 'none';
            if (isHidden) {
                const input = replyArea.querySelector('.fb-input');
                if (input) {
                    input.value = '';
                    input.focus();
                }
            }
        });
    });
});
