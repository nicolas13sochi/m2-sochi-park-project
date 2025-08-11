from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from django.utils.translation import gettext_lazy as _
from cms.consts import SeoParams

# Create your models here.
class BasePage(Page):
    use_in_sitemap = models.BooleanField(
        verbose_name=_('Включить в sitemap'),
        default=True,
        help_text=_('Включить в sitemap')
    )

    changefreq = models.CharField(max_length=10, choices=SeoParams.CHANGE_FREQ, default=SeoParams.CHANGE_FREQ[2][0], help_text=_('Как часто страница, вероятно, будет меняться'))

    priority = models.CharField(max_length=10, choices=SeoParams.PRIORITY, default=SeoParams.PRIORITY[10][0], help_text=_('Приоритет этого URL-адреса по отношению к другим URL-адресам на вашем сайте'))

    promote_panels = Page.promote_panels + [
        MultiFieldPanel([
            FieldPanel('use_in_sitemap'),
            FieldPanel('changefreq'),
            FieldPanel('priority'),
        ],
        heading='Управление SEO'
        )
    ]

    def get_sitemap_urls(self, request):

        sitemap = []
        
        if self.use_in_sitemap:
            sitemap.append(
                {
                    'location': self.full_url,
                    'changefreq': self.changefreq,
                    'priority': self.priority,
                    'lastmod': self.last_published_at
                }
            )

        return sitemap

    class Meta:
        abstract = True
        

class MainPage(BasePage):
    template = 'pages/index.html'
