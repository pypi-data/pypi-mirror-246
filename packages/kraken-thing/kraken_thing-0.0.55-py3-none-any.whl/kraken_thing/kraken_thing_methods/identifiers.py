
"""

"""






def get(record_type):
    """ returns key combinations that can be used as identifier for an object
    """    

    identifiers = []

    rule =  {
        'name': 'Base',
        'keys': ['@type', '@id'],
        'credibility': 1
        }

    identifiers.append(rule)

    if record_type not in ['action']:
        rule =  {
            'name': 'Base',
            'keys': ['@type', 'sameAs'],
            'credibility': 0.9
            }
    
        identifiers.append(rule)

    
    if record_type in ['organization', 'person']:
        rule = {
            'name': 'Base',
            'keys': ['@type', 'url'],
            'credibility': 1
            }
        identifiers.append(rule)
    
    if record_type in ['person']:
        rule = {
            'name': 'Email',
            'keys': ['@type', 'email'],
            'credibility': 0.7
            }
        identifiers.append(rule)


    return identifiers