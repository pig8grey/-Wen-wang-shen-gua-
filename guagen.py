import eacal 


from datetime import datetime,date
import random as ra
import Iching as ic
import pytz
import numpy as np
from decimal import *



#定八卦
class bagua :

	

	def __init__ (self,yao):
		self.yao=yao
		self.gua={111:'乾', 222:'坤', 122: '艮', 212:'坎',
	 		221:'震', 112:'巽',121:'离',211:'兑'} 
		self.topgua=np.zeros((3,1))
		self.botgua=np.zeros((3,1))
        
		for i in range(0,len(yao)):

			if (yao[i]==1 or yao[i]==3):
				if i>2:

					self.topgua[i-3]=1

				else:

					self.botgua[i]=1

			else:
				if i>2:

					self.topgua[i-3]=2


				else:

					self.botgua[i]=2

	def kongwang(pos):
		if pos<=11:
			empty='戌亥'
			return empty
		if 11<pos<=23:
			empty='申酉'
			return empty
		if 23<pos<=35:
			empty='午未'
			return empty
		if 35<pos<=47:
			empty='辰巳'
			return empty
		else:
			empty='寅卯'
			return empty



	def givename (self):
		total=self.givesum()
		topguaname=self.gua[total[0]]
		botguaname=self.gua[total[1]]
		dualname=[topguaname, botguaname]
		return dualname



	def findbranch(self):

		topbranch={111:['戌','申','午'],222:['酉','亥','丑'], 122:['寅','子','戌'],
						212:['子','戌','申'],221:['戌','申','午'],112:['卯','巳','未'],
						121:['巳','未','酉'],211:['未','酉','亥']}
		botbranch={111:['辰','寅','子'],222:['卯','巳','未'], 122:['申','午','辰'],
						212:['午','辰','寅'],221:['辰','寅','子'],112:['酉','亥','丑'],
						121:['亥','丑','酉'],211:['丑','卯','巳']}
		total=self.givesum()
		shangzhi=topbranch[total[0]]

		xiazhi=botbranch[total[1]]
#由于从上往下，且从最上爻开始打，顺序就是这样了
		zhi=[xiazhi[2],xiazhi[1],xiazhi[0],shangzhi[2],shangzhi[1],shangzhi[0]]

		return zhi

	def changebranch(self):
		tmptop=[0,0,0]
		tmpbot=[0,0,0]
		tmptop=self.topgua
		tmpbot=self.botgua


#写变爻
		for i in range (0, len(self.topgua)):
			if self.yao[i+3]==0 or self.yao[i+3]==3:
				if self.yao[i+3]==0:
					self.topgua[i]=1
				else:
					self.topgua[i]=2


		for i in range (0, len(self.botgua)):
			if self.yao[i]==0 or self.yao[i]==3:
				if self.yao[i]==0:
					self.botgua[i]=1
				else:
					self.botgua[i]=2

		result=self.findbranch()
#重置值
		self.topgua=tmptop
		self.botgua=tmpbot

		return result


	def criticalnumber(self):
		num=0
		if ( (abs(self.yao[0]-self.yao[3])!=2) and (abs(self.yao[0]-self.yao[3])!=0)):
			num+=1


		if ( (abs(self.yao[1]-self.yao[4])!=2) and (abs(self.yao[1]-self.yao[4])!=0)):
			num+=2


		if ((abs(self.yao[2]-self.yao[5])!=2) and (abs(self.yao[2]-self.yao[5])!=0)):
			num+=4



		return num
	#起上下卦名

	def givesum(self):

		tmpbot=[self.botgua[0],self.botgua[1]*10,self.botgua[2]*100]
		tmptop=[self.topgua[0],self.topgua[1]*10,self.topgua[2]*100]

		topguasum=int(np.sum(tmptop))
		botguasum=int(np.sum(tmpbot))
			
		total=[topguasum, botguasum]

		return total

#世应爻算法
	def detsy (self):
		num=self.criticalnumber()
		drawsy={0:6,1:1,3:2,7:3,6:4,4:5,5:4,2:3}

		shi=drawsy[num]

		if shi > 3:
			ying=shi-3
		else:
			ying=shi+3

		sy=[shi,ying]
		return sy
	#查看卦首

	def checkmaster(self):
		[topguasum,botguasum]=self.givesum()

		num=self.criticalnumber()
		crossgua=[]
		#算（交）错卦
		for i in range(0,len(self.botgua)):
			if (self.botgua[i]==1):
				crossgua.append(2)
			else:
				crossgua.append(1)
		crossgua=np.array(crossgua)
		crossgua=np.array([crossgua[0],crossgua[1]*10,crossgua[2]*100])
		crossguasum=np.sum(crossgua)
		#看卦首
		if (num==0 or num ==1 or num==7 or num==3):
			return self.gua[topguasum]

		if (num==6 or num==4 or num==5):
			return self.gua[crossguasum]

		if (num==2):
			return self.gua[botguasum]


	def gua64 (self):
	
		gua=np.array([self.botgua[0],self.botgua[1],self.botgua[2],self.topgua[0],self.topgua[1],self.topgua[2]])
		#由于另外一个字典是以上爻为最后，本程序以上爻开始。所以要倒置一下
		gua=np.flipud(gua)

		i=1
		j=0

		while (i<10**6):
			gua[j]=gua[j]*i
			j+=1
			i*=10

		guasum=int(np.sum(gua))
		num=ic.hexa_lines[guasum]
		name=ic.hexa_names[num]

		result =[name,num]
		return result

		
	def drawgua(self):	
		#爻支画法
		drawbranch={0:"o ━  ━", 1:"  ━━━", 2:'  ━  ━', 3:'x ━━━' }
		master=self.checkmaster()
		print('卦首是： ' + str(master)+ '\n\n')
		#起世应爻
		[shi,ying]=self.detsy()
		#世应爻

		zhi=self.findbranch()
		[guaname,guanum]=self.gua64()
		deltazhi=self.changebranch()
		#写卦首
		[deltaguaname,deltaguanum]=self.gua64()

		print ("┼┼┼┼┼ "+str(guanum)+":"+guaname+"╋╋╋》"+str(deltaguanum)+":"+deltaguaname+" ┼┼┼┼┼\n\n")

		#画卦
		i=5
		while(i>=0):
		#填地支
		#少阴，少阳
			
			if(self.yao[i]!=0 and self.yao[i]!=3):


				if (i==(ying-1)):
					
					print("应"+drawbranch[self.yao[i]]+'  '+zhi[i])
					i-=1
					continue

				if (i==(shi-1)):
					print("世"+drawbranch[self.yao[i]]+'  '+zhi[i])
					i-=1
					continue

				print("  "+drawbranch[self.yao[i]]+'  '+zhi[i])
				i-=1
				continue
		#老阴
			if(self.yao[i]==0):

				if (i==(ying-1)):
					
					
					
					print("应"+drawbranch[self.yao[i]]+'  '+zhi[i]+"    ━━━"+'  '+deltazhi[i])
					i-=1
					continue

				if (i==(shi-1)):
					print("世"+drawbranch[self.yao[i]]+'  '+zhi[i]+"    ━━━"+'  '+deltazhi[i])
					i-=1
					continue

				print("  "+drawbranch[self.yao[i]]+'  '+zhi[i]+"    ━━━"+'  '+deltazhi[i])
				i-=1
				continue
		#老阳
			if(self.yao[i]==3):
				if (i==(ying-1)):
					print("应"+drawbranch[self.yao[i]]+'  '+zhi[i]+"    ━  ━"+'  '+deltazhi[i])
					i-=1
					continue

				if (i==(shi-1)):
					print("世"+drawbranch[self.yao[i]]+'  '+zhi[i]+"    ━  ━"+'  '+deltazhi[i])
					i-=1

					continue

				print("  "+drawbranch[self.yao[i]]+'  '+zhi[i]+"    ━  ━"+'  '+deltazhi[i])
				i-=1
				continue
		print("\n\n\n\n")
        



num=[]
for i in range(6):
    num.append(ra.randint(0,3))
    
#for j in range(6):
#	print(num[j])
        
asd=bagua(num)
asd.drawgua()
print('卦首为：'+asd.checkmaster())
