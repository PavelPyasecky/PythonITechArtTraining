from django import template


register = template.Library()


@register.filter
def get_page_url(page_number, filter_initials):
    platforms = filter_initials['platforms']
    genres = filter_initials['genres']
    rating = filter_initials['rating']
    url = '?'
    for platform in platforms:
        url += f'platforms={platform}' + '&'
    for genre in genres:
        url += f'genres={genre}' + '&'
    url += f'rating={rating}' + '&'
    url += f'page={page_number}'
    return url
