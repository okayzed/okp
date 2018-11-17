#include <vector>

#include <iostream>
#include <queue>

using namespace std;

class Node {
  public:
    int node, depth; };

auto bfs(int node, vector<vector<int>> edges) {
    Node max_node;
    auto max_depth = 0;

    queue<Node> q;
    q.push({node, 0});

    vector<int> visited(edges.size(), 0);

    while (not q.empty()) {
        auto c = q.front(); q.pop();
        visited[c.node] = true;

        if (c.depth > max_depth) {
            max_depth = c.depth;
            max_node = c; }

        for (auto dest : edges[c.node]) {
            if (visited[dest]) {
                continue; }

            q.push({dest, c.depth+1}); } }

    return max_node; };

int main() {
    int n, a, b;
    cin >> n ;

    vector<vector<int>> edges(n+1);
    for (auto i = 1; i < n; i++) {
        cin >> a >> b ;
        edges[a].push_back(b);
        edges[b].push_back(a); }

    auto node = bfs(1, edges);
    node = bfs(node.node, edges);

    cout << node.depth << endl; };


