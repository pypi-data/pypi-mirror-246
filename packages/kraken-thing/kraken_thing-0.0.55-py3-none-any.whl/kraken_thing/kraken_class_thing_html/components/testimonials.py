
from kraken_thing.kraken_class_thing_html import html
from kraken_thing.kraken_class_thing_html.html import cardgrid
from kraken_thing.kraken_class_thing_html.html.panes import panes
from kraken_thing.kraken_class_thing_html.components.hero_banner import hero_banner


def testimonials(record):

    icon = record.get('icon', '')
    title = record.get('headline', '')
    text = record.get('text', '')
    content = record.get('content', '')
    color = record.get('color', '')
    rating = record.get('rating', '')
    items = record.get('items', [])


    contents = []

    for i in items:
        item_content = testimonial(i)
        contents.append(item_content)

    product_features_content = cardgrid(contents)

    section_content = hero_banner(icon, title, text,  product_features_content, color)


    return section_content





def testimonial(record):
    """Returns a card with a testimonial. card_flag True returns it in a card
    """

    icon = record.get('icon', '')
    title = record.get('headline', '')
    text = record.get('text', '')
    name = record.get('name', '')
    content = record.get('content', '')
    color = record.get('color', '')
    rating = record.get('rating', '')
    items = record.get('items', [])

    
    icon_content = ''
    rating_content = ''

    if content is None:
        content = ''

    # Remove bi suffix if provided
    if icon and icon.startswith('bi-'):
        icon = icon[3:]

    if icon:
        icon_content = f'<i class="bi bi-{icon}" style="font-size: 4rem;"></i>'

    if rating:
        rating_content = html.rating(rating)

    
    content = f'''
    
    
        <figure>
        {icon_content}
          <blockquote class="blockquote">
            <p>{text}</p>
          </blockquote>
          <figcaption class="blockquote-footer">
            {name}</cite>
          </figcaption>
          {rating_content}
        </figure>
    
    '''


    content = html.card('', content)
    
    return content