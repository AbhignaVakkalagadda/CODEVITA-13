#include <bits/stdc++.h>
using namespace std;

int m,n,l;
char a[20][20];
int dx[4]={-1,0,1,0},dy[4]={0,1,0,-1};
int v[20][20][2];

struct S{int x,y,o,d;};

bool ok(int x,int y){return x>=0&&x<m&&y>=0&&y<n;}

bool can(int x,int y,int o){
    for(int i=0;i<l;i++){
        int nx=x+(o?0:i);
        int ny=y+(o?i:0);
        if(!ok(nx,ny)||a[nx][ny]=='B')return 0;
    }
    return 1;
}

bool rot(int x,int y,int o){
    for(int i=0;i<l;i++)for(int j=0;j<l;j++){
        int nx=x+(o?j:i);
        int ny=y+(o?i:j);
        if(!ok(nx,ny)||a[nx][ny]=='B')return 0;
    }
    return 1;
}

int bfs(int sx,int sy,int so,int ex,int ey,int eo){
    queue<S>q;
    memset(v,-1,sizeof(v));
    q.push({sx,sy,so,0});
    v[sx][sy][so]=0;
    while(!q.empty()){
        S c=q.front();q.pop();
        int x=c.x,y=c.y,o=c.o,d=c.d;
        if(x==ex&&y==ey&&o==eo)return d;
        for(int i=0;i<4;i++){
            int nx=x+dx[i],ny=y+dy[i];
            if(can(nx,ny,o)&&v[nx][ny][o]==-1){
                v[nx][ny][o]=d+1;
                q.push({nx,ny,o,d+1});
            }
        }
        int no=1-o;
        if(rot(x,y,o)&&v[x][y][no]==-1){
            v[x][y][no]=d+1;
            q.push({x,y,no,d+1});
        }
    }
    return -1;
}

int main(){
    cin>>m>>n;
    int i,j,sx,sy,so,ex,ey,eo;
    vector<pair<int,int>>si,sl;
    for(i=0;i<m;i++)for(j=0;j<n;j++){
        cin>>a[i][j];
        if(a[i][j]=='I')si.push_back({i,j});
        if(a[i][j]=='L')sl.push_back({i,j});
    }
    l=si.size();
    sx=si[0].first;sy=si[0].second;so=0;
    if(si[1].first==sx)so=1,sy=si[1].second;
    ex=sl[0].first;ey=sl[0].second;eo=0;
    if(sl[1].first==ex)eo=1,ey=sl[1].second;
    int ans=bfs(sx,sy,so,ex,ey,eo);
    cout<<(ans<0?"Impossible":to_string(ans));
}
