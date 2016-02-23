# -*- coding: cp936 -*-
'''yiyuezhuo 616271835@163.com'''
import graph
import random
import copy


map_size_x=20
map_size_y=20
character_dimension=3
agent_number=150
R_factor=0.006
died_percent=0.02
evade_percent=0.7
aggressive_percent=0.7
ada_factor=1
graphics=True
save=True
load=True


testmat=[
    [
        [[1,1,1],[1,1,1],[1,1,1]],
        [[2,2,2],[2,2,2],[2,2,2]],
        [[3,3,3],[3,3,3],[3,3,3]]
        ],
    [
        [[1,1,1],[1,1,1],[1,1,1]],
        [[2,2,2],[2,2,2],[2,2,2]],
        [[3,3,3],[3,3,3],[3,3,3]]
        ],
    [
        [[1,1,1],[1,1,1],[1,1,1]],
        [[2,2,2],[2,2,2],[2,2,2]],
        [[3,3,3],[3,3,3],[3,3,3]]
        ]
    ]

def norm(xv,yv,n):
    return sum([(xv[i]-yv[i])**n for i in range(len(xv))])**(float(1)/n)
def norm2(xv,yv):
    return norm(xv,yv,2)
def vector_plus(x,y):
    return [x[i]+y[i] for i in range(len(x))]
def vector_minus(x,y):
    return [x[i]-y[i] for i in range(len(x))]
def vector_times(x,y):
    return [x[i]*y for i in range(len(x))]
def vector_over(x,y):
    return [x[i]/float(y) for i in range(len(x))]
def vector_avg(l):
    return vector_over(reduce(vector_plus,l),float(len(l)))
def matrix_avg(l):
    nl=null_map()
    for x in range(len(l[0])):
        for y in range(len(l[0][0])):
            nl[x][y]=vector_avg([i[x][y] for i in l])
    return nl
def matrix_D(l):
    avg=matrix_avg(l)
    s=0
    for vec in l:
        for x in range(len(l[0])):
            for y in range(len(l[0][0])):
                s+=norm2(vec[x][y],avg[x][y])
    return s

def norm2_matrix(l):
    matrix=[]
    for i in range(len(l)):
        ll=[]
        for ii in range(len(l)):
            ll.append(norm2(l[i],l[ii]))
        matrix.append(ll)
    return matrix
def cut_matrix(mat,n):
    return [[1 if i<=n else 0 for i in line] for line in mat]
def open_group3(mat):
    s=0
    for x in range(len(mat)):
        for y in range(len(mat[0])):
            if mat[x][y]==1:
                s+=sum(mat[y])
    return s/2
def block_group3(mat):
    s=0
    for x in range(len(mat)):
        for y in range(len(mat[0])):
            if mat[x][y]==1:
                s+=sum([1 if i==1 and mat[i][x]==1 else 0  for i in mat[y]])
    return s/2
def CC_n(l,n):
    cut_mat=cut_matrix(norm2_matrix(l),n)
    op=open_group3(cut_mat)
    bp=block_group3(cut_mat)
    return float(bp)/op

def purelist(l):
    return all([not(iscontainer(i)) for i in l])
def purelist2(l):
    return purelist(l) or all([purelist(i) for i in l])
def iscontainer(t):
    return type(t) in (type([]),type({1:1}),type((1,2)))
    
def tend(l):
    '''将一个列表递归得把所有元素全放到一个表中，使该表没有其他表'''
    p=[]
    for i in l:
        if type(i)==type(1)or type(i)==type(1.0) or type(i)==type(True):
            p.append(i)
        elif type(i)==type({}):
            p.extend(tend(i.values()))
        elif type(i)==type([]):
            p.extend(tend(i))
        else:
            print 'bug'
    return p
def tend1(l):
    if purelist2(l):
        return l[:]
    else:
        kl=[]
        for i in l:
            if iscontainer(i):
                kl=kl+tend1(i)
            else:
                kl.append(i)
        return kl 

def D(l):
    avg=sum(l)/float(len(l))
    return norm2(l,[avg for i in range(len(l))])


def CH(n):
    return abs(n+N())
def CHL(n):
    d=abs(n+N()*0.1)
    if 0<=d<=1:
        return d
    else:
        return d
def CHF(n):
    return n+N()
def CHV(l):
    return [CHF(i) for i in l]
def CHM(mat):
    nm=null_map()
    for x in range(map_size_x):
        for y in range(map_size_y):
            nm[x][y]=CHV(mat[x][y])
    return nm


def N():
    return random.normalvariate(0,1)
def takelow(l):
    '''取值最小的元素的下标'''
    return l.index(min(l))
def takelown(l,n):
    '''取n个最小元素的下标'''
    ll=l[:]
    r=[]
    for i in range(n):
        s=ll.index(min(ll))
        r.append(s)
        ll[s]=max(ll)+1
    return r
def vector_D(l):#这个不是真正的方差，是与平均向量作二范数的和
    avg=vector_avg(l)
    p=sum([norm2(i,avg) for i in l])
    return p
    

def null_map():#注意这里是限制了map_size_x的。不是任意一个map，只能是那个map
    return [{} for i in range(map_size_x)]

def assert_file(s):
    try:
        f=open(s,'rb')
        f.close()
        return True
    except:
        return False

class Agent:
    def __init__(self,ev,ids):
        self.id=ids
        #按照当前设定，下面那些值可以是负的。这显然是不合逻辑的。
        self.isolate=0#此值越大，越容易移入与自己相性不合的格子
        self.aggressive=0#此值越大，越不容易攻击一个差异越小的主体
        self.evade=0#此值越大，越不会去排除冲突，
        self.rational=0#此值越大，对既成事实的接受速度越快
        self.influence=0#此值越大，越容易受周围人投射影响
        self.leadship=0#此值暂不使用，表示引导其他主体的容易程度
        self.ev=ev
        self.character=[0 for i in range(character_dimension)]
        self.map=null_map()
        self.location=self.ev.draw()#这个location存的是图的序号
        self.movement=2
        self.live=True
    def soul(self):
        return (self.isolate,self.aggressive,self.evade,self.rational,self.influence)
    def teach(self,a,b,c,d,e):
        self.isolate=a    #此值越大，越容易移入与自己相性不合的格子
        self.aggressive=b #此值越大，越容易攻击一个差异越小的主体
        self.evade=c      #此值越大，越不会去排除冲突，
        self.rational=d   #此值越大，对既成事实的接受速度越快
        self.influence=e  #此值越大，越容易受周围人投射影响
    def conflict(self):
        #冲突遍历每个其他agent，得出未判定干涉纯冲突图
        conflict_map=null_map()
        for x in range(map_size_x):
            for y in range(map_size_y):
                location=self.ev.xy_to_location(x,y)
                agent_list=self.ev.location_to_agents(location)
                if self in agent_list:#抑制自杀，与另一个配合
                    agent_list.remove(self)
                conflict_map[x][y]=max([norm2(agent.character,self.map[x][y]) for agent in agent_list]) if len(agent_list)!=0 else 0
        return conflict_map
    def interfere(self):
        interfere_map=null_map()
        for x in range(map_size_x):
            for y in range(map_size_y):
                c=norm2(self.character,self.map[x][y])
                interfere_map[x][y]=False if c<=self.evade*evade_percent else True
        return interfere_map
    def peace(self):
        peace_map=null_map()
        for x in range(map_size_x):
            for y in range(map_size_y):
                peace_map[x][y]=True if self.map[x][y]<=self.isolate else False
        return peace_map
    def represent(self):
        represent_map=null_map()
        for x in range(map_size_x):
            for y in range(map_size_y):
                location=self.ev.xy_to_location(x,y)
                agent_list=self.ev.location_to_agents(location)
                represent_map[x][y]=vector_avg([agent.character for agent in agent_list]) if len(agent_list)!=0 else self.map[x][y]
        return represent_map
    def attack_goal(self):
        cm=self.conflict()
        im=self.interfere()
        evil=[]
        evilagent=[]
        evilvalue=[]
        for x in range(map_size_x):
            for y in range(map_size_y):
                if im[x][y]==True and cm[x][y]>=self.aggressive*aggressive_percent and cm[x][y]>0.01:
                    ee=self.ev.xy_to_location(x,y)
                    evil.append(ee)
                    evilvalue.append(cm[x][y])
                    evilagent.append(self.ev.location_to_agents(ee))
        if evil==[]:
            return None,None
        evildistance=[self.ev.graph.distance(self.location,i) for i in evil]
        evilpower=[float(evilvalue[i])/(evildistance[i] if evildistance[i]>0 else 1) for i in range(len(evil))]
        evil_id=evilpower.index(max(evilpower))
        goal_location=evil[evil_id]
        agentlist=evilagent[evil_id]
        x,y=self.ev.location_to_xy(goal_location)
        ll=[norm2(agent.character,self.map[x][y]) if agent !=self else 0 for agent in agentlist]
        #print lls上面那段加了个反自杀
        goal_agent=agentlist[ll.index(max(ll))]
        return goal_location,goal_agent
    def step(self):
        goal_location,goal_agent=self.attack_goal()
        if goal_location==None:
            #print 'walk'
            self.walk()
        else:
            #print 'attack'
            self.attackmove(goal_location,goal_agent)
    def do(self):
        #print 'doing'
        #print self.movement==0
        #print self.libe==False
        while not(self.movement==0 or self.live==False):
            #print 'whiling'
            self.step()
            self.movement-=1
        return 'live' if self.live==True else 'died'

    def walk(self):
        peace_map=self.peace()
        between=self.ev.graph.between(self.location)
        between_xy=[self.ev.location_to_xy(i) for i in between]
        allow=[peace_map[x][y] for (x,y) in between_xy]
        if not(any(allow)):
            obj=between[random.choice(range(len(allow)))]
        else:
            obj=between[random.choice([i for i in range(len(allow)) if allow[i]])]
        self.move(obj)
    def move(self,obj):
        self.location=obj
    def attackmove(self,goal_location,goal_agent):
        if goal_location!=self.location:
            nextstep=self.ev.graph.first_foot(self.location,goal_location)
            self.move(nextstep)
        else:
            self.fight(goal_agent)
    def fight(self,obj):
        #print 'fight!' if obj!=self else 'suicide!'
        if random.random()>=0.5:
            if obj!=self:
                self.ev.kill(obj)
            else:
                self.live=False
        else:
            self.live=False
    def ready(self):
        #这里设平时不会突变，但交叉时会有突变。这里主要发生投射上潜移默化的变化
        self.movement=2
        rm=self.represent()
        for x in range(map_size_x):
            for y in range(map_size_y):
                self.map[x][y]=vector_plus(vector_times(vector_minus(rm[x][y],self.map[x][y]),self.rational*R_factor),self.map[x][y])
                pass
        if random.random<=died_percent:
            self.master.kill(self)
        myxy=self.ev.location_to_xy(self.location)
        linkxy=[self.ev.location_to_xy(i) for i in self.ev.graph.between(self.location)]
        x=myxy[0]
        y=myxy[1]
        self.map[x][y]=vector_plus(vector_times(vector_minus(self.character,self.map[x][y]),self.rational*R_factor*ada_factor),self.map[x][y])
        for (x,y) in linkxy:
            self.map[x][y]=vector_plus(vector_times(vector_minus(self.character,self.map[x][y]),self.rational*R_factor*ada_factor*0.5),self.map[x][y])
        #这里还没写受周围影响的影响
        #另外这个影响本身就好像写的有问题，看上去因为因子太小还是什么原因根本没发挥作用。还要补上周围影响和更大概率的猛然突变。还有自动死亡
        
        
        
                    

class Environment:
    '''这个类负责一些交互函数，统计量以及追踪'''
    def __init__(self):
        self.graph=graph.Graph()
        self.graph.create_grid(map_size_x,map_size_y)
        self.graph.all_analysy()
        self.agent_list=[self.create_agent() for i in range(agent_number)]
        self.monitor_list=[]
        self.turn=0
        if save==True:
            import pickle
            global pickle
    def draw(self):
        return int(random.random()*len(self.graph.matrix))
    def location_to_agents(self,location):
        return [i for i in self.agent_list if i.location==location]
    def xy_to_agents(self,x,y):
        return location_to_agents(self.xy_to_location(x,y))
    def xy_to_location(self,x,y):
        #这两个函数xy都是从0数起的，graph类才要处理那些从1数起的情况
        return x*map_size_y+y
    def location_to_xy(self,location):
        return location//map_size_y,location%map_size_y
    def kill(self,obj):
        #print 'pass'
        self.agent_list.remove(obj)
    def step(self):
        self.killed=[]
        if len(self.agent_list)<agent_number:
            self.agent_list.extend([self.cross_agent() for i in range(agent_number-len(self.agent_list))])
        for i in self.agent_list:
            i.ready()
        for i in self.monitor_list:
            i.run()
        available=copy.copy(self.agent_list)
        #print available
        for act in available:
            #print act
            #print act in self.agent_list
            if act in self.agent_list:
                #print 'in!'
                message=act.do()
                if message=='died':
                    self.kill(act)
        self.turn+=1
        if save==True:
            f=open('modeldata','wb')
            pickle.dump(self,f)
            f.close()
    def go(self,n):
        for i in range(n):
            self.step()
    def create_agent(self):
        ag=Agent(self,N())
        for i in range(map_size_x):
            for ii in range(map_size_y):
                ag.map[i][ii]=[N() for iii in range(character_dimension)]
        ag.character=[N()*3 for i in range(character_dimension)]
        ag.teach(abs(N()*10),abs(N()*10),abs(N()*10),abs(N()*10),abs(N()*10))
        return ag
    def near_agent(self,me,n):
            dis=[self.graph.distance(me.location,agent.location)  for agent in self.agent_list]
            nearagent=[self.agent_list[i] for i in takelown(dis,n)]
            
            return nearagent
    def cross_agent(self):
        if len(self.agent_list)<=10:
            return create_agent()
        else:
            ag=Agent(self,N())
            thenear=self.near_agent(ag,3)
            thesoul=vector_avg([i.soul() for i in thenear])
            thecharacter=vector_avg([i.character for i in thenear])
            themap=matrix_avg([i.map for i in thenear])
            ag.teach(abs(N()*10),abs(N()*10),abs(N()*10),abs(N()*10),abs(N()*10))
            #ag.teach(CH(thesoul[0]),CH(thesoul[1]),CH(thesoul[2]),CH(thesoul[3]),CH(thesoul[4]))
            ag.map=CHM(themap)
            ag.character=CHV(thecharacter)
            return ag
    def add_monitor(self,m):
            self.monitor_list.append(m)
    def trace_map_n(self,n):
        ag=self.agent_list[n]
        mat=[]
        for x in range(map_size_x):
            line=[]
            for y in range(map_size_y):
                line.append(ag.map[x][y])
            mat.append(line)
        return mat
    def trace_map(self):
        return self.trace_map_n(int(agent_number*0.7))
    def recover(self):#这个方法在反序列化后恢复一些设定
        for i in self.monitor_list:
            i.graphics_setup()

class monitor:
    def __init__(self,master):
        self.master=master
        self.log=[]
        if graphics==True:
            self.graphics_setup()
    def matrix_link(self,me):
        s=0
        for x in range(map_size_x):
            for y in range(map_size_y):
                ss=0
                il=self.master.xy_to_location(x,y)
                bl=self.master.graph.between(il)
                bbl=[set(self.master.graph.between(i)) for i in bl]
                tl=reduce(lambda x,y:x&y,bbl)
                for ol in tl:
                    xx,yy=self.master.location_to_xy(ol)
                    dis=self.master.graph.distance(il,ol)
                    ss+=norm2(me.map[x][y],me.map[xx][yy])/(dis if dis>0 else 1)
                '''
                for xx in range(map_size_x):
                    for yy in range(map_size_y):
                        il=self.master.xy_to_location(x,y)
                        yl=self.master.xy_to_location(xx,yy)
                        dis=self.master.graph.distance(il,yl)
                        ss+=norm2(me.map[x][y],me.map[xx][yy])/(dis if dis>0 else 1)
                s+=ss
                '''
                s+=ss
        return s
    def run(self):
        line=int(len(self.master.agent_list)/2)
        agl=self.master.agent_list
        v1=sum([norm2(agl[i].character,agl[i+line].character) for i in range(line)])
        #这个量是逐对比对的是绝对分散度
        v2=vector_D([i.character for i in agl])
        #这个是与平均向量二范数的和
        v30=CC_n([i.character for i in agl],1)
        v31=CC_n([i.character for i in agl],2)
        v32=CC_n([i.character for i in agl],3)
        v33=CC_n([i.character for i in agl],4)
        v34=CC_n([i.character for i in agl],5)
        v35=CC_n([i.character for i in agl],6)
        v36=CC_n([i.character for i in agl],8)
        v37=CC_n([i.character for i in agl],10)
        #这个量是截断量为n=0.1,1,10的聚类系数
        v4=matrix_D([i.map for i in agl])
        #这个量是一大堆东西以上面方式求和的结果。单作用于map上。
        v5=sum([self.matrix_link(self.master.agent_list[i]) for i in range(agent_number)])/agent_number
        #这个量是抽5人样评价投射中的临接情况。由于定义不科学，其值不会降到很低
        print ''
        print self.master.turn
        print v1
        print v2
        print v30,v31,v32,v33,v34,v35,v36,v37
        print v4
        print v5
        self.log.append((self.master.turn,v1,v2,v30,v31,v32,v33,v34,v35,v36,v37,v4,v5))
        if graphics==True:
            self.write_graph()
    def graphics_setup(self):
        import pygame
        import time
        global pygame
        global time
        pygame.init()
        self.size=20
        lx,ly=map_size_x*self.size,map_size_y*self.size
        self.surface=None
        #self.screen=pygame.display.set_mode((lx,ly))
        #self.surface=pygame.Surface((lx,ly))#这样改是为了序列化，尼玛这对象不能序列化
    def write_graph_n(self,n):
        lx,ly=map_size_x*self.size,map_size_y*self.size
        self.surface=pygame.Surface((lx,ly))#这样改是为了序列化，尼玛这对象不能序列化
        mat=self.tend_color(self.master.trace_map_n(n))
        for x in range(map_size_x):
            for y in range(map_size_y):
                for xx in range(self.size):
                    for yy in range(self.size):
                        self.surface.set_at((x*self.size+xx,y*self.size+yy),tuple((mat[x][y])))
        ct=time.ctime()+'.bmp'
        ct=ct.replace(':',' ')
        pygame.image.save(self.surface,ct)
        self.surface=None
    def write_graph(self):
        self.write_graph_n(int(agent_number*0.7))
    def tend_color(self,mat):
        #这个函数把map归一化到RGB色区间上。
        fl=tend1(mat)
        minR=min(fl,key=lambda x:x[0])[0]
        maxR=max(fl,key=lambda x:x[0])[0]
        minG=min(fl,key=lambda x:x[1])[1]
        maxG=max(fl,key=lambda x:x[1])[1]
        minB=min(fl,key=lambda x:x[2])[2]
        maxB=max(fl,key=lambda x:x[2])[2]
        f=lambda t,minb,maxb:int(((t-minb)/float(maxb-minb))*255)
        return [[[f(mat[x][y][0],minR,maxR),f(mat[x][y][1],minG,maxG),f(mat[x][y][2],minB,maxB)] for y in range(len(mat[0])) ] for x in range(len(mat))]
                
                        
 
        
if load ==True and assert_file('modeldata'):
    import pickle
    f=open('modeldata','rb')
    myev=pickle.load(f)
    myev.recover()
else:
    myev=Environment()
    mon=monitor(myev)
    myev.add_monitor(mon)

myev.go(1000)
raw_input( 'mizho!')
        

'''
这里要衡量两个量，实质多样化量和投射多样化量。

实质多样化量是说，个体本身的表属性的分类程度。
这里又有两个量度，平分散度和聚类分散度。平分散度是直接衡量数据差异的，刻画规律性无法刻画动态平衡的多分化系统。
聚类分散度刻画聚类的程度。对绝对无规律分散值较高。对一体和多体聚集都有较低的值。

投射多样化直接比较平分散度，应为多体分散度肯定是不稳定的(不过也可以看看)。


向量组的绝对分散度可以直接用方差，我用的是逐对比较二范数求和。
向量组的截断聚类分散度是，指定一个截断数。如果两个向量范数小于此数，被认为相连，然后用全局聚类系数计算。
向量组的蒙特卡洛聚类分散度是，放若干个爬虫到一个向量上，以一个分布(越近的越容易爬到)不断爬行n轮(称为n蒙卡特罗分散度)。最后以所有爬虫离原向量距离计算分散度。所有节点都进行一次然后求和。

区域分野分散度
指混乱的点成为区域的度量
假设最小化法，通过一步一步引入更多的结构研究它们的平衡态与演进速度的关系。

秩序演进论

这里有若干主体，每个主体具有一组属性刻画它的行为。以及一组外特征刻画它的行为无关的属性。主体会把外特征投射到地图上。一旦在他看来外属性相差较大的其他主体在地图一点上，他就会去解决。

主体会在他自认为无冲突的点游荡，但若在某些点上与其他主体看法不一。导致被“解决”，这样就发生了投射的同化，一个异化的投射被移除了。最后某个投射获得一致通过。不再有大冲突，主体根据特征分为若干个群，占据特定的(通常是连成片的)的节点。
'''
