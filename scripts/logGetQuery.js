function(doc) {
	if (doc.accessToken == '~accessToken~' && doc.streamId=='~streamId~'){
		emit(doc.datetime,{accessToken:doc.accessToken,
						   streamId:doc.streamId,
						   referralIPAddress:doc.referralIPAddress,
						   totalDocs:doc.totalDocs,
						   datetime:doc.datetime,
						   responseTimeMS:doc.responseTimeMS,
						   status:doc.state
						   });
	}
}