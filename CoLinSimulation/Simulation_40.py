import numpy as np
from operator import itemgetter      #for easiness in sorting and finding max and stuff
from matplotlib.pylab import *
from random import sample, choice
from scipy.sparse import csgraph 
import os
# local address to save simulated users, simulated articles, and results
from conf import sim_files_folder, result_folder, save_address
from util_functions import *
from Articles import *
from Users import *
#from Algori import *
#from Algori import *

from LinUCB import *
from CoLin import *
from GOBLin import *

from W_Alg import *
from W_W0Alg import *
from eGreedyUCB1 import *
from scipy.linalg import sqrtm
import math

class simulateOnlineData():
	def __init__(self, dimension, iterations, articles, users, 
					batchSize = 1000,
					noise = lambda : 0,
					matrixNoise = lambda:0,
					type_ = 'UniformTheta', 
					signature = '', 
					poolArticleSize = 10, 
					NoiseScale = 0,
					epsilon = 1, Gepsilon = 1):

		self.simulation_signature = signature
		self.type = type_

		self.dimension = dimension
		self.iterations = iterations
		self.noise = noise
		self.matrixNoise = matrixNoise
		self.articles = articles 
		self.users = users

		self.poolArticleSize = poolArticleSize
		self.batchSize = batchSize
		
		self.W = self.initializeW(epsilon)
		self.GW = self.initializeGW(Gepsilon)
		self.NoiseScale = NoiseScale
	def constructAdjMatrix(self):
		n = len(self.users)	

		G = np.zeros(shape = (n, n))
		for ui in self.users:
			sSim = 0
			for uj in self.users:
				sim = np.dot(ui.theta, uj.theta)
 				if ui.id == uj.id:
 					sim *= 1.0
				G[ui.id][uj.id] = sim
				sSim += sim
				
			G[ui.id] /= sSim
			'''
			for i in range(n):
				print '%.3f' % G[ui.id][i],
			print ''
			'''
		return G
    
    # top m users
	def constructSparseMatrix(self, m):
		n = len(self.users)	

		G = np.zeros(shape = (n, n))
		for ui in self.users:
			sSim = 0
			for uj in self.users:
				sim = np.dot(ui.theta, uj.theta)
 				if ui.id == uj.id:
 					sim *= 1.0
 				elif uj.id >=m or ui.id >=m:
 					sim = 0
				G[ui.id][uj.id] = sim
				sSim += sim
				
			G[ui.id] /= sSim
			'''
			for i in range(n):
				print '%.3f' % G[ui.id][i],
			print ''
			'''
		return G

		

	# create user connectivity graph
	def initializeW(self, epsilon):	
 		#W = self.constructAdjMatrix()
 		W = self.constructSparseMatrix(40)   # sparse matrix top m users 
 		print 'W.T', W.T
		return W.T

	def initializeGW(self, Gepsilon):

 		G = self.constructAdjMatrix()	
 		L = csgraph.laplacian(G, normed = False)
 		I = np.identity(n = G.shape[0])
 		GW = I + Gepsilon*L  # W is a double stochastic matrix
 		print 'GW', GW
		return GW.T

	def getW(self):
		return self.W
	def getGW(self):
		return self.GW
	def getW0(self):
		temp = self.W+abs(self.matrixNoise())
		W0 = temp
		for i in range(self.W.shape[0]):
			W0.T[i] = [float(j)/sum(temp.T[i]) for j in temp.T[i]]
		print 'W0.T', W0.T
		return W0
	def getGW0(self):
		temp = self.GW+abs(self.matrixNoise())
		GW0 = temp
		for i in range(self.GW.shape[0]):
			GW0.T[i] = [float(j)/sum(temp.T[i]) for j in temp.T[i]]
		print 'GW0.T', GW0.T
		return GW0
	def getTheta(self):
		Theta = np.zeros(shape = (self.dimension, len(self.users)))
		for i in range(len(self.users)):
			Theta.T[i] = self.users[i].theta
		return Theta

	def batchRecord(self, iter_):
		print "Iteration %d"%iter_, "Pool", len(self.articlePool)," Elapsed time", datetime.datetime.now() - self.startTime

	def regulateArticlePool(self):
		# Randomly generate articles
		self.articlePool = sample(self.articles, self.poolArticleSize)   
		# generate articles 

	def CoTheta(self):
		for ui in self.users:
			ui.CoTheta = np.zeros(self.dimension)
			for uj in self.users:
				ui.CoTheta += self.W[uj.id][ui.id] * np.asarray(uj.theta)
			print 'Users', ui.id, 'CoTheta', ui.CoTheta

	def getReward(self, user, pickedArticle):
		return np.dot(user.CoTheta, pickedArticle.featureVector)

	def GetOptimalReward(self, user, articlePool):		
		maxReward = sys.float_info.min
		for x in articlePool:	 
			reward = self.getReward(user, x)
			if reward > maxReward:
				maxReward = reward
		return maxReward
	
	def getL2Diff(self, x, y):
		return np.linalg.norm(x-y) # L2 norm

	def runAlgorithms(self, algorithms):
		# get cotheta for each user
		self.startTime = datetime.datetime.now()
		timeRun = datetime.datetime.now().strftime('_%m_%d_%H_%M') 
		#fileSig = ''
		filenameWriteRegret = os.path.join(save_address, 'AccRegret' + timeRun + '.csv')
		filenameWritePara = os.path.join(save_address, 'ParameterEstimation' + timeRun + '.csv')


		self.CoTheta()
		self.startTime = datetime.datetime.now()

		tim_ = []
		BatchAverageRegret = {}
		AccRegret = {}
		ThetaDiffList = {}
		CoThetaDiffList = {}
		WDiffList = {}
		
		ThetaDiffList_user = {}
		CoThetaDiffList_user = {}
		WDiffList_user = {}
		
		# Initialization
		for alg_name in algorithms.iterkeys():
			BatchAverageRegret[alg_name] = []
			
			CoThetaDiffList[alg_name] = []
			AccRegret[alg_name] = {}
			if alg_name == 'syncCoLinUCB' or alg_name == 'AsyncCoLinUCB' or alg_name =='WCoLinUCB' or alg_name =='WknowTheta' or alg_name =='W_W0':
				ThetaDiffList[alg_name] = []
			if alg_name =='WCoLinUCB' or alg_name =='WknowTheta' or alg_name =='W_W0':
				WDiffList[alg_name] = []


			for i in range(len(self.users)):
				AccRegret[alg_name][i] = []
		
		userSize = len(self.users)

		with open(filenameWriteRegret, 'a+') as f:
			f.write('Time(Iteration)')
			f.write(',' + ','.join( [str(alg_name) for alg_name in algorithms.iterkeys()]))
			f.write('\n')
		with open(filenameWritePara, 'a+') as f:
			f.write('Time(Iteration)')
			f.write(',' + ','.join( [str(alg_name)+'CoTheta' for alg_name in algorithms.iterkeys()]))
			f.write(','+ ','.join([str(alg_name)+'Theta' for alg_name in ThetaDiffList.iterkeys()]))
			f.write(','+ ','.join([str(alg_name)+'W' for alg_name in WDiffList.iterkeys()]))
			f.write('\n')
		
		
		# Loop begin
		for iter_ in range(self.iterations):
			# prepare to record theta estimation error
			for alg_name in algorithms.iterkeys():
				CoThetaDiffList_user[alg_name] = []
				if alg_name == 'syncCoLinUCB' or alg_name == 'AsyncCoLinUCB' or alg_name == 'WCoLinUCB' or alg_name =='WknowTheta' or alg_name =='W_W0':
					ThetaDiffList_user[alg_name] = []
				if alg_name =='WCoLinUCB' or alg_name =='WknowTheta' or alg_name =='W_W0':
					WDiffList_user[alg_name] = []
			#self.regulateArticlePool() # select random articles	
			for u in self.users:
				#u = choseUser()
				#u = choice(self.users)
				self.regulateArticlePool() # select random articles

				noise = self.noise()
				#get optimal reward for user x at time t
				OptimalReward = self.GetOptimalReward(u, self.articlePool) + noise
							
				for alg_name, alg in algorithms.items():
					pickedArticle = alg.decide(self.articlePool, u.id)
					reward = self.getReward(u, pickedArticle) + noise
					alg.updateParameters(pickedArticle, reward, u.id)

					regret = OptimalReward - reward	
					AccRegret[alg_name][u.id].append(regret)

					# every algorithm will estimate co-theta
					
					if  alg_name == 'syncCoLinUCB' or alg_name == 'AsyncCoLinUCB' or alg_name == 'WCoLinUCB' or alg_name =='WknowTheta' or alg_name =='W_W0':
						CoThetaDiffList_user[alg_name] += [self.getL2Diff(u.CoTheta, alg.getCoThetaFromCoLinUCB(u.id))]
						ThetaDiffList_user[alg_name] += [self.getL2Diff(u.theta, alg.getLearntParameters(u.id))]
						if alg_name =='WCoLinUCB' or alg_name =='WknowTheta' or alg_name =='W_W0':
							WDiffList_user[alg_name] +=  [self.getL2Diff(self.W.T[u.id], alg.getW(u.id))]	
					elif alg_name == 'LinUCB'  or alg_name == 'GOBLin':
						CoThetaDiffList_user[alg_name] += [self.getL2Diff(u.CoTheta, alg.getLearntParameters(u.id))]
			for alg_name, alg in algorithms.items():
				if alg_name == 'syncCoLinUCB':
					alg.LateUpdate()						

			for alg_name in algorithms.iterkeys():
				CoThetaDiffList[alg_name] += [sum(CoThetaDiffList_user[alg_name])/userSize]
				if alg_name == 'syncCoLinUCB' or alg_name == 'AsyncCoLinUCB':
					ThetaDiffList[alg_name] += [sum(ThetaDiffList_user[alg_name])/userSize]
				if alg_name =='WCoLinUCB' or alg_name =='WknowTheta' or alg_name =='W_W0':
					ThetaDiffList[alg_name] += [sum(ThetaDiffList_user[alg_name])/userSize]
					WDiffList[alg_name] += [sum(WDiffList_user[alg_name])/userSize]
				
			if iter_%self.batchSize == 0:
				self.batchRecord(iter_)
				tim_.append(iter_)
				for alg_name in algorithms.iterkeys():
					TotalAccRegret = sum(sum (u) for u in AccRegret[alg_name].itervalues())
					BatchAverageRegret[alg_name].append(TotalAccRegret)
				
				with open(filenameWriteRegret, 'a+') as f:
					f.write(str(iter_))
					f.write(',' + ','.join([str(BatchAverageRegret[alg_name][-1]) for alg_name in algorithms.iterkeys()]))
					f.write('\n')
				with open(filenameWritePara, 'a+') as f:
					f.write(str(iter_))
					f.write(',' + ','.join([str(CoThetaDiffList[alg_name][-1]) for alg_name in algorithms.iterkeys()]))
					f.write(','+ ','.join([str(ThetaDiffList[alg_name][-1]) for alg_name in ThetaDiffList.iterkeys()]))
					f.write(','+ ','.join([str(ThetaDiffList[alg_name][-1]) for alg_name in WDiffList.iterkeys()]))
					f.write('\n')
		for alg_name in algorithms.iterkeys():
			print '%s: %.2f' % (alg_name, BatchAverageRegret[alg_name][-1])
		# plot the results		
		f, axa = plt.subplots(2, sharex=True)
		for alg_name in algorithms.iterkeys():	
			axa[0].plot(tim_, BatchAverageRegret[alg_name],label = alg_name)

			#plt.lines[-1].set_linewidth(1.5)
			print '%s: %.2f' % (alg_name, BatchAverageRegret[alg_name][-1])
		axa[0].legend(loc='lower right',prop={'size':9})
		axa[0].set_xlabel("Iteration")
		axa[0].set_ylabel("Regret")
		axa[0].set_title("Accumulated Regret")
		
		# plot the estimation error of co-theta
		time = range(self.iterations)
		
		for alg_name in algorithms.iterkeys():
			axa[1].plot(time, CoThetaDiffList[alg_name], label = alg_name + '_CoTheta')
			#plt.lines[-1].set_linewidth(1.5)
			if alg_name == 'AsyncCoLinUCB' or alg_name =='syncCoLinUCB' or alg_name =='WCoLinUCB' or alg_name =='W_W0':
				axa[1].plot(time, ThetaDiffList[alg_name], label = alg_name + '_Theta')
				
		
		axa[1].legend(loc='upper right',prop={'size':6})
		axa[1].set_xlabel("Iteration")
		axa[1].set_ylabel("L2 Diff")
		axa[1].set_yscale('log')
		axa[1].set_title("Parameter estimation error")

		'''
		for alg_name in algorithms.iterkeys():
			if alg_name == 'WCoLinUCB' or alg_name =='W_W0' or alg_name =='WknowTheta':
				axa[2].plot(time, WDiffList[alg_name], label = alg_name + '_W')
		
		axa[2].legend(loc='upper right',prop={'size':6})
		axa[2].set_xlabel("Iteration")
		axa[2].set_ylabel("L2 Diff")
		axa[2].set_yscale('log')
		axa[2].set_title("Parameter estimation error")
		'''
		plt.show()


if __name__ == '__main__':
	iterations = 500
	NoiseScale = .1
	matrixNoise = 0.3

	dimension = 5
	alpha  = 0.2
	lambda_ = 0.1   # Initialize A
	epsilon = 0 # initialize W
	eta_ = 0.1

	n_articles = 1000
	ArticleGroups = 5

	n_users = 80
	UserGroups = 5	

	poolSize = 10
	batchSize = 10

	# Parameters for GOBLin
	G_alpha = alpha
	G_lambda_ = lambda_
	Gepsilon = 1
	# Epsilon_greedy parameter
 
	eGreedy = 0.3
	
	userFilename = os.path.join(sim_files_folder, "users_"+str(n_users)+"+dim-"+str(dimension)+ "Ugroups" + str(UserGroups)+".json")
	
	#"Run if there is no such file with these settings; if file already exist then comment out the below funciton"
	# we can choose to simulate users every time we run the program or simulate users once, save it to 'sim_files_folder', and keep using it.
	UM = UserManager(dimension, n_users, UserGroups = UserGroups, thetaFunc=featureUniform, argv={'l2_limit':1})
	#users = UM.simulateThetafromUsers()
	#UM.saveUsers(users, userFilename, force = False)
	users = UM.loadUsers(userFilename)

	articlesFilename = os.path.join(sim_files_folder, "articles_"+str(n_articles)+"+dim"+str(dimension) + "Agroups" + str(ArticleGroups)+".json")
	# Similarly, we can choose to simulate articles every time we run the program or simulate articles once, save it to 'sim_files_folder', and keep using it.
	AM = ArticleManager(dimension, n_articles=n_articles, ArticleGroups = ArticleGroups,
			FeatureFunc=featureUniform,  argv={'l2_limit':1})
	#articles = AM.simulateArticlePool()
	#AM.saveArticles(articles, articlesFilename, force=False)
	articles = AM.loadArticles(articlesFilename)

	simExperiment = simulateOnlineData(dimension  = dimension,
						iterations = iterations,
						articles=articles,
						users = users,		
						noise = lambda : np.random.normal(scale = NoiseScale),
						matrixNoise = lambda : np.random.normal(scale = matrixNoise),
						batchSize = batchSize,
						type_ = "UniformTheta", 
						signature = AM.signature,
						poolArticleSize = poolSize, NoiseScale = NoiseScale, epsilon = epsilon, Gepsilon =Gepsilon)
	print "Starting for ", simExperiment.simulation_signature

	algorithms = {}
	
	algorithms['LinUCB'] = LinUCBAlgorithm(dimension = dimension, alpha = alpha, lambda_ = lambda_, n = n_users)
	
	algorithms['GOBLin'] = GOBLinAlgorithm( dimension= dimension, alpha = G_alpha, lambda_ = G_lambda_, n = n_users, W = simExperiment.getGW() )
	algorithms['syncCoLinUCB'] = syncCoLinUCBAlgorithm(dimension=dimension, alpha = alpha, lambda_ = lambda_, n = n_users, W = simExperiment.getW())
	algorithms['AsyncCoLinUCB'] = AsyCoLinUCBAlgorithm(dimension=dimension, alpha = alpha, lambda_ = lambda_, n = n_users, W = simExperiment.getW())
	
	#algorithms['WCoLinUCB'] =  WAlgorithm(dimension = dimension, alpha = alpha, lambda_ = lambda_, eta_ = eta_, n = n_users)
	#algorithms['WknowTheta'] = WknowThetaAlgorithm(dimension = dimension, alpha = alpha, lambda_ = lambda_, eta_ = eta_, n = n_users, theta = simExperiment.getTheta())
	#algorithms['W_W0'] = W_W0_Algorithm(dimension = dimension, alpha = alpha, lambda_ = lambda_, eta_ = eta_, n = n_users, W0 = simExperiment.getW0())

	#algorithms['eGreedy'] = eGreedyAlgorithm(epsilon = eGreedy)
	#algorithms['UCB1'] = UCB1Algorithm()
	
	
	simExperiment.runAlgorithms(algorithms)



	
