from django.shortcuts import render

from django.views import generic
from .models import Item,  MEAL_TYPE  # imports from the models table


class MenuList(generic.ListView):
    queryset = Item.objects.order_by("-date_created")
    template_name = "index.html"#connects views to index html file

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)#key and value tells html code what the keys value is
        context["meals"] = MEAL_TYPE
        return context


class MenuItemDetail(generic.DetailView):
    model = Item
    template_name = "menu_item_detail.html"#connects views to menu item html file


