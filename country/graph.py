# -*- coding: cp936 -*-
'''yiyuezhuo��ͼ��ģ�飬֧������ͼ�Ľ�����ʽ�����巨����󷨡�����������ж�������̾��룬�������·�������ŵ�һ���ȡ�������ֱ�������ı�ͼ���ı߸�ѭ��ͼ
����Ȥ�߿�����ϵ616271835@163.com'''
#ͼ�ṹʹ�þ���������0��ʾ�����ӡ�����ֵ��ʾȨ����ṹ������ʾ

pathmax0=[[0,1,0],
         [1,0,1],
         [0,0,1]]

#������һ���б���ָ��������еĻ���
#namelist0=['left','midlle','right']
def nullchar(n):
    '''����n�������ո�'''
    l=''
    for i in range(n):
        l=l+' '
    return l
def formal_line(line,block):
    '''��һ���ַ��鰴һ�����������ʽ��'''
    l=''
    for word in line:
        l=l+word+nullchar(block-len(word))
    return l
def tend(l):
    '''��һ���б�ݹ�ð�����Ԫ��ȫ�ŵ�һ�����У�ʹ�ñ�û��������'''
    p=[]
    for i in l:
        if type(i)!=type([]):
            p.append(i)
        else:
            p.extend(tend(i))
    return p
def T_mat(mat):
    '''ת�þ���'''
    x,y=len(mat),len(mat[0])
    zero=[[0 for tt in  range(x)] for t in range(y)]
    for ix in range(x):
        for iy in range(y):
            zero[iy][ix]=mat[ix][iy]
    return zero
def listtostr(l):
    '''���б�תΪ�ַ���'''
    s=''
    for i in l:
        s=s+str(i)+' '
    return s
def matrix_display(mat,T=False):
    '''�������ʽ����ӡ����'''
    b=max([len(str(abs(i))) for i in tend(mat)])+1
    if T==True:
        mat=T_mat(mat)
    for i in mat:
        print formal_line([str(ii) for ii in i],b)
    
        
    
def back_dict(dic,value):
    '''����ȡ�б��ֵ'''
    for i in dic:
        if dic[i]==value:
            return i
    return None
def load(file_name):
    '''����һ���ļ�������һ������ͼ�õ���Ԫ��'''
    f=open(file_name,'r')
    l=f.readlines()
    f.close()
    namelist=[]
    matrix=[]
    statue='define'
    for i in l:
        #print i
        if statue=='define':
            if not('end' in i):
                namelist.append(i[:-1])
            else:
                statue='matrix'
        elif statue=='matrix':
            if not('end'in i):
                number_squ=[int(x) for x in i.split()]
                matrix.append(number_squ)
            else:
                break
    return (matrix,namelist)
def pre_load(file_name):
    '''����һ���ļ�������һ������ͼ�õ���Ԫ�顣������ʽ����'''
    #����ʽ�ļ����������ж��ٸ��㡣Ȼ��ʼ����������������·������������δ��ʾ����������δ֪��0.
    #���ǰ��Ҫ���жԳƻ���������������X��ӦĬ�϶Գ�,���ǵ�����
    f=open(file_name)
    l=f.readlines()
    ll=[i[:-1] for i in l]
    if ll[len(ll)-1]=='en':
        ll[len(ll)-1]='end'
    f.close()
    matrix=[]
    namelist={}
    statue='claim'
    k=0
    name_list={}
    #print ll
    for l in ll:
        #print l
        if statue=='claim':
            #print ('end' in l)
            if ('end' in l):
                statue='name'
                #print 'turn'
        elif statue=='name':
            if not( 'end' in l):
                #���������һ�����ֺ�һ���ַ������
                u=l.split()
                if len(u)==1:
                    name=u[0]
                    name_list[k]=name
                    k+=1
                else:
                    number=int(u[0])
                    k=number+1
                    name=u[1]
                    name_list[number]=name
                #print 'hit'
            else:
                statue='path'
                print name_list.keys()
                length=max(name_list.keys())+1
                matrix=[[0 for x in range(length)] for y in range(length)]
        elif statue=='path':
            if not( 'end' in l):
                #�������������x,y,cost��¼���Լ�һ�����ƴ�����Ϊ����(��ѡ)�ı��
                p=l.split()
                x,y,cost=p[0],p[1],p[2]
                if x in name_list.values() and y in name_list.values():
                    x,y,cost=int(back_dict(name_list,p[0])),int(back_dict(name_list,p[1])),int(p[2])
                else:
                    x,y,cost=int(p[0]),int(p[1]),int(p[2])
                if len(p)==3:
                    matrix[x][y]=cost
                    matrix[y][x]=cost
                elif len(p)==4 and p[3]=='!':
                    matrix[x][y]=cost
            else:
                break
    if len(namelist)==len(matrix):
        nl=zip(name_list.keys(),name_list.values())
        return (matrix,[i[1] for i in sorted(nl,key=lambda t:t[0])])
    else :
        nl=zip(name_list.keys(),name_list.values())
        ntr=[i[1] for i in sorted(nl,key=lambda t:t[0])]
        ntrr=ntr+['unknow' for i in range(len(namelist)-len(matrix))]
        return (matrix,ntrr)
        
            

#z=load('ss.txt')
#print z[0]
            
class Graph:
    '''ͼ���Զ�����'''
    def __init__(self):
        self.matrix=[]
        self.name_list=[]
    def create_by_file(self,file_name):
        '''���ļ���ʼ��һ��ͼ'''
        y=load(file_name)
        self.matrix=y[0]
        self.name_list=y[1]
    def create_by_file_define(self,file_name):
        '''���ļ���ʼ��һ��ͼ'''
        y=pre_load(file_name)
        self.matrix=y[0]
        self.name_list=y[1]
    def create_by_define(self,matrix,name_list):
        '''������Ԫ���ʼ��һ��ͼ'''
        self.matrix=matrix
        self.name_list=name_list
    def create_grid(self,x,y,dis=1,circle=False):
        '''��ʼ��һ����������'''
        matrix=[[0 for i in range(x*y)] for ii in range(x*y)]
        namelist=[str(i) for i in range(x*y)]
        f=lambda xx,yy:xx*y+yy
        if circle==False:
            for ix in range(x):
                for iy in range(y):
                    if ix-1>=0:#up
                        matrix[f(ix,iy)][f(ix-1,iy)]=dis
                    if ix+1<x:
                        matrix[f(ix,iy)][f(ix+1,iy)]=dis
                    if iy-1>=0:
                        matrix[f(ix,iy)][f(ix,iy-1)]=dis
                    if iy+1<y:
                        matrix[f(ix,iy)][f(ix,iy+1)]=dis
        else:
            for ix in range(x):
                for iy in range(y):
                    if ix-1>=0:#up
                        matrix[f(ix,iy)][f(ix-1,iy)]=dis
                    else:
                        matrix[f(ix,iy)][f(x,iy)]=dis
                    if ix+1<x:
                        matrix[f(ix,iy)][f(ix+1,iy)]=dis
                    else:
                        matrix[f(ix,iy)][f(0,iy)]=dis
                    if iy-1>=0:
                        matrix[f(ix,iy)][f(ix,iy-1)]=dis
                    else:
                        matrix[f(ix,iy)][f(ix,y)]=dis
                    if iy+1<y:
                        matrix[f(ix,iy)][f(ix,iy+1)]=dis
                    else:
                        matrix[f(ix,iy)][f(ix,0)]=dis
        self.matrix=matrix
        self.name_list=namelist          
    def between(self,location):
        '''���-����һ������ڽӵ�'''
        location=self.pure(location)
        #print self.matrix[location]
        between_list=[i for i in range(len(self.matrix[location])) if self.matrix[location][i]!= 0]
        return between_list
    def between_for_name(self,location):
        '''����-����һ������ٽ��'''
        name_list=self.for_name(between(location))
        return name_list
    def pure(self,location):
        '''�����������ֺ�λ�ö�ӳ��Ϊ����'''
        if type(location)==type(1):
            real_index=location
        elif type(location)==type('1'):
            real_index=self.name_list.index(location)
        else:
            raise TypeError
        return real_index
    def for_name(self,index_list):
        '''����һ���������У�����һ���������'''
        return [self.name_list[i] for i in index_list]
    def analysy(self,x):
        '''���һ���㵽��������������'''
        x=self.pure(x)
        min_cost_list=self.matrix[x][:]
        matrix=self.matrix
        focus_list=[i for i in range(len(min_cost_list)) if min_cost_list[i]!=0]
        while len(focus_list)!=0:
            #print focus_list
            temp_list=[]
            for focusing in focus_list:
                base=min_cost_list[focusing]
                for checking in range(len(matrix[focusing])):
                    if matrix[focusing][checking]!=0 and min_cost_list[checking]==0:
                        min_cost_list[checking]=base+matrix[focusing][checking]
                        temp_list.append(checking)
                    elif matrix[focusing][checking]!=0 and min_cost_list[checking]!=0:
                        if base+matrix[focusing][checking] < min_cost_list[checking]:
                            min_cost_list[checking]=base+matrix[focusing][checking]
                            temp_list.append(checking)
                focus_list=temp_list
        return min_cost_list
    def all_analysy(self):
        '''������е㵽�������������룬�����浽sll_distance������'''
        self.all_distance=[]
        for i in range(len(self.matrix)):
            #print 'y'
            cl=self.analysy(i)
            self.all_distance.append(cl)
        #print self.all_distance
    def distance(self,x,y):
        '''�ж�x,y�ľ��롣��Ҫ֮ǰ����ȫ����'''
        x,y=self.pure(x),self.pure(y)
        if self.all_distance[x][y]!=0:
            return self.all_distance[x][y]
        else:
            return 0
    def path(self,x,y):
        '''���x��y�����ͨ·����Ҫȫ������������Ϊ������x��Ŀ�ĵ�y'''
        x,y=self.pure(x),self.pure(y)
        if self.all_distance[x][y]==0:
            return []
        x,y=self.pure(x),self.pure(y)
        ing=x
        path=[]
        while not (y in self.between(ing)):
            #print ing
            b=self.between(ing)
            costlist=[self.distance(i,y) if self.distance(i,y)!=0 else 10000 for i in b ]
            ing=b[costlist.index(min(costlist))]#����ܶ�۵㣬����10000����ͷ�ֵ��ʵ������ǿ��ϵ�
            path.append(ing)
        path.append(y)
        return path
    def first_foot(self,x,y):
        '''�����x��y��Ҫ�߳��ĵ�һ������Ҫȫ����'''
        return self.path(x,y)[0]
    def link(self,x,y):
        '''�ж�x,y�Ƿ���ͨ����Ҫȫ����'''
        return True if self.all_distance[self.pure(x)][self.pure(y)]!=0 else False#����ж��ǶԵģ�0������Ǳ�ʾ�����ӣ�����path��С��Ϊ������(˳��֧���������)û��ר���ж�0�����������
        
    
                
            

def test1():
    ig=Graph()
    ig.create_by_file('ss.txt')
    ig.all_analysy()
    '''
    print ig.between(0)
    print ig.between(1)
    print ig.between(2)
    print ig.between(3)
    print ig.between('left')
    '''
    print ig.analysy('left')
    print ig.path('left','right')
def test2():
    ig=Graph()
    ig.create_by_file_define('t.txt')
    print ig.matrix
#test2()
'''
ig=Graph()
ig.create_grid(6,6)
ig.all_analysy()
matrix_display(ig.matrix)
'''



'''
Hello world
end
beijing
jian
chengdu
shanghai
guangzhou
end
beijing jian 10
chengdu shanghai 5
guangzhou jian 1
end
'''

