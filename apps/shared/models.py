"""uuid4 generation"""
from uuid import uuid4

from django.db import models

from apps.shared.translation import _


class BaseModel(models.Model):
    """
    Represents a base model that all subsequent models can be derived from
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    @property
    def creating(self) -> bool:
        """
        If this instance is being created and cannot be found in the database
        """
        return self._state.adding

    def presave_routine(self):
        """
        Called before self.save()
        """
        pass

    def postsave_routine(self):
        """
        Called immedietly after a self.save()
        """
        pass

    def save(self, *args, **kwargs):
        self.presave_routine()
        super(BaseModel, self).save(*args, **kwargs)
        self.postsave_routine()

    def predelete_routine(self):
        """
        Called before self.delete()
        """
        pass

    def postdelete_routine(self):
        """
        Called after self.delete()
        """
        pass

    def update(self, **kwargs):
        """
        Helper function since Django only supports update() calls on querysets
        """
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.save()

    def delete(self, *args, **kwargs):
        self.predelete_routine()
        super(BaseModel, self).delete(*args, **kwargs)
        self.postdelete_routine()

    class Meta:
        abstract = True
