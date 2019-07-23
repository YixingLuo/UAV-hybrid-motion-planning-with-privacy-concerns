import numpy as np
def dfs(u,v):
    print(u,v)
    A[u, v] = num+1
    vis[u][v]=1
    for i in range(4):
        newx=u+x[i]
        newy=v+y[i]
        if newx<0 or newx>n-1 or newy<0 or newy>=m-1:
            continue
        if vis[newx][newy]== 0 and A[newx][newy]==1:
            dfs(newx,newy)

if __name__== '__main__':
    num = 0
    maxn = 50

    A=np.loadtxt('map1.txt',delimiter=' ')
    print(A)

    n=A.shape[0]
    m=A.shape[1]
    print(n,m)

    x=[0,0,1,-1]
    y=[1,-1,0,0]
    vis=np.zeros((maxn,maxn))
    print(type(vis))
    print(vis)
    for i in range(n):
        for j in range(m):
            if vis[i][j]==0 and A[i][j]==1:
                dfs(i,j)
                print("\n")
                num+=1
                #A[i,j]=num
    np.savetxt("maplabel.txt", A, fmt='%d', delimiter=' ')
    print("连通字块个数：",num)
