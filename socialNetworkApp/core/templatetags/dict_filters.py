from django import template
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string

register = template.Library()

REACTION_EMOJI = {
    'like': '👍',
    'love': '❤️',
    'haha': '😂',
    'wow': '😮',
    'sad': '😢',
}


@register.filter
def get_item(dictionary, key):
    if dictionary is None:
        return None
    return dictionary.get(key)


@register.filter
def get_reaction_emoji(reaction_type):
    return REACTION_EMOJI.get(reaction_type, '👍')


@register.simple_tag(takes_context=True)
def render_comment_node(context, comment, post, depth=0):
    if depth > 8:
        return mark_safe('')
    rendered = render_to_string('comment_node.html', {
        'comment': comment,
        'post': post,
        'depth': depth,
        'request': context.get('request'),
    }, request=context.get('request'))
    return mark_safe(rendered)
