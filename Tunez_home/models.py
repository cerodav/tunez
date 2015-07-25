from django.db import models
from datetime import datetime

class userquery(models.Model):
	query_content=models.CharField(max_length=200)
	query_date=models.DateTimeField('date created',default=datetime.now())

class result(models.Model):
	title=models.CharField(max_length=100)
	duration=models.CharField(max_length=20)
	quality=models.CharField(max_length=20)
	size=models.CharField(max_length=20)
	url=models.CharField(max_length=400)
	downloaded=models.IntegerField(default=0)
	query=models.ForeignKey(userquery)


