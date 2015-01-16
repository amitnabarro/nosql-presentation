from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from pymongo import MongoClient
from bson import json_util
import json
import logging
import datetime

logger = logging.getLogger('jobs')


# get a mongodb client
_client = MongoClient()
# get a db ref
_db = _client['my-database']
# get a collection ref of create a new one
_coll = _db['jobs']

@csrf_exempt
def simple_insert(request):
	if request.method=='POST': 
		job =  json.loads(request.body)
		job['timestamp'] = datetime.datetime.utcnow()
		_coll.insert(job)

	return HttpResponse(status=204)





@csrf_exempt
def simple_insert_handler(request):
	if request.method=='POST': 
		job =  json.loads(request.body)
		logger.debug(job)
	return HttpResponse(status=204)




def group_by(request):
	# filter results from the past 5 days
	ts_end = datetime.datetime.utcnow()
	ts_start = ts_end - datetime.timedelta(days=5)

	res = _coll.aggregate([
		{ 
			'$match' : {
				'timestamp' : { '$gte' : ts_start, '$lte' : ts_end },
			}
		},{
				'$group' : {
					'_id': '$job_id',
					'start' : {'$first' : '$timestamp'},
					'end' : {'$last' : '$timestamp'},
					'events' : { 
						'$push': {
							'timestamp' : '$timestamp',
							'step' :'$step',
							'data' : '$data',
						}
					}, 
				},
			}
		])

	return HttpResponse(
		json.dumps(res,default=json_util.default),
		content_type="application/json")






uuids = [
	'da6dbf2e-8d79-4a7a-915b-e903eca3579f',
	'ae02090a-aa6e-4778-b557-5664a6879bba',
	'6dd60f81-ab78-4d8b-acf5-26981b8a7b66',
	'a7ea037a-c372-402d-924c-b72489a02711',
	'a5832688-16a9-4b77-b186-f7ad040e1674',
	'5fd4c966-f9c3-487c-8f30-8e9d32923bdf',
]