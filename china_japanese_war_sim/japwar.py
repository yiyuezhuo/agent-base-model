# -*- coding: cp936 -*-
# by yiyuezhuo
import random
import copy
#������

#����Ϊ������
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
#ȫ�ֺ�����
class Platform:
    def __init__(self,sidenumber=4):
        self.history=[]
        self.statue=None
        self.sidenumber=sidenumber
    def setup(self):
        namelist=['KMT','CP','JAP','WAL']
        #��ʼ����Ӧ����200������30���λ�����ʽ����
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
        #�����ǽ������б��ʽת�ɶ��ŷָ��ַ����б�����1��2,3�Ǹ�ͷ��
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
        self.defend=army#��ʼĬ�Ϸ��أ������㶮��
        self.industry=industry
        self.resources=0
        self.infiltration=infiltration
        self.control=control
        self.aid=aid
        self.allside=namelist#����ֻ�����֣����Ƕ���
        self.namelist=namelist
        self.sidenumber=len(namelist)
        self.thinking=200
        #self.US=US
        self.opportunity=[0 for i in range(len(namelist)-1)]
        self.bonus=[1.0 for i in range(len(namelist)-1)]
    def value(self,statue):#�����������Ҳֻ����ת��ʱʹ�ã����Ե�Ȼ��statue����
        enmey=sum([(i.army+i.defend) for i in statue.otherside(self.name)])
        if self.defend==0:
            threat=enmey/0.0001*self.land
        else:
            threat=enmey/self.defend*self.land
        return self.land*10+self.army*0.01+self.control-self.infiltration*0.2+\
               statue.diplomacy(self.name)-threat
    def product(self):
        #n������Ϊ����n�����ܵĵ����⻹���Լ��ķ��ر���(������������Ͳ�������)
        return [randomvector(self.sidenumber) for i in range(self.thinking)]
    def update(self,statue):
        #�������⺯��֮һ��������Ҫͨ��statue�޸����ݡ�
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
        #�������⺯��֮һ��
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
                selfing.army+=(ASS-AS)/bonus[ii]#����д��ʾ�ӳɻ��ܼ���������д���ұ����ʾֻ����ɱ�˲���������
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
        #�������⺯��֮һ��������Ҫͨ��statue�޸����ݡ�
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
        #�������⺯��֮һ��������Ҫͨ��statue�޸����ݡ�
        self.industry*=0.99
        self.army+=self.defend
        self.defend=0
        income=self.land*0.2+self.control*0.1+self.aid+self.industry
        outcome=self.infiltration*0.7+self.army*0.01
        #�ձ�������(�й�)�л�õ�������٣���Ҫ������ҵ��
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
                self.opportunity[i]+=0.1#�ձ�ӵ�и�ǿ��ս��Ѱ������
class CWAL(Side):
    def __init__(self,name,land,army,industry,infiltration,control,aid,namelist):
        Side.__init__(self,name,land,army,industry,infiltration,control,aid,namelist)
    def product(self):
        return [focus_vector(randomvector(self.sidenumber),0.9,3) for i in range(self.thinking)]
class CCP(Side):
    def __init__(self,name,land,army,industry,infiltration,control,aid,namelist):
        Side.__init__(self,name,land,army,industry,infiltration,control,aid,namelist)
    def update(self,statue):
        #�������⺯��֮һ��������Ҫͨ��statue�޸����ݡ�
        self.industry*=1.02
        self.army+=self.defend
        self.defend=0
        income=self.land*1.5+self.control*0.5+self.aid+self.industry*1.5
        outcome=self.infiltration*0.5+self.army*0.005
        #���������и��ߵĵ�����������͵�ά�ַ�
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
        p=0.4 #ռ������ǿ��Ƶı���
        AF=0.02#������ս����ʽʹ�ط�û�����Ʋ���С˫��������
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

'''����ս���Ķ���ѧģ��


ģ�ͷ�Ϊ���ɻغϣ�ÿ���غϾ���һ��״̬��ÿ���غϵ�״̬������һ���غϵ�״̬�����о���һ����������ء�
ÿ��״̬�����ĸ����棬˳��Ϊ���񵳣����������ձ���������
ÿ��״̬�ĸ��µĹ����ǣ�����ÿһ����ÿһ���ڹ��еķ�չ��(�粹���������չ��ҵ)���ƶ�������غ��еľ���ս�ԣ�����Ϊ������ٱ���������������������ٱ������ء��ƶ���ѡ���������ŵ�ִ�У��ֵ���һ����ֱ��ÿ��������ִ��һ��Ϊֹ����ʼ��һ�غϡ�
�ƶ�����ս�Եķ����ǣ��������������ά���������Ϊ��������(��Ϊ1)��Ԥ��ÿ����������������״̬��Ӱ��(����û��������أ��������׼ȷ�Ĺ��ƾ��ߵ�Ӱ��)����һ��Ч�ú���ȡ����״̬����������Ϊ��״̬���Զ��׼��������ɵ�����������ִ�ʱ�����������Ч�ú���ֵ��󻯡�����ȡ��������200�Ρ�
Ч�ú�����Ϊ�������֣���ʱ״̬����״̬�볤����������ʱ״̬��¼Ԥ��״̬�Ŀ������;��������ȣ���״̬���ǵ���һ�غ������ֵ��Լ�֮ǰ�����µķ��ر������������������¿�������ʧ�Ŀ���Ӱ�졣������������Ϊ�˶�����ǿ��һ���������ݻ���������С���Ĺ���(�Լ�����ǿһ��ʱ��Ͳ�������)��
����һ��Ĺ����⣬ÿ����������Ĺ������̻����ǵ����ԡ������ձ����ж�����ս�ȵ��趨���ò�ս�Ȼ��������ӣ����𲽼����ձ�����ս������Դ�������ձ��Ĺ�ҵ��ֱ�Ӽ��١������ձ�ռ�������õ�����������������ٵö࣬������ȴ��öࡣ������������ս��ʹ˫������С�ö��������������Դ�Ļ��Ч�ʸ��ߡ�������Ѹ���ı��������Ա������Ҹ�����Դ������������öɵ�(���񵳲���������������ֹ��񵳶Ծ������𲽿���)��
�����������������ʽ������������λ����������������������棬���λ���ȴ��������档��������Ӹ������λ����л�����档��������������������˶�ȡ�������򣬸����������λ�����
ս���þ���ÿ����һ��ս������Ϊ˫������/����/��ҵ�ĸı䡣һ����˵һ��ս������Խ��Խ�ã�Ϊ�˼������һ���Ĳ��ֱ�����û��ר�����ڷ��أ�����һ���оͲ������ڷ��ء���һ��ս����˫����ʧ��Խ���⣬��ʧ�������Խ�࣬�ʸ������ᱣ��һ���ķ��ر���������ս������ս�����Դ��ģ��սΪ��Ҫ���أ������Ŷ�˫��Ӱ�첻�󡣶Դˣ�ÿ������һ��������һ����ս��Ѱ�ٶȡ���ֵ��Ѱ�ٶ��ǳ��������������Ψһ�����������Ӱ������ء�Ѱ�ٶ�һ��������������ÿ�غ϶���һ�����ἤ�Ѱ�ٶ�Խ�߼���ĸ���Խ�ߣ��������Ч��ҲԽ��(�����Ѱ�ٶ��½�)��Ѱ�ٶ���߿���������ս�߽�����һ����ս��������������һ����ط�������������˫����һ��ռ��ȴ������Խ�������Ƶ��ϰ�ʱ���õ���ս�����Ϳ�����Խ�ϰ���������ս����ս����ȥ���ϰ��ָ����ã���������š������Ϳ̻��˿���ս���л�ս������ţ����ż����ս���������Ȼ����ս����ʼ��ʱ���ձ����й����о��������ƣ��ʸ�������Ҫ��Խ�ϰ��Ϳ��Բ��ϵĽ�������һ��Ҳ�������ֳ������ձ�һ��ʼ�ͶԹ�����100%��Ѱ�ٶȣ������˳���һ�ߴ��ֲ����������

ģ�͵Ľ���ǣ��ձ����ڿ��Զ�ȡ��������Ȼ������Խ��Խ�������Ų�ս��Խ��Խ�ߣ��ձ���Դ���㣬���볤�ڶ��ţ���󱻷��������������ڴ�ʱ���������������ʼ��ս(��Ȼ��ģ�͵��趨��С��ģ��ս����ûͣ��)����һ��ʱ��ս���󣬹����λ���Խ��Խ�࣬������ձ�һ����Դ�����������������ȡ��ʤ��������ʾ��ģ�͵�����������������ǿ����������Ľ�����������ԡ�
��Ȼ����Ľ���Ƕ���ģ���������Ҫ�ش���ǹ������ڿ���ս���е�λ�����⡣��Ȼ���������ڿ�ս���Կ���ս����Ȼ�й��ף������ǵ������ǣ����û�й��������ǲ��ǿ�ս������ȡʤ�أ��������������Ȼ��������ֻ�и������ˡ����������ǿ���׬100�飬��Ϊĳԭ��ȴֻ��׬50�飬������ʵ�����ǿ���50�������׬��50�顣
ģ�͵Ľ���ǣ��������������Դ���˾����͹��񵳣���ѱ�����140+�غϵ�ʤ���ӿ쵽120+�غ�(����ģ���й������е����λ��ӵ�ȫ�����ã�����������ǹ����Լ�Ҳ���Է����λ��ӿ��ܻ���졣)����Ȼ����ֻ��˵�����ֿ��ܵ�����¹������Ĺ���Ϊ������ʵ����Ϊʲô����ɾȥ���񵳻����������ɾȥ���������ֻ�����������ء����������ǵ��趨�й�����������Դ��������ǿ�����Կ϶������Լӿ�ʤ���ٶȡ���������ֻ��ӳ��һ�㣬���ڸ���ս�������첢���Ǻܴ�������(�峯���ֿ϶����У�ս�������̫����)���ҵ�ͳһ���ܷ������ս���������ǣ����ֻ���ǿ���ս��ʱ�ڣ���һ˼����Ȼ���岻����ô������Ӧ����ô�����������ڿ���ս���е������ء�����˵�������ڴ�������񵳺;�����Ҳ�ڴ򣬽��˶��ѡ�

'''
