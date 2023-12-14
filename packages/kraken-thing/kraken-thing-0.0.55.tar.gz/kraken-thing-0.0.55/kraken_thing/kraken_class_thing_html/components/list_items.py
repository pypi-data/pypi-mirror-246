
from kraken_thing.kraken_class_thing_html.html.panes import panes
from kraken_thing.kraken_class_thing_html.components.hero_banner import hero_banner

from kraken_thing.kraken_class_thing_html import html

def list_items(record):

    icon = record.get('icon', '')
    title = record.get('headline', '')
    text = record.get('text', '')
    content = record.get('content', '')
    color = record.get('color', '')
    rating = record.get('rating', '')
    items = record.get('items', [])

    contents = []
    
    for i in items:

        item_content = list_item(i)
        contents.append(item_content)

    product_features_content = ' '.join(contents)

    section_content = hero_banner(icon, title, text,  product_features_content, color)
    

    return section_content





def list_item(record, no=None):
    """
    """
    
    icon = record.get('icon', '')
    headline = record.get('headline', '')
    text = record.get('text', '')
    content = record.get('content', '')
    color = record.get('color', '')
    rating = record.get('rating', '')
    items = record.get('items', [])
    position = record.get('position', [])


    icon_content = ''
    rating_content = ''
    position_content=''

    if content is None:
        content = ''
    
    # Remove bi suffix if provided
    if icon and icon.startswith('bi-'):
        icon = icon[3:]

    if icon:
        icon_content = f'<i class="bi bi-{icon}" style="font-size: 4rem;"></i>'

    if rating:
        rating_content = html.rating(rating)

    if position:
        icon_position = str(position) + '-circle-fill'
        position_content = f'<i class="bi bi-{icon_position}" style="font-size: 2rem;"></i>'
    
    content = f'''
    <div class="row"> 
        <div class="col col-3 text-center "> 
            {icon_content} 
        </div>
        
        <div class="col col-2 text-center "> 
            {position_content} 
        </div>
        
        <div class="col col-7 text-start">

              <h4>{headline}</h4>
              
              <p>{text}</p>
              {content}
              {rating_content}
        </div>
    </div>
            

    '''

    

    return content






