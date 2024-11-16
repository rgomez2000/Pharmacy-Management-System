from django import template

register = template.Library()

@register.filter
def get_item_details(item, purchase):
    # Returns the PurchasedItemDetails object associated with the
    # instance of `item` and `purchase`
    return item.purchaseditemdetails_set.get(purchase=purchase)