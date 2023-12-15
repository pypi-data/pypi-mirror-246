from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_sites.models import CurrentSiteManager, SiteModelMixin

from ..managers import SubjectRefusalManager
from ..model_mixins import SubjectRefusalModelMixin


class SubjectRefusal(SubjectRefusalModelMixin, SiteModelMixin, BaseUuidModel):
    objects = SubjectRefusalManager()

    on_site = CurrentSiteManager()

    history = HistoricalRecords()

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Subject Refusal"
        verbose_name_plural = "Subject Refusals"
