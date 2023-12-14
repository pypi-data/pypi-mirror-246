

def hero_banner(icon_name, title, subtitle, sub_content=None, color = ''):
    """Returns a banner 

    https://icons.getbootstrap.com/#usage
    """

    #<img class="d-block mx-auto mb-4" src="icon_url" alt="" width="72" height="57">
    #<button type="button" class="btn btn-outline-secondary btn-lg px-4">Secondary</button>

    #                <h1 class="display-5 fw-bold text-body-emphasis">{title}</h1>

    # <div class="d-grid gap-2 d-sm-flex justify-content-sm-center">

    
    icon_content = ''
    # Remove bi suffix if provided
    if icon_name and icon_name.startswith('bi-'):
        icon_name = icon_name[3:]

    if icon_name:
        icon_content = f'<i class="bi bi-{icon_name}" style="font-size: 10rem;"></i>'
    

    
    content = f'''

            <div class="px-4 py-5 my-5 text-center {color}">

                {icon_content}

                
                <h1 class="display-5 fw-bold ">{title}</h1>
                <div class="col-lg-6 mx-auto">
                  <p class="lead mb-4">{subtitle}</p>
                  <div class="d-grid gap-2  justify-content-sm-center">
                    
                    {sub_content}
                  </div>
                </div>
              </div>
            

    '''
    return content

