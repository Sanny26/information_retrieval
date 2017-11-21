from collections import Counter
import pdb

class NaiveBayes():

	'''Data : [list of [doc ids, data, class labels]]'''
	def __init__(self, data=list()):
		self.data = data
		self.vocab = set()
		self.P_c = dict()
		self.P_wc = dict()

		self.update_class_probability()
		self.update_vocab()
		self.update_P_wc()



	def add_data(self, text, class_label):
		self.data.append([1, text, class_label])

		return

	def update_vocab(self):
		for each in self.data:
			self.vocab |= set([item for item in each[1]])

		return 

	def update_class_probability(self):
		for each in self.data:
			if each[2] in self.P_c:
				self.P_c[each[2]] += 1
			else:
				self.P_c[each[2]] = 1

		for each in self.P_c.keys():
			self.P_c[each] /= float(len(self.data))

		return

	def update_P_wc(self):

		counter= dict()

		for each in self.P_c.keys():
			counter[each] = Counter([])

		for each in self.data:
			counter[each[2]] += Counter(each[1])

		for each in self.P_c.keys():
			count_c = sum(counter[each].values())

			for word in self.vocab:
				count_wc = counter[each][word]
				self.P_wc[ word+'.'+each ] = float(count_wc + 1)/ (count_c+len(self.vocab))

		return


	def test(self, query):
		if type(query)!=list:
			query = query.strip().split()
		
		class_label = max_p = None

		for label in self.P_c.keys():
			p = self.P_c[label]
			for word in query:
				if word not in self.P_wc.keys():
					p *= 1/ float(len(self.vocab))
				else:
					p *= self.P_wc[ word+'.'+label]

			if p > max_p:
				max_p = p
				class_label = label

		return class_label


if __name__ == '__main__':
	
	data = [[1, ['Chinese','Beijing','Chinese'], 'c'],
			[2, ['Chinese', 'Chinese', 'Shanghai'], 'c'],
			[3, ['Chinese', 'Macao'], 'c'],
			[4, ['Tokyo', 'Japan', 'Chinese'], 'j']]
	classifier = NaiveBayes(data) 

	print classifier.test('Chinese Chinese Chinese Tokyo Japan')






