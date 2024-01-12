import sqlite3
import pickle
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from Vectorizer import vectorize as v
from fuzzywuzzy import fuzz

def find_matching_keywords(sentence, keywords, threshold=80):
    sentence_lower = sentence.lower()

    matching_keywords = [keyword for keyword in keywords if fuzz.ratio(keyword.lower(), sentence_lower) >= threshold or keyword.lower() in sentence_lower]

    return matching_keywords

def getQuestion(cursor,index):
	if not isinstance(index, int):
		index = int(index)
	select_query = "Select Question FROM questionsList WHERE id = ?"
	cursor.execute(select_query,(index,))
	question = cursor.fetchone()

	return question[0]

def getVector(cursor,index):
	if not isinstance(index, int):
		index = int(index)
	select_query = "Select VectorizedQ FROM questionsList WHERE id = ?"
	cursor.execute(select_query,(index,))
	question = cursor.fetchone()
	question_data = question[0]
	question = pickle.loads(question_data)
	return question
	

def getTotalQuestion(cursor):
	select_query = "SELECT VectorizedQ FROM questionsList" 
	cursor.execute(select_query)
	total = cursor.fetchall()
	total = len(total)

	return total 

def _getVectorizedData(cursor):
	vectorized_data = []
	questions = getTotalQuestion(cursor)
	select_query = "SELECT VectorizedQ FROM questionsList WHERE id = ?" 

	for i in range(questions):
		cursor.execute(select_query,[i+1])
		question = cursor.fetchone()

		if question is not None:
			question_data = question[0]
			if question_data:
				question = pickle.loads(question_data)
				vectorized_data.append(question)

	return vectorized_data


def _getAnswer(cursor,index):
	if not isinstance(index, int):
		index = int(index)
	select_query = "SELECT Answer FROM questionsList WHERE id = ?" 
	cursor.execute(select_query,(index,))
	answer = cursor.fetchone()

	return answer[0]

def getAnswerAndScore(question):
	path = 'Data\model-4-database.db'
	connection = sqlite3.connect(path) 
	cursor = connection.cursor()

	question_vector = np.array(v.vectorize(question,4))
	question_vector = question_vector.reshape(1, -1)

	vectorizedDataset = _getVectorizedData(cursor)

	similarity_scores = cosine_similarity(question_vector,vectorizedDataset)
	highest_score_index = np.argmax(similarity_scores)
	highest_score = similarity_scores[0, highest_score_index]

	answer = _getAnswer(cursor,highest_score_index)

	connection.close()

	return answer,highest_score


def getAnswer(question):
	path = 'Data\model-5-database.db'
	model = 5

	connection = sqlite3.connect(path) 
	cursor = connection.cursor()

	question_vector = np.array(v.vectorize(question,model))
	question_vector = question_vector.reshape(1, -1)

	file_path = 'Data/keywords.txt'  

	with open(file_path, 'r') as file:
		keywords = file.readlines()

	keywords = [keyword.strip() for keyword in keywords]
	matching_keywords = find_matching_keywords(question, keywords)
	if matching_keywords.__contains__(""):
		matching_keywords.remove("")
	print(matching_keywords)
	
	database_questions = getTotalQuestion(cursor)
	relevant_questions = []
	similarities = []

	for i in range(1,database_questions+1):
		database_question = getQuestion(cursor,i)
		question_keyword = all(keyword in database_question for keyword in matching_keywords)
		
		if question_keyword:
			database_vector = np.array(getVector(cursor,i))
			database_vector = database_vector.reshape(1, -1)
		
			similarity_score = cosine_similarity(database_vector,question_vector)[0]
			similarities.append([similarity_score,i])
			relevant_questions.append(database_question)
		
	if relevant_questions:
		similarities = sorted(similarities, key=lambda x: x[0], reverse=True)
		answer = _getAnswer(cursor,similarities[0][1])
		print("relevant question",similarities[0][1])
	
		
	else:

		vectorizedDataset = _getVectorizedData(cursor)
		similarities = cosine_similarity(question_vector,vectorizedDataset)
		highest_score_index = np.argmax(similarities)
		highest_score = similarities[0, highest_score_index]
		answer = _getAnswer(cursor,highest_score_index)
		print(highest_score_index)
	

	connection.close()
	return answer
	








	


