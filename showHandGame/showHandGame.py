import random
class ShowHandGame(object):
	"""docstring for showHandGame"""
	def __init__(self, players):
		self.deck = []
		self.players = players
		self.playerList = []
		self.rankList = []
		self.dualList = []
		temp1 = PokerCard(1,11)
		temp2 = PokerCard(4,9)
		temp3 = PokerCard(3,9)
		temp4 = PokerCard(2,5)
		temp5 = PokerCard(1,1)
		self.hello1 = [temp1, temp2, temp3, temp4, temp5]
		temp1 = PokerCard(1,10)
		temp2 = PokerCard(4,7)
		temp3 = PokerCard(3,6)
		temp4 = PokerCard(2,3)
		temp5 = PokerCard(2,1)
		self.hello2 = [temp1, temp2, temp3, temp4, temp5]
		temp1 = PokerCard(1,10)
		temp2 = PokerCard(4,6)
		temp3 = PokerCard(1,6)
		temp4 = PokerCard(2,2)
		temp5 = PokerCard(3,1)
		self.hello3 = [temp1, temp2, temp3, temp4, temp5]
	
	def __player(self):
		return {"cards":[]}

	def __genPoker(self):
		for i in range(1,5,1):
			for j in range(1,14,1):
				tempPoker = PokerCard(i, j)
				self.deck.append(tempPoker)
		return self.deck

	def __castPoker(self, player):
		for i in range(5):
			totalCard = len(self.deck)
			player['cards'].append(self.deck.pop(random.randint(0,totalCard)-1))

	def __sortCard(self, handcard):
		pointList = [x.point for x in handcard]
		suitList = [x.suit for x in handcard]
		temp = sorted(zip(pointList, suitList, handcard), reverse=True)
		_, _, sortedHandcard = zip(*temp)
		return {"cards": sortedHandcard}

	def __calResult(self, sortedHandcard):
		rank = 0
		pointCount = 0
		flushFlag = True
		straightFlag = True
		pointList = [x.point for x in sortedHandcard]
		suitList = [x.suit for x in sortedHandcard]

		for i in range(5):
			if(i!=4 and pointList[i]-pointList[i+1]==1 and straightFlag):
				straightFlag = True
			elif(i==4 or not straightFlag):
				pass
			else:
				straightFlag = False

			if(i!=4 and suitList[i]==suitList[i+1] and flushFlag):
				flushFlag = True
			elif(i==4 or not flushFlag):
				pass
			else:
				flushFlag = False

			for j in range(4-i):
				if pointList[i]==pointList[4-j]:
					pointCount +=1

		if(pointList==[13, 12, 11, 10, 1]):
			straightFlag = True

		# Straight Flush : rank = 9
		if(flushFlag and straightFlag):
			rank = 9
			if(1 in pointList):
				dual = sortedHandcard[-1]
			else:
				dual = sortedHandcard[0]
		# Four of a Kind : rank = 8
		elif(pointCount == 6):
			rank = 8
			if pointList[0]!=pointList[1]:
				dual = sortedHandcard[1]
			else:
				dual = sortedHandcard[0]
		# Full House     : rank = 7
		elif(pointCount == 4):
			rank = 7
			if pointList[0]==pointList[1] and pointList[1]==pointList[2]:
				dual = sortedHandcard[0]
			else:
				dual = sortedHandcard[2]
		# Flush          : rank = 6
		elif(flushFlag and not straightFlag):
			rank = 6
			if(1 in pointList):
				dual = sortedHandcard[-1]
			else:
				dual = sortedHandcard[0]
		# Straight       : rank = 5
		elif(not flushFlag and straightFlag):
			if(1 in pointList):
				dual = sortedHandcard[-1]
			else:
				dual = sortedHandcard[0]
			rank = 5
		# Three of a Kind: rank = 4
		elif(pointCount == 3):
			rank = 4
			for i in range(4):
				if pointList[i]==pointList[i+1]:
					dual = sortedHandcard[i]
					break
		# Two Pairs      : rank = 3
		elif(pointCount == 2):
			rank = 3
			if pointList[0]==pointList[1]:
				dual = sortedHandcard[0]
			elif pointList[1]==pointList[2]:
				dual = sortedHandcard[1]
			if pointList[3]==1:
				dual = sortedHandcard[3]
				
		# One Pair       : rank = 2
		elif(pointCount == 1):
			rank = 2
			for i in range(4):
				if pointList[i]==pointList[i+1]:
					dual = sortedHandcard[i]
					break
		# High card      : rank = 1
		else:
			rank = 1
			if(1 in pointList):
				dual = sortedHandcard[-1]
			else:
				dual = sortedHandcard[0]

		return rank, dual

	def __judge(self):
		# print(self.rankList)
		flag = True
		i = 0
		sortedRankList = sorted(self.rankList, reverse = True)
		while(flag):
			if(i==len(self.playerList)-1):
				break
			if(sortedRankList[i]==sortedRankList[i + 1]):
				i+=1
			else:
				flag = False
				break
		# print('i  = ',i)
		if(i==0):
			print('player', self.rankList.index(max(self.rankList)), 'wins!!')
		else:
			_, indexList = zip(*sorted(zip(self.rankList, [x for x in range(self.players)]), reverse = True))
			# print(_)
			temp = self.__compare([self.dualList[x] for x in indexList[0:i + 1]])
			# print(temp.suit, temp.point)
			print('player', self.dualList.index(temp), 'wins!!')

	def __compare(self, handcardList):
		pointList = [x.point if x.point>1 else 14 for x in handcardList]
		# print('pointList = ', pointList)
		suitList = [x.suit for x in handcardList]
		# print('suitList = ', suitList)
		maxIndex = pointList.index(max(pointList))
		if len(pointList)!=len(list(set(pointList))):
			maxIndex = suitList.index(max(suitList))
		return handcardList[maxIndex]

	def startGame(self):
		self.__genPoker()
		for i in range(self.players):
			handcard = self.__player()
			self.__castPoker(handcard)
			sortedHandcard = self.__sortCard(handcard['cards'])
			rank, dual = self.__calResult(sortedHandcard['cards'])
			self.rankList.append(rank)
			self.dualList.append(dual)
			self.playerList.append(sortedHandcard)

			print("player"+str(i))
			for item in sortedHandcard['cards']:
				print(item.suit, item.point)
		self.__judge()

	def test(self):
		for hello in [self.hello1, self.hello2, self.hello3]:
			sortedHandcard = self.__sortCard(hello)
			rank, dual = self.__calResult(sortedHandcard['cards'])
			print('rank = ', rank)
			print('dual = ', dual.suit, dual.point)
			self.rankList.append(rank)
			self.dualList.append(dual)
			self.playerList.append(sortedHandcard)
			# for item in sortedHandcard['cards']:
			# 	print(item.suit, item.point)
		print(self.rankList)
		self.__judge()

class PokerCard(object):
	def __init__(self, suit, point):
		self.suit = suit	
		self.point = point

if __name__ == '__main__':
	test = ShowHandGame(3)
	test.startGame()
	# test.test()
	# print(chr(0x2660))

# player0
# 3 11
# 4 9
# 1 9
# 2 5
# 4 1
# player1
# 2 10
# 1 7
# 4 6
# 3 3
# 1 1
# player2
# 3 10
# 3 6
# 1 6
# 4 2
# 3 1
