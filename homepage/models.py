from django.db import models
from django.contrib import admin

class SecurityFlaw(models.Model):
    name = models.TextField(null=True, blank = True)
    description = models.TextField(null=True, blank = True)
    exploitability = models.TextField(null=True, blank = True)
    prevalence = models.TextField(null=True, blank = True)
    detectability = models.TextField(null=True, blank = True)
    impact = models.TextField(null=True, blank = True)
    OWASP = models.TextField(null=True, blank = True)

admin.site.register(SecurityFlaw)
