from wagtail import hooks
from wagtail.admin.site_summary import SummaryItem, PagesSummaryItem
from wagtail.documents.wagtail_hooks import DocumentsSummaryItem
from wagtail.images.wagtail_hooks import ImagesSummaryItem
from django.utils.safestring import mark_safe
from wagtail.admin.ui.components import Component
from django.utils.html import format_html
from django.templatetags.static import static
from wagtail import hooks
from django.urls import path, reverse
from wagtail.admin.menu import Menu, MenuItem, SubmenuMenuItem

@hooks.register('insert_global_admin_css')
def global_admin_css():
    return format_html('<link rel="stylesheet" href="{}">', static('css/wagtail/theme.css'))


@hooks.register('construct_main_menu')
def hide_snippets_menu_item(request, menu_items):
    menu_items[:] = [item for item in menu_items if item.name not in ['reports', 'help']]
