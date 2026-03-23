from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    profile_pic = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics')
    bio = models.TextField(null=True, blank=True, max_length=500, default='')

    def get_num_posts(self):
        return Post.objects.filter(user=self).count()

    def is_following(self, user_B):
        return Friends.objects.filter(user_A=self, user_B=user_B).exists()

    def get_followings(self):
        return list(Friends.objects.filter(user_A=self).values_list('user_B_id', flat=True))


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.TextField(max_length=600, null=False, blank=True)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return self.caption

    def get_reaction_counts(self):
        counts = {}
        for r in self.reactions.all():
            counts[r.reaction_type] = counts.get(r.reaction_type, 0) + 1
        return counts

    def get_total_reactions(self):
        return self.reactions.count()

    def get_top_reactions(self):
        counts = self.get_reaction_counts()
        sorted_types = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        emoji_map = dict(REACTION_CHOICES)
        return [emoji_map[r] for r, _ in sorted_types[:3]]

    def get_comments(self):
        return self.comments.filter(parent=None).select_related('user').prefetch_related(
            'replies__user'
        ).order_by('created_at')

    def get_comment_count(self):
        return self.comments.count()


class Friends(models.Model):
    user_A = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_A')
    user_B = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_B')

    def __str__(self):
        return self.user_A.username + " --- " + self.user_B.username


REACTION_CHOICES = [
    ('like', '👍'),
    ('love', '❤️'),
    ('haha', '😂'),
    ('wow', '😮'),
    ('sad', '😢'),
]

REACTION_EMOJI = dict(REACTION_CHOICES)


class Reaction(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reactions')
    reaction_type = models.CharField(max_length=10, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f"{self.user.username} reacted {self.reaction_type} on post {self.post.id}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def __str__(self):
        return f"{self.user.username} commented on post {self.post.id}"

    def get_replies(self):
        return self.replies.select_related('user').order_by('created_at')


    