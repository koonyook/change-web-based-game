from django.db import models
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist

# Import models
from newtype.core.models import ServerStatus, ResearchLog

# Create your models here.
class State(models.Model):
    """(State description)"""
    time = models.DateTimeField(blank=True, default=datetime.now())
    researches = models.IntegerField()
    air_pollution = models.IntegerField()
    water_pollution = models.IntegerField()
    earth_pollution = models.IntegerField()
    natural_resources = models.IntegerField()

    @staticmethod
    def update():
        """docstring for update"""
        try:
            state = State.objects.latest('time')
            if state.time.date() != datetime.now().date():
                now = datetime.now()
                State.objects.create(
                    air_pollution=int(ServerStatus.objects.get(name='air_pollution').value),
                    water_pollution=int(ServerStatus.objects.get(name='water_pollution').value),
                    earth_pollution=int(ServerStatus.objects.get(name='earth_pollution').value),
                    natural_resources=int(ServerStatus.objects.get(name='natural_resources').value),
                    researches=ResearchLog.objects.filter(time__year=now.year, time__month=now.month, time__day=now.day).count(),
                )
        except ObjectDoesNotExist:
            now = datetime.now()
            State.objects.create(
                    air_pollution=int(ServerStatus.objects.get(name='air_pollution').value),
                    water_pollution=int(ServerStatus.objects.get(name='water_pollution').value),
                    earth_pollution=int(ServerStatus.objects.get(name='earth_pollution').value),
                    natural_resources=int(ServerStatus.objects.get(name='natural_resources').value),
                    researches=ResearchLog.objects.filter(time__year=now.year, time__month=now.month, time__day=now.day).count(),
                )

    def __unicode__(self):
        return unicode(self.time)
