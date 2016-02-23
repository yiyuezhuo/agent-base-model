# -*- coding: cp936 -*-
# by yiyuezhuo
import random
import copy
#引用区

#以上为参数区
def randomvector(n):
    T=[random.random() for i in range(n)]
    return [i/sum(T) for i in T]
def flow(x,y,d):
    if x-d>=0:
        return x-d,y+d
    else:
        return 0,y+x
def zero(x,y):
    return x if x>y else 0
def flowx(x,d):
    return zero(x-d,0)
def cond_vector(l,n):
    l=l[:]
    t=l[n]
    s=sum(l)
    for i in range(len(l)):
        if i==n:
            l[i]=0
        else:
            l[i]+=t*(l[i]/(s-t))
    return l
def focus_vector(l,p,n):
    l=l[:]
    if l[n]>p:
        return l
    else:
        t=l[n]
        s=sum(l)
        d=p-l[n]
        for i in range(len(l)):
            if i==n:
                l[n]=p
            else:
                l[i]-=d*l[i]/(s-t)
    return l
#全局函数区
class Platform:
    def __init__(self,sidenumber=4):
        self.history=[]
        self.statue=None
        self.sidenumber=sidenumber
    def setup(self):
        namelist=['KMT','CP','JAP','WAL']
        #初始地域应该是200，其中30以游击区形式存在
        KMT=CKMT('KMT',80,800,20,10,0,5,namelist)
        CP=CCP('CP',10,300,5,0,30,5,namelist)
        JAP=CJAP('JAP',10,2500,200,10,0,10,namelist)
        WAL=CWAL('WAL',70,700,10,10,0,0,namelist)
        self.statue=Statue([KMT,CP,JAP,WAL])
        self.history.append(self.statue)
    def go(self):
        statue=copy.deepcopy(self.statue)
        for i in range(self.sidenumber):
            sideing=statue.sidelist[i]
            sideing.update(statue)
            statue=sideing.think(statue)
        #statue.display()
        self.statue=statue
        self.history.append(statue)
    def run(self,n):
        for i in range(n):
            print i
            self.go()
    def display(self):
        for i in range(self.sidenumber):
            self.statue.sidelist[i].display()
    def formal(self):
        return self.statue.formal()
    def formalX(self,X,Y):
        return self.statue.formalXY(X,Y)
    def formalH(self):
        return [i.formal() for i in self.history]
    def formalHXY(self,X,Y):
        return [i.formalXY(X,Y) for i in self.history]
    def formalHX(self,X):
        return [i.formalX(X) for i in self.history]
    def formalStr(self,l):
        #这里是将各种列表格式转成逗号分隔字符串列表。不加1，2,3那个头。
        if len(l)==0:
            return ''
        elif type(l[0])!=type([]):
            return ','.join([str(i) for i in l])
        else:
            return [','.join([str(i) for i in ii]) for ii in l]
    def head(self,fff):
        if type(fff)==type(''):
            return [self.formalStr([str(i+1) for i in range(len(fff.split(',')))]),fff]
        else:
            return [self.formalStr([str(i+1) for i in range(len(fff[0].split(',')))])]+fff
    def linebyline(self,s):
        if type(s)==type(''):
            return s
        else:
            #print s
            return '\n'.join(s)
    def IO_ExcelOne(self,X,Y):
        f=open('output.txt','w')
        f.write(self.linebyline(self.head(self.formalStr(self.formalHXY(X,Y)))))
        f.close()
    def IO_ExcelExam(self):
        land=self.formalHXY(2,1)
        land=self.formalHXY(2,1)
        
            
class Side:
    def __init__(self,name,land,army,industry,infiltration,control,aid,namelist):
        self.name=name
        self.land=land
        self.army=0
        self.defend=army#初始默认防守，否则你懂得
        self.industry=industry
        self.resources=0
        self.infiltration=infiltration
        self.control=control
        self.aid=aid
        self.allside=namelist#这里只有名字，不是对象
        self.namelist=namelist
        self.sidenumber=len(namelist)
        self.thinking=200
        #self.US=US
        self.opportunity=[0 for i in range(len(namelist)-1)]
        self.bonus=[1.0 for i in range(len(namelist)-1)]
    def value(self,statue):#这个函数本身也只会在转移时使用，所以当然有statue传入
        enmey=sum([(i.army+i.defend) for i in statue.otherside(self.name)])
        if self.defend==0:
            threat=enmey/0.0001*self.land
        else:
            threat=enmey/self.defend*self.land
        return self.land*10+self.army*0.01+self.control-self.infiltration*0.2+\
               statue.diplomacy(self.name)-threat
    def product(self):
        #n个是因为除了n个可能的敌人外还有自己的防守兵力(否则随机向量就不好用了)
        return [randomvector(self.sidenumber) for i in range(self.thinking)]
    def update(self,statue):
        #两个对外函数之一。尽量不要通过statue修改数据。
        self.industry*=1.01
        self.army+=self.defend
        self.defend=0
        income=self.land+self.control*0.5+self.aid+self.industry
        outcome=self.infiltration*0.5+self.army*0.01
        self.resources=income-outcome
        self.army+=self.resources if self.resources>=0 else self.resources*10
        self.resources=0
        self.bonus=[1.0 for i in range(len(self.namelist)-1)]
        for i in range(len(self.opportunity)):
            r=random.random()
            if r<=self.opportunity[i]:
                self.bonus[i]+=r
                self.opportunity[i]-=r
            else:
                self.opportunity[i]+=0.05
    def power(self):
        myside=self
        return myside.land+myside.army*0.1+myside.industry*0.1
    def spread(self):
        return self.army/self.land*1
    def combat(self,AS,DS,AZ,AE,DZ,DE,AI,DI,CL):
        AF=0.05
        DF=0.075
        AL=DF*DS
        DL=AF*AS
        if (DZ==0 and DE==0)or AS/DS<=0.2:
            return AS,DS,AZ,AE,DZ,DE,AI,DI,CL
        elif DL>DS or AL==0:
            return flowx(AS,AL),0,AZ+DZ,AE+DE,0,0,AI+DI*0.1,0,CL
        elif AL>AS or DL==0:
            return 0,flowx(DS,DL),0,0,AZ+DZ,AE+DE,0,AI*0.1+DI,CL
        else:
            ZL=zero(DL/AL,1)*((DZ+DE)*0.05)*2
            ZLL=min(ZL,DZ+DE)
            ZP=DZ/(DZ+DE)
            EP=DE/(DZ+DE)
            return AS-AL,DS-DL,AZ+ZLL*ZP,AE+ZLL*EP,DZ-ZLL*ZP,DE-ZLL*EP,AI+0.1*ZLL/(DZ+DE)*DI,DI-ZLL/(DZ+DE)*0.7*DI,CL
    def think(self,statue):
        #两个对外函数之一。
        virlist=[copy.deepcopy(statue) for i in range(self.thinking)]
        actlist=self.product()
        result=self.max_value(virlist,actlist)
        return result
    def max_value(self,virlist,actlist):
        for i in range(self.thinking):
            statueing=virlist[i]
            acting=actlist[i]
            selfing=statueing.theside(self.name)
            otherside=statueing.otherside(self.name)
            assign=[selfing.army*acting[ii] for ii in range(self.sidenumber)]
            bonus=selfing.bonus
            for ii in range(selfing.sidenumber-1):
                defendside=otherside[ii]
                AS,DS,AZ,AE,DZ,DE,AI,DI,CL=assign[ii]*selfing.bonus[ii],defendside.defend,\
                                         selfing.land,selfing.infiltration,defendside.land,\
                                         defendside.infiltration,selfing.industry,defendside.industry,\
                                         self.control
                ASS,DSS,AZZ,AEE,DZZ,DEE,AII,DII,CLL=selfing.combat(AS,DS,AZ,AE,DZ,DE,AI,DI,CL)
                selfing.army+=(ASS-AS)/bonus[ii]#这样写表示加成还能减少伤亡，写到右边则表示只增加杀伤不减少伤亡
                defendside.defend+=DSS-DS
                selfing.land+=AZZ-AZ
                selfing.infiltration+=AEE-AE
                defendside.land+=DZZ-DZ
                defendside.infiltration+=DEE-DE
                selfing.industry+=AII-AI
                defendside.industry+=DII-DI
                selfing.control+=CLL-CL
            selfing.defend+=assign[selfing.sidenumber-1]
            selfing.army-=assign[selfing.sidenumber-1]
        valuelist=[i.theside(self.name).value(statueing) for i in virlist]
        #print actlist[valuelist.index(max(valuelist))]
        return virlist[valuelist.index(max(valuelist))]
    def display(self):
        print ''
        print 'name: ',self.name
        print 'zone: ',self.land+self.infiltration+self.control
        print 'land: ',self.land
        print 'infiltration: ',self.infiltration
        print 'control: ',self.control
        print 'army+defend: ',self.army+self.defend
        #print 'army: ',self.army
        #print 'defend: ',self.defend
        #print 'industry: ',self.industry
    def formal(self):
        return (self.name,self.army+self.defend,self.land+self.infiltration+self.control,self.land,self.infiltration,self.control,self.army,self.defend,self.industry)
            
class CKMT(Side):
    def __init__(self,name,land,army,industry,infiltration,control,aid,namelist):
        Side.__init__(self,name,land,army,industry,infiltration,control,aid,namelist)
    def product(self):
        return [cond_vector(randomvector(self.sidenumber),2) for i in range(self.thinking)]
    def update(self,statue):
        #两个对外函数之一。尽量不要通过statue修改数据。
        self.industry*=1.01
        self.army+=self.defend
        self.defend=0
        self.resources=self.land+self.control*0.5-self.infiltration*0.5\
                        +self.aid-self.army*0.01+self.industry
        self.army+=self.resources if self.resources>=0 else self.resources*10
        self.resources=0
        self.bonus=[1.0 for i in range(len(self.namelist)-1)]
        for i in range(len(self.opportunity)):
            r=random.random()
            if r<=self.opportunity[i]:
                self.bonus[i]+=r
                self.opportunity[i]-=r
            else:
                self.opportunity[i]+=0.05
        WAL_side=statue.theside('WAL')
        flow_p=0.03
        WAL_side.land,self.land=flow(WAL_side.land,self.land,WAL_side.land*flow_p)
        WAL_side.army,self.army=flow(WAL_side.army,self.army,WAL_side.army*flow_p)
        WAL_side.industry,self.industry=flow(WAL_side.industry,self.industry,WAL_side.industry*flow_p)

class CJAP(Side):
    def __init__(self,name,land,army,industry,infiltration,control,aid,namelist):
        Side.__init__(self,name,land,army,industry,infiltration,control,aid,namelist)
        self.US=0
        self.opportunity[0]=1.0
    def update(self,statue):
        #两个对外函数之一。尽量不要通过statue修改数据。
        self.industry*=0.99
        self.army+=self.defend
        self.defend=0
        income=self.land*0.2+self.control*0.1+self.aid+self.industry
        outcome=self.infiltration*0.7+self.army*0.01
        #日本从领土(中国)中获得的收益很少，主要依赖工业。
        self.resources=income*(1-self.US)-outcome if self.resources>=0 else self.resources*10
        self.US+=0.01
        self.army+=self.resources
        self.army=zero(self.army,0)
        self.resources=0
        self.bonus=[1.0 for i in range(len(self.namelist)-1)]
        for i in range(len(self.opportunity)):
            r=random.random()
            if r<=self.opportunity[i]:
                self.bonus[i]+=r
                self.opportunity[i]-=r
            else:
                self.opportunity[i]+=0.1#日本拥有更强的战术寻觅能力
class CWAL(Side):
    def __init__(self,name,land,army,industry,infiltration,control,aid,namelist):
        Side.__init__(self,name,land,army,industry,infiltration,control,aid,namelist)
    def product(self):
        return [focus_vector(randomvector(self.sidenumber),0.9,3) for i in range(self.thinking)]
class CCP(Side):
    def __init__(self,name,land,army,industry,infiltration,control,aid,namelist):
        Side.__init__(self,name,land,army,industry,infiltration,control,aid,namelist)
    def update(self,statue):
        #两个对外函数之一。尽量不要通过statue修改数据。
        self.industry*=1.02
        self.army+=self.defend
        self.defend=0
        income=self.land*1.5+self.control*0.5+self.aid+self.industry*1.5
        outcome=self.infiltration*0.5+self.army*0.005
        #共产党具有更高的调度能力与更低的维持费
        self.resources=income-outcome 
        self.army+=self.resources*1.1 if self.resources>=0 else self.resources*10
        self.resources=0
        self.bonus=[1.0 for i in range(len(self.namelist)-1)]
        for i in range(len(self.opportunity)):
            r=random.random()
            if r<=self.opportunity[i]:
                self.bonus[i]+=r
                self.opportunity[i]-=r
            else:
                self.opportunity[i]+=0.05
    def combat(self,AS,DS,AZ,AE,DZ,DE,AI,DI,CL):
        #print CL
        p=0.4 #占领而不是控制的比例
        AF=0.02#共党的战斗方式使守方没有优势并减小双方伤亡。
        DF=0.02
        AL=DF*DS
        DL=AF*AS
        if (DZ==0 and DE==0)or AS/DS<=0.1:
            return AS,DS,AZ,AE,DZ,DE,AI,DI,CL
        elif DL>DS or AL==0:
            return flowx(AS,AL),0,AZ+DZ+DE,AE,0,0,AI+DI*0.1,0,CL
        elif AL>AS or DL==0:
            return 0,flowx(DS,DL),0,0,AZ+DZ,AE+DE,0,AI*0.1+DI,CL
        else:
            ZL=zero(DL/AL,1/4)*((DZ+DE)*0.05)*1
            ZLL=min(ZL,DZ+DE)
            ZP=DZ/(DZ+DE)
            EP=DE/(DZ+DE)
            #print CL
            dAZ=AZ+ZLL*p
            dDZ=DZ-ZLL*p*ZP
            dDE=DE-ZLL*p*EP
            dCL=CL-ZLL*p*EP
            #print dCL
            if ZLL*(1-p)<=dDZ:
                dDZ-=ZLL*(1-p)
                dDE+=ZLL*(1-p)
                dCL+=ZLL*(1-p)
            else:
                d=dDZ
                dDZ=0
                dDE+=d
                dCL+=d
                c=ZLL*(1-p)-d
                dDE-=c
                dCL-=c
                dAZ+=c
            #print 'dCL',dCL
            return AS-AL,DS-DL,dAZ,AE,dDZ,dDE,AI+0.1*ZLL/(DZ+DE)*DI,DI-ZLL/(DZ+DE)*0.7*DI,dCL
     

class Statue:
    def __init__(self,sidelist):
        self.sidelist=sidelist
        self.namelist=[i.name for i in sidelist]
    def otherside(self,name):
        return filter(lambda x:x.name!=name,self.sidelist)
    def power(self,name):
        myside=self.theside(name)
        return myside.power()
    def diplomacy(self,name):
        myside=self.theside(name)
        powerlist=[self.power(i.name) for i in self.sidelist]
        powerside=self.sidelist[powerlist.index(max(powerlist))]
        if name!=powerside.name:
            return -1.1*powerside.power()+0.1*sum([i.power() for i in self.otherside(name)])
        else:
            return -sum([i.power() for i in self.otherside(name)])*0.5
    def theside(self,name):
        #print name
        return filter(lambda x:x.name==name,self.sidelist)[0]
    def display(self):
        for i in self.sidelist:
            i.display()
    def formal(self):
        return [i.formal() for i in self.sidelist]
    def formalXY(self,X,Y):
        return self.sidelist[X].formal()[Y]
    def formalX(self,X):
        return [i.formal()[X] for i in self.sidelist]



game=Platform()
game.setup()
game.run(150)
#game.display()
game.IO_ExcelOne(2,2)

'''抗日战争的动力学模型


模型分为若干回合，每个回合具有一个状态，每个回合的状态决定下一个回合的状态，其中具有一定的随机因素。
每个状态具有四个方面，顺序为国民党，共产党，日本，军阀。
每个状态的更新的规则是，迭代每一方，每一方在固有的发展后(如补充兵力，发展工业)，制定其在这回合中的军事战略，具体为分配多少兵力进攻其他方，分配多少兵力防守。制定后，选择其中最优的执行，轮到下一方，直到每方都这样执行一次为止，开始下一回合。
制定军事战略的方法是，随机生成若干四维随机向量作为决策向量(和为1)，预测每个决策向量运用于状态的影响(这里没有随机因素，故其可以准确的估计决策的影响)。由一个效用函数取各新状态中最优者作为新状态。显而易见，当生成的向量数量充分大时，结果趋近于效用函数值最大化。这里取的数量是200次。
效用函数分为三个部分，即时状态，导状态与长期期望。即时状态记录预期状态的控制区和军队数量等，导状态考虑到下一回合重新轮到自己之前，留下的防守兵力对其他方攻击导致控制区损失的可能影响。长期期望考虑为了遏制最强的一方，可以暂缓对其他弱小方的攻击(自己是最强一方时候就不考虑了)。
除了一般的规则外，每方具有特殊的规则来刻画他们的属性。比如日本具有对美参战度的设定，该参战度会慢慢增加，并逐步减少日本用于战斗的资源。而且日本的工业会直接减少。而且日本占领领土得到的收益比另外三方少得多，而负担却大得多。而共产党具有战斗使双方伤亡小得多的特征，而且资源的获得效率更高。军阀会把更多的兵力用于自保，而且各项资源会向国民党慢慢让渡等(国民党不会进攻军阀，体现国民党对军阀的逐步控制)。
区域具有两个表现形式，正常区域和游击区区域。正常区域会带来收益，而游击区却会减少收益。共产党则从各方的游击区中获得收益。共产党进攻其他方面除了夺取正常区域，更容易扩大游击区。
战斗裁决，每方的一个战斗表现为双方兵力/区域/工业的改变。一般来说一次战斗兵力越多越好，为了简化起见，一方的部分兵力若没有专门用于防守，在下一轮中就不会用于防守。而一次战斗中双方损失比越悬殊，丢失的区域就越多，故各方均会保留一定的防守兵力。抗日战争正面战斗中以大规模会战为主要因素，而对峙对双方影响不大。对此，每方对另一方都具有一个“战机寻觅度”数值，寻觅度是除生成随机向量外唯一的有随机因素影响的因素。寻觅度一般在慢慢上升，每回合都有一定机会激活，寻觅度越高激活的概率越高，而激活的效果也越好(激活后寻觅度下降)。寻觅度最高可以提升该战线进攻方一倍的战力。这样，由于一般防守方更有利，于是双方在一方占优却不能逾越防守优势的障碍时，得到了战机，就可能逾越障碍，发生会战。而战机过去后，障碍恢复作用，又陷入对峙。这样就刻画了抗日战争中会战间隔对峙，对峙间隔会战的情况。当然，就战争开始的时候，日本对中国具有决定性优势，故根本不需要跨越障碍就可以不断的进攻，这一点也可以体现出来。日本一开始就对国民党有100%的寻觅度，体现了初期一线措手不及的情况。

模型的结果是，日本初期可以夺取大量区域，然而攻势越来越慢，随着参战度越来越高，日本资源不足，陷入长期对峙，最后被反攻崩溃。国民党在此时具有最多的区域，随后开始内战(当然由模型的设定，小规模内战从来没停过)，在一段时间战斗后，国民党游击区越来越多，最后像日本一样资源不足而崩溃，共产党取得胜利。这显示了模型的拟合能力还不错。我们可以期望它的结果具有启发性。
当然后面的结果是额外的，我们这里要回答的是共产党在抗日战争中地位的问题。显然，共产党在抗战，对抗日战争当然有贡献，但我们的问题是，如果没有共产党，是不是抗战更容易取胜呢？如果是这样，当然共产党就只有负贡献了。就像本来我们可以赚100块，因为某原因却只能赚50块，那我们实际上是亏了50块而不是赚了50块。
模型的结果是，如果共产党的资源给了军阀和国民党，会把本来的140+回合的胜利加快到120+回合(由于模型中共产党承担了游击队的全部作用，所以如果考虑国民党自己也可以发动游击队可能会更快。)。当然，这只能说在这种可能的情况下共产党的贡献为负，但实际上为什么不能删去国民党或军阀，甚至删去国民党与军阀只保留共产党呢。由于在我们的设定中共产党利用资源的能力更强，所以肯定更可以加快胜利速度。所以这里只反映了一点，即在各派战斗力差异并不是很大的情况下(清朝那种肯定不行，战斗力差距太大了)国家的统一才能发挥最大战斗力。但是，如果只考虑抗日战争时期，这一思索显然意义不大，那么，我们应该怎么看待共产党在抗日战争中的作用呢。我们说，他们在打，正如国民党和军阀们也在打，仅此而已。

'''
