from django import template

register = template.Library()

@register.filter
def get_difficulty(flower_name):
    difficulties = {
        'Black Eyed Susan': 1,
        'Calendula': 1,
        'California Poppy': 1,
        'Carnation': 2,
        'Common Daisy': 1,
        'Daffodil': 1,
        'Dandelion': 1,
        'Iris': 2,
        'Lavender': 2,
        'Orchid': 4,
        'Rose': 3,
        'Sunflower': 1,
        'Tulip': 2
    }
    return difficulties.get(flower_name, 2)

@register.filter
def range_filter(value):
    return range(1, value + 1)