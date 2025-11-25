#include <bits/stdc++.h>
using namespace std;

using Perm = vector<int>;

Perm compose(const Perm& a, const Perm& b){
    int n=a.size()-1;
    Perm r(n+1);
    for(int i=1;i<=n;i++) r[i]=a[b[i]];
    return r;
}

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int E;
    if(!(cin>>E)) return 0;
    vector<pair<int,int>> e1(E), e2(E);
    int mx=0;
    for(int i=0;i<E;i++){
        int a,b; cin>>a>>b; if(a>b) swap(a,b);
        e1[i]={a,b}; mx=max(mx,max(a,b));
    }
    for(int i=0;i<E;i++){
        int a,b; cin>>a>>b; if(a>b) swap(a,b);
        e2[i]={a,b}; mx=max(mx,max(a,b));
    }
    int n=mx;
    
    vector<vector<int>> A(n+1, vector<int>(n+1,0)), B(n+1, vector<int>(n+1,0));
    for(auto [u,v]:e1){A[u][v]=A[v][u]=1;}
    for(auto [u,v]:e2){B[u][v]=B[v][u]=1;}
    
    vector<int> degA(n+1,0), degB(n+1,0);
    for(int i=1;i<=n;i++){
        for(int j=1;j<=n;j++){degA[i]+=A[i][j]; degB[i]+=B[i][j];}
    }
    
    vector<int> order(n);
    iota(order.begin(),order.end(),1);
    sort(order.begin(),order.end(),[&](int x,int y){
        if(degA[x]!=degA[y]) return degA[x]>degA[y];
        return x<y;
    });
    
    vector<int> used(n+1,0), p(n+1,0);
    function<bool(int)> dfsIso=[&](int idx)->bool{
        if(idx==(int)order.size()) return true;
        int v=order[idx];
        for(int w=1;w<=n;w++){
            if(used[w]) continue;
            if(degA[v]!=degB[w]) continue;
            bool ok=true;
            for(int i=0;i<idx;i++){
                int u=order[i];
                if(A[v][u] && p[u]!=0 && !B[w][p[u]]) {ok=false; break;}
                if(!A[v][u] && p[u]!=0 && B[w][p[u]]) {ok=false; break;}
            }
            if(!ok) continue;
            used[w]=1; p[v]=w;
            if(dfsIso(idx+1)) return true;
            used[w]=0; p[v]=0;
        }
        return false;
    };
    dfsIso(0);
    
    Perm target_inv(n+1);
    for(int i=1;i<=n;i++) target_inv[p[i]] = i;
    
    vector<vector<int>> adj(n+1);
    for(int i=1;i<=n;i++)
        for(int j=i+1;j<=n;j++)
            if(A[i][j]){ adj[i].push_back(j); adj[j].push_back(i); }
    
    vector<vector<int>> cycles;
    vector<int> usedv(n+1,0), path;
    function<void(int,int)> dfsCyc = [&](int s,int u){
        for(int v:adj[u]){
            // if(v==s) continue;
            if(v==s && (int)path.size()>=3){
                cycles.push_back(path);
                continue;
            }
            if(!usedv[v] && v>s){
                usedv[v]=1; path.push_back(v);
                dfsCyc(s,v);
                path.pop_back(); usedv[v]=0;
            }
        }
    };
    
    for(int s=1;s<=n;s++){
        usedv.assign(n+1,0);
        usedv[s]=1; path.clear(); path.push_back(s);
        dfsCyc(s,s);
    }
    
    vector<Perm> gens;
    for(auto &cy:cycles){
        int k=cy.size();
        Perm t(n+1); iota(t.begin(),t.end(),0);
        for(int i=0;i<k;i++){
            int a=cy[i], b=cy[(i+1)%k];
            t[a]=b;
        }
        gens.push_back(t);
        Perm t2(n+1); iota(t2.begin(),t2.end(),0);
        for(int i=0;i<k;i++){
            int a=cy[i], b=cy[(i-1+k)%k];
            t2[a]=b;
        }
        gens.push_back(t2);
    }
    
    Perm id(n+1); iota(id.begin(),id.end(),0);
    if(target_inv==id){ cout<<0; return 0; }
    
    queue<Perm> q;
    unordered_map<string,int> dist;
    auto key=[&](const Perm& pr){
        string s; s.reserve(n*3);
        for(int i=1;i<=n;i++){ s.push_back('#');
            s+=to_string(pr[i]); }
        return s;
    };
    q.push(id); dist[key(id)]=0;
    int ans=-1;
    while(!q.empty()){
        auto cur=q.front(); q.pop();
        int d=dist[key(cur)];
        for(auto &g:gens){
            Perm nxt = compose(g,cur);
            string kstr=key(nxt);
            if(!dist.count(kstr)){
                dist[kstr]=d+1;
                if(nxt==target_inv){ ans=d+1; cout<<ans; return 0; }
                q.push(nxt);
            }
        }
    }
    cout<<-1;
    return 0;
}