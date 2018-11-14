#include <iostream>
#include <queue>

using namespace std;

class Node:
  public:
    int node, depth

def bfs(int node, vector<vector<int>> edges):
    Node max_node
    max_depth = 0; 

    queue<Node> q; 
    q.push({node, 0})

    vector<int> visited(edges.size(), 0);

    while not q.empty():
        c = q.front(); q.pop()
        visited[c.node] = true

        if c.depth > max_depth:
            max_depth = c.depth
            max_node = c

        for auto dest : edges[c.node]:
            if visited[dest]:
                continue

            q.push({dest, c.depth+1})

    return max_node

def main():
    int n, a, b
    read n

    vector<vector<int>> edges(n+1);
    for i n-1:
        read a, b
        edges[a].push_back(b)
        edges[b].push_back(a)

    node = bfs(1, edges)
    node = bfs(node.node, edges)

    print node.depth
