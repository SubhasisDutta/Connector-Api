function(doc) {
	if (doc.token == '~accessToken~'){
		emit(doc.id,doc);
	}
}