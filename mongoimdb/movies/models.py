from django.db import models
from mongoengine import *
import datetime

class Comment(EmbeddedDocument):
	comment = StringField(required=True, max_length=1024)
	created = DateTimeField(default=datetime.datetime.now)


class Person(Document):
	first_name = StringField(required=True)
	last_name = StringField(required=True)
	dob = DateTimeField()

	def __unicode__(self):
		return self.full_name

	@property 
	def full_name(self):
		return '%s %s' % (self.first_name, self.last_name)


class Movie(Document):
	title = StringField(required=True)
	director = ReferenceField(Person, required=True, reverse_delete_rule=CASCADE)
	actors = ListField(ReferenceField(Person))
	comments = ListField(EmbeddedDocumentField(Comment))

	def __unicode__(self):
		return self.title



