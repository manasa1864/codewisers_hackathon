"""
generate_data.py  —  CareerForge data generator
  * Every problem has at least one link (leetcode OR blog)
  * topic["total"] matches len(problems) exactly (no hardcoding)
  * Correct answer is always options[0] here.
    questions.py shuffles options deterministically at serve-time,
    so the client never sees option-A as always correct.
"""
import json, os

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
GFG = "https://www.geeksforgeeks.org"
LC  = "https://leetcode.com/problems"

# ─────────────────────────────────────────────────────────────────
#  QUESTION BANK  (110 questions)
# ─────────────────────────────────────────────────────────────────
DSA_QUESTIONS = [
  # EASY
  {"id":1,"section":"DSA","difficulty":"easy","question":"What is the output of reversing the array [1,2,3,4,5]?","options":["[5,4,3,2,1]","[1,2,3,4,5]","[5,3,1,4,2]","[2,4,1,3,5]"],"correct_answer":"[5,4,3,2,1]","tags":["arrays"]},
  {"id":2,"section":"DSA","difficulty":"easy","question":"Time complexity of accessing an element in an array by index?","options":["O(1)","O(n)","O(log n)","O(n^2)"],"correct_answer":"O(1)","tags":["arrays","complexity"]},
  {"id":3,"section":"DSA","difficulty":"easy","question":"Which data structure uses FIFO order?","options":["Queue","Stack","Heap","Tree"],"correct_answer":"Queue","tags":["queue"]},
  {"id":4,"section":"DSA","difficulty":"easy","question":"push(1); push(2); pop() — what value is returned?","options":["2","1","Empty","Error"],"correct_answer":"2","tags":["stack"]},
  {"id":5,"section":"DSA","difficulty":"easy","question":"Inorder traversal of a BST produces?","options":["Sorted ascending order","Sorted descending order","Level order","Reverse order"],"correct_answer":"Sorted ascending order","tags":["trees","bst"]},
  {"id":6,"section":"DSA","difficulty":"easy","question":"Worst-case time complexity of bubble sort?","options":["O(n^2)","O(n log n)","O(n)","O(log n)"],"correct_answer":"O(n^2)","tags":["sorting"]},
  {"id":7,"section":"DSA","difficulty":"easy","question":"A linked list node contains a value and a?","options":["Pointer to the next node","Array index","Parent pointer","Random integer"],"correct_answer":"Pointer to the next node","tags":["linked-list"]},
  {"id":8,"section":"DSA","difficulty":"easy","question":"BFS uses which data structure internally?","options":["Queue","Stack","Heap","Array"],"correct_answer":"Queue","tags":["graphs","bfs"]},
  {"id":9,"section":"DSA","difficulty":"easy","question":"Space complexity of a recursive factorial(n)?","options":["O(n)","O(1)","O(n^2)","O(log n)"],"correct_answer":"O(n)","tags":["recursion"]},
  {"id":10,"section":"DSA","difficulty":"easy","question":"Result of 5 & 3 (bitwise AND)?","options":["1","7","5","3"],"correct_answer":"1","tags":["bit-manipulation"]},
  {"id":11,"section":"DSA","difficulty":"easy","question":"Height of a balanced binary tree with n nodes?","options":["O(log n)","O(n)","O(n^2)","O(1)"],"correct_answer":"O(log n)","tags":["trees"]},
  {"id":12,"section":"DSA","difficulty":"easy","question":"Which sort performs best on nearly-sorted data?","options":["Insertion Sort","Quick Sort","Heap Sort","Merge Sort"],"correct_answer":"Insertion Sort","tags":["sorting"]},
  {"id":13,"section":"DSA","difficulty":"easy","question":"Binary search on [1,3,5,7,9] for value 7 returns index?","options":["3","4","2","Not found"],"correct_answer":"3","tags":["binary-search"]},
  {"id":14,"section":"DSA","difficulty":"easy","question":"Average lookup time complexity of a hash map?","options":["O(1)","O(n)","O(log n)","O(n log n)"],"correct_answer":"O(1)","tags":["hashing"]},
  {"id":15,"section":"DSA","difficulty":"easy","question":"Kadane's algorithm solves?","options":["Maximum subarray sum","Shortest path","Binary search","Sorting"],"correct_answer":"Maximum subarray sum","tags":["arrays","dp"]},
  {"id":16,"section":"DSA","difficulty":"easy","question":"The two-pointer technique works best for?","options":["Sorted arrays and strings","Only trees","Only graphs","Only stacks"],"correct_answer":"Sorted arrays and strings","tags":["two-pointers"]},
  {"id":17,"section":"DSA","difficulty":"easy","question":"DFS uses which structure (implicit or explicit)?","options":["Stack","Queue","Heap","Array"],"correct_answer":"Stack","tags":["graphs","dfs"]},
  {"id":18,"section":"DSA","difficulty":"easy","question":"Which is NOT a linear data structure?","options":["Tree","Array","Queue","Stack"],"correct_answer":"Tree","tags":["data-structures"]},
  {"id":19,"section":"DSA","difficulty":"easy","question":"In a min-heap, the root element is always?","options":["The smallest element","The largest element","A middle element","A random element"],"correct_answer":"The smallest element","tags":["heap"]},
  {"id":20,"section":"DSA","difficulty":"easy","question":"Time complexity to merge two sorted arrays of size m and n?","options":["O(m+n)","O(m*n)","O(log(m+n))","O(max(m,n))"],"correct_answer":"O(m+n)","tags":["sorting"]},
  # MEDIUM
  {"id":21,"section":"DSA","difficulty":"medium","question":"Dijkstra's algorithm with a priority queue runs in?","options":["O((V+E) log V)","O(V^2)","O(E log E)","O(VE)"],"correct_answer":"O((V+E) log V)","tags":["graphs","dijkstra"]},
  {"id":22,"section":"DSA","difficulty":"medium","question":"Sliding window typically improves time from?","options":["O(n^2) to O(n)","O(n) to O(log n)","O(n^3) to O(n^2)","No improvement"],"correct_answer":"O(n^2) to O(n)","tags":["sliding-window"]},
  {"id":23,"section":"DSA","difficulty":"medium","question":"Floyd's cycle detection algorithm uses?","options":["Two pointers at different speeds","BFS","DFS","Recursion only"],"correct_answer":"Two pointers at different speeds","tags":["linked-list","cycle"]},
  {"id":24,"section":"DSA","difficulty":"medium","question":"LCA of nodes 4 and 6 in a BST with root 5 is?","options":["5","4","6","3"],"correct_answer":"5","tags":["trees","lca"]},
  {"id":25,"section":"DSA","difficulty":"medium","question":"0/1 Knapsack recurrence dp[i][w] = max(dp[i-1][w], ___)?","options":["val[i] + dp[i-1][w-wt[i]]","val[i] + dp[i][w-wt[i]]","dp[i-1][w] + val[i]","val[i] * dp[i-1][w]"],"correct_answer":"val[i] + dp[i-1][w-wt[i]]","tags":["dp","knapsack"]},
  {"id":26,"section":"DSA","difficulty":"medium","question":"Topological sort is valid only for?","options":["Directed Acyclic Graphs","Undirected graphs","Trees only","Complete graphs"],"correct_answer":"Directed Acyclic Graphs","tags":["graphs","topological-sort"]},
  {"id":27,"section":"DSA","difficulty":"medium","question":"Best structure for implementing LRU Cache?","options":["HashMap + Doubly Linked List","Array + Stack","Binary Tree","Trie"],"correct_answer":"HashMap + Doubly Linked List","tags":["design","lru"]},
  {"id":28,"section":"DSA","difficulty":"medium","question":"Quick sort worst-case time complexity?","options":["O(n^2)","O(n log n)","O(n)","O(log n)"],"correct_answer":"O(n^2)","tags":["sorting","quicksort"]},
  {"id":29,"section":"DSA","difficulty":"medium","question":"Monotonic stack pattern solves?","options":["Next Greater Element problems","Graph shortest paths","DP recurrences","Binary search problems"],"correct_answer":"Next Greater Element problems","tags":["stack","monotonic"]},
  {"id":30,"section":"DSA","difficulty":"medium","question":"Diameter of a binary tree is?","options":["Longest path between any two nodes","Height of the tree","Number of nodes","Depth of deepest leaf"],"correct_answer":"Longest path between any two nodes","tags":["trees"]},
  {"id":31,"section":"DSA","difficulty":"medium","question":"Which traversal visits root BETWEEN left and right subtrees?","options":["Inorder","Preorder","Postorder","Level order"],"correct_answer":"Inorder","tags":["trees","traversal"]},
  {"id":32,"section":"DSA","difficulty":"medium","question":"Bellman-Ford cannot handle?","options":["Negative weight cycles","Directed graphs","Undirected graphs","Sparse graphs"],"correct_answer":"Negative weight cycles","tags":["graphs","bellman-ford"]},
  {"id":33,"section":"DSA","difficulty":"medium","question":"Minimum coin change is correctly solved by?","options":["Dynamic Programming","Greedy always","BFS","Binary Search"],"correct_answer":"Dynamic Programming","tags":["dp","coin-change"]},
  {"id":34,"section":"DSA","difficulty":"medium","question":"A trie is most efficient for?","options":["Prefix-based string searches","Integer range queries","Graph traversal","Numerical sorting"],"correct_answer":"Prefix-based string searches","tags":["trie","strings"]},
  {"id":35,"section":"DSA","difficulty":"medium","question":"Minimum Spanning Tree algorithms include?","options":["Kruskal's and Prim's","Dijkstra's","Bellman-Ford","Floyd-Warshall"],"correct_answer":"Kruskal's and Prim's","tags":["graphs","mst"]},
  {"id":36,"section":"DSA","difficulty":"medium","question":"In-place linked list reversal needs how many extra pointers?","options":["3 (prev, curr, next)","1","0","n"],"correct_answer":"3 (prev, curr, next)","tags":["linked-list"]},
  {"id":37,"section":"DSA","difficulty":"medium","question":"merge_sort([3,1,4,1,5]) produces?","options":["[1,1,3,4,5]","[5,4,3,1,1]","[3,1,4,1,5]","[1,3,4,1,5]"],"correct_answer":"[1,1,3,4,5]","tags":["sorting"]},
  {"id":38,"section":"DSA","difficulty":"medium","question":"Bipartite graph check can be done using?","options":["BFS/DFS with 2-coloring","Dijkstra's","Topological sort","MST"],"correct_answer":"BFS/DFS with 2-coloring","tags":["graphs","bipartite"]},
  {"id":39,"section":"DSA","difficulty":"medium","question":"Space complexity of BFS on a graph with V vertices?","options":["O(V)","O(E)","O(V+E)","O(V^2)"],"correct_answer":"O(V)","tags":["graphs","bfs"]},
  {"id":40,"section":"DSA","difficulty":"medium","question":"Meet-in-the-middle reduces complexity from?","options":["O(2^n) to O(2^(n/2))","O(n^2) to O(n)","O(n) to O(log n)","O(n^3) to O(n^2)"],"correct_answer":"O(2^n) to O(2^(n/2))","tags":["optimization"]},
  # HARD
  {"id":41,"section":"DSA","difficulty":"hard","question":"LCS DP recurrence when characters match is dp[i][j] = ?","options":["dp[i-1][j-1] + 1","dp[i-1][j] + dp[i][j-1]","min(dp[i-1][j], dp[i][j-1]) + 1","dp[i][j-1]"],"correct_answer":"dp[i-1][j-1] + 1","tags":["dp","lcs"]},
  {"id":42,"section":"DSA","difficulty":"hard","question":"Tarjan's algorithm finds?","options":["Strongly Connected Components","Minimum Spanning Tree","Shortest Path","Bipartite components"],"correct_answer":"Strongly Connected Components","tags":["graphs","scc"]},
  {"id":43,"section":"DSA","difficulty":"hard","question":"A segment tree with n leaves has up to how many nodes?","options":["4n","n","n log n","2n - 1"],"correct_answer":"4n","tags":["segment-tree"]},
  {"id":44,"section":"DSA","difficulty":"hard","question":"Edit distance (Levenshtein) DP time complexity?","options":["O(m*n)","O(m+n)","O(m log n)","O(2^(m+n))"],"correct_answer":"O(m*n)","tags":["dp","edit-distance"]},
  {"id":45,"section":"DSA","difficulty":"hard","question":"Morris traversal achieves O(1) space inorder by?","options":["Temporarily modifying tree links","Using an implicit stack","Using parent pointers","Applying threading"],"correct_answer":"Temporarily modifying tree links","tags":["trees","morris"]},
  {"id":46,"section":"DSA","difficulty":"hard","question":"Burst Balloons DP time complexity?","options":["O(n^3)","O(n^2)","O(n log n)","O(2^n)"],"correct_answer":"O(n^3)","tags":["dp"]},
  {"id":47,"section":"DSA","difficulty":"hard","question":"Articulation points in a graph are found via?","options":["DFS with low[] and disc[] arrays","BFS","Dijkstra","Kruskal"],"correct_answer":"DFS with low[] and disc[] arrays","tags":["graphs","articulation-points"]},
  {"id":48,"section":"DSA","difficulty":"hard","question":"KMP failure function is used to?","options":["Skip redundant character comparisons","Sort strings","Build a trie","Hash strings efficiently"],"correct_answer":"Skip redundant character comparisons","tags":["strings","kmp"]},
  {"id":49,"section":"DSA","difficulty":"hard","question":"Persistent data structures support?","options":["Accessing any previous version after updates","Infinite memory allocation","Always faster queries","Distributed computation"],"correct_answer":"Accessing any previous version after updates","tags":["advanced"]},
  {"id":50,"section":"DSA","difficulty":"hard","question":"Largest Rectangle in Histogram optimal solution uses?","options":["Monotonic stack in O(n)","DP in O(n^2)","Divide and conquer O(n log n)","BFS in O(n)"],"correct_answer":"Monotonic stack in O(n)","tags":["stack","histogram"]},
]

CS_QUESTIONS = [
  {"id":101,"section":"CS Fundamentals","difficulty":"easy","question":"A process in an OS is?","options":["A program in execution","A program stored on disk","A network packet","A cache entry"],"correct_answer":"A program in execution","tags":["os"]},
  {"id":102,"section":"CS Fundamentals","difficulty":"easy","question":"A primary key must be?","options":["Unique and Not Null","Only Unique","Only Not Null","Auto-incremented"],"correct_answer":"Unique and Not Null","tags":["dbms"]},
  {"id":103,"section":"CS Fundamentals","difficulty":"easy","question":"HTTP stands for?","options":["HyperText Transfer Protocol","High Transfer Text Protocol","HyperText Transmission Program","Host Transfer Protocol"],"correct_answer":"HyperText Transfer Protocol","tags":["cn"]},
  {"id":104,"section":"CS Fundamentals","difficulty":"easy","question":"Encapsulation in OOP means?","options":["Bundling data and methods together","Inheriting from a parent class","Overriding methods","Creating multiple objects"],"correct_answer":"Bundling data and methods together","tags":["oop"]},
  {"id":105,"section":"CS Fundamentals","difficulty":"easy","question":"A foreign key?","options":["References the primary key of another table","Is a duplicate primary key","Must always be null","Is always indexed automatically"],"correct_answer":"References the primary key of another table","tags":["dbms"]},
  {"id":106,"section":"CS Fundamentals","difficulty":"easy","question":"TCP is a ___ protocol.","options":["Connection-oriented","Connectionless","Broadcast","Multicast"],"correct_answer":"Connection-oriented","tags":["cn"]},
  {"id":107,"section":"CS Fundamentals","difficulty":"easy","question":"Deadlock in OS occurs when?","options":["Two or more processes wait for each other indefinitely","A process crashes suddenly","Memory is exhausted","CPU is overloaded"],"correct_answer":"Two or more processes wait for each other indefinitely","tags":["os"]},
  {"id":108,"section":"CS Fundamentals","difficulty":"easy","question":"SQL SELECT DISTINCT returns?","options":["Only unique rows","All rows including duplicates","Only duplicate rows","Sorted rows"],"correct_answer":"Only unique rows","tags":["dbms"]},
  {"id":109,"section":"CS Fundamentals","difficulty":"easy","question":"IP protocol operates at which OSI layer?","options":["Network layer","Transport layer","Application layer","Data link layer"],"correct_answer":"Network layer","tags":["cn"]},
  {"id":110,"section":"CS Fundamentals","difficulty":"easy","question":"Polymorphism in OOP means?","options":["Same interface, multiple implementations","Only method overloading","Only method overriding","Hiding internal state"],"correct_answer":"Same interface, multiple implementations","tags":["oop"]},
  {"id":111,"section":"CS Fundamentals","difficulty":"easy","question":"Virtual memory is?","options":["Disk space used as RAM extension","GPU memory","Cache memory","ROM"],"correct_answer":"Disk space used as RAM extension","tags":["os"]},
  {"id":112,"section":"CS Fundamentals","difficulty":"easy","question":"Database normalization aims to?","options":["Reduce data redundancy","Encrypt stored data","Create indexes automatically","Back up data"],"correct_answer":"Reduce data redundancy","tags":["dbms"]},
  {"id":113,"section":"CS Fundamentals","difficulty":"medium","question":"Which CPU scheduling can cause starvation?","options":["Priority Scheduling","Round Robin","FCFS","SJF with equal priorities"],"correct_answer":"Priority Scheduling","tags":["os"]},
  {"id":114,"section":"CS Fundamentals","difficulty":"medium","question":"ACID stands for?","options":["Atomicity, Consistency, Isolation, Durability","Accuracy, Consistency, Integrity, Data","Atomicity, Concurrency, Isolation, Durability","All Complete Integrated Data"],"correct_answer":"Atomicity, Consistency, Isolation, Durability","tags":["dbms"]},
  {"id":115,"section":"CS Fundamentals","difficulty":"medium","question":"End-to-end communication in OSI is handled by which layer?","options":["Transport layer","Network layer","Session layer","Application layer"],"correct_answer":"Transport layer","tags":["cn"]},
  {"id":116,"section":"CS Fundamentals","difficulty":"medium","question":"Key difference between thread and process?","options":["Threads share memory; processes have separate memory","Threads are heavier than processes","Processes share memory; threads do not","No real difference"],"correct_answer":"Threads share memory; processes have separate memory","tags":["os"]},
  {"id":117,"section":"CS Fundamentals","difficulty":"medium","question":"In a B+ Tree, all data is stored in?","options":["Leaf nodes only","Root only","Internal nodes only","Random nodes"],"correct_answer":"Leaf nodes only","tags":["dbms"]},
  {"id":118,"section":"CS Fundamentals","difficulty":"medium","question":"DNS resolves?","options":["Domain names to IP addresses","IP to MAC addresses","HTTP to HTTPS","URLs to file paths"],"correct_answer":"Domain names to IP addresses","tags":["cn"]},
  {"id":119,"section":"CS Fundamentals","difficulty":"medium","question":"A race condition occurs when?","options":["Outcome depends on non-deterministic event timing","Two processes compete for CPU cycles","Fast CPU outperforms slow memory","Network congestion spikes"],"correct_answer":"Outcome depends on non-deterministic event timing","tags":["os"]},
  {"id":120,"section":"CS Fundamentals","difficulty":"medium","question":"3NF eliminates?","options":["Transitive dependencies on primary key","Partial dependencies","Multivalued dependencies","Non-atomic attributes"],"correct_answer":"Transitive dependencies on primary key","tags":["dbms"]},
  {"id":121,"section":"CS Fundamentals","difficulty":"medium","question":"TCP Three-Way Handshake is used to?","options":["Establish a reliable connection","Terminate a connection","Transfer bulk data","Encrypt packets"],"correct_answer":"Establish a reliable connection","tags":["cn"]},
  {"id":122,"section":"CS Fundamentals","difficulty":"medium","question":"Liskov Substitution Principle (LSP) states?","options":["Subclass objects should substitute for superclass objects","Classes should have one reason to change","Depend on abstractions not concretions","Program to interface not implementation"],"correct_answer":"Subclass objects should substitute for superclass objects","tags":["oop"]},
  {"id":123,"section":"CS Fundamentals","difficulty":"medium","question":"A mutex can only be released by?","options":["The thread that acquired it","Any thread in the process","The OS scheduler","Always the main thread"],"correct_answer":"The thread that acquired it","tags":["os"]},
  {"id":124,"section":"CS Fundamentals","difficulty":"medium","question":"A database index is?","options":["A structure that speeds up queries","A table backup","A foreign key constraint","A schema version"],"correct_answer":"A structure that speeds up queries","tags":["dbms"]},
  {"id":125,"section":"CS Fundamentals","difficulty":"hard","question":"Optimistic locking differs from pessimistic by?","options":["Checking for conflict only at commit, not locking upfront","Locking the resource immediately","Being used only in NoSQL","Being identical in practice"],"correct_answer":"Checking for conflict only at commit, not locking upfront","tags":["dbms"]},
  {"id":126,"section":"CS Fundamentals","difficulty":"hard","question":"A system call is triggered when?","options":["User program requests OS service (e.g., I/O)","Hardware interrupt fires","Timer tick occurs","Page fault occurs only"],"correct_answer":"User program requests OS service (e.g., I/O)","tags":["os"]},
  {"id":127,"section":"CS Fundamentals","difficulty":"hard","question":"TCP slow start is triggered by?","options":["Connection start or packet loss","Every ACK received","Full receive buffer","Timeout only"],"correct_answer":"Connection start or packet loss","tags":["cn"]},
  {"id":128,"section":"CS Fundamentals","difficulty":"hard","question":"CAP theorem: a distributed system can guarantee at most 2 of?","options":["Consistency, Availability, Partition tolerance","Cache, API, Performance","Correctness, Atomicity, Persistence","Speed, Safety, Scalability"],"correct_answer":"Consistency, Availability, Partition tolerance","tags":["distributed"]},
  {"id":129,"section":"CS Fundamentals","difficulty":"hard","question":"Write-Ahead Logging (WAL) ensures?","options":["Changes are logged before applied for crash recovery","Faster reads via caching","Automatic horizontal sharding","Schema migration safety"],"correct_answer":"Changes are logged before applied for crash recovery","tags":["dbms"]},
  {"id":130,"section":"CS Fundamentals","difficulty":"hard","question":"Horizontal scaling means?","options":["Adding more machines to a pool","Upgrading CPU/RAM of one machine","Increasing disk I/O speed","Reducing network latency"],"correct_answer":"Adding more machines to a pool","tags":["system"]},
]

SD_QUESTIONS = [
  {"id":201,"section":"System Design","difficulty":"easy","question":"A load balancer primarily?","options":["Distributes traffic across multiple servers","Stores cached data","Acts as a DB proxy","Serves as a CDN node"],"correct_answer":"Distributes traffic across multiple servers","tags":["load-balancing"]},
  {"id":202,"section":"System Design","difficulty":"easy","question":"CDN stands for?","options":["Content Delivery Network","Central Data Node","Core Distribution Network","Cache Data Network"],"correct_answer":"Content Delivery Network","tags":["cdn"]},
  {"id":203,"section":"System Design","difficulty":"easy","question":"Caching reduces?","options":["Latency by serving frequent data faster","Data encryption cost","Load balancer overhead","Schema complexity"],"correct_answer":"Latency by serving frequent data faster","tags":["caching"]},
  {"id":204,"section":"System Design","difficulty":"easy","question":"A REST API is?","options":["Stateless HTTP API using standard methods","A proprietary database protocol","A caching system","A message broker"],"correct_answer":"Stateless HTTP API using standard methods","tags":["api"]},
  {"id":205,"section":"System Design","difficulty":"easy","question":"SQL databases are characterized by?","options":["Relational model with fixed schema","Schema-less flexible structure","Horizontal scaling by default","Only for small datasets"],"correct_answer":"Relational model with fixed schema","tags":["databases"]},
  {"id":206,"section":"System Design","difficulty":"easy","question":"Vertical scaling means?","options":["More CPU/RAM on existing server","Adding more servers to pool","More database replicas","Geographic distribution"],"correct_answer":"More CPU/RAM on existing server","tags":["scaling"]},
  {"id":207,"section":"System Design","difficulty":"easy","question":"A message queue enables?","options":["Async communication between services","Synchronous API calls","Caching API responses","Real-time load balancing"],"correct_answer":"Async communication between services","tags":["message-queue"]},
  {"id":208,"section":"System Design","difficulty":"easy","question":"An API Gateway provides?","options":["Single entry point routing to backend services","DB abstraction layer","Cache tier only","Static load balancer"],"correct_answer":"Single entry point routing to backend services","tags":["api-gateway"]},
  {"id":209,"section":"System Design","difficulty":"easy","question":"HTTPS provides over HTTP?","options":["Encrypted communication via TLS","Faster transfer","Compression","Auto load balancing"],"correct_answer":"Encrypted communication via TLS","tags":["security"]},
  {"id":210,"section":"System Design","difficulty":"easy","question":"Database sharding means?","options":["Splitting data across multiple DB instances","Copying data to replicas","Caching query results","Creating secondary indexes"],"correct_answer":"Splitting data across multiple DB instances","tags":["databases"]},
  {"id":211,"section":"System Design","difficulty":"medium","question":"Write-through caching writes data to?","options":["Cache and DB simultaneously","Cache only, flushed later","DB first, then cache","Only on cache miss"],"correct_answer":"Cache and DB simultaneously","tags":["caching"]},
  {"id":212,"section":"System Design","difficulty":"medium","question":"Best data store for a URL shortener's redirect mapping?","options":["Key-value NoSQL (Redis/DynamoDB)","Relational SQL with JOINs","In-memory array","File system"],"correct_answer":"Key-value NoSQL (Redis/DynamoDB)","tags":["system-design"]},
  {"id":213,"section":"System Design","difficulty":"medium","question":"Consistent hashing is used for?","options":["Distributing load with minimal remapping when nodes change","Encrypting distributed data","Sorting distributed keys","Normalizing schemas"],"correct_answer":"Distributing load with minimal remapping when nodes change","tags":["distributed"]},
  {"id":214,"section":"System Design","difficulty":"medium","question":"Synchronous communication means?","options":["Caller waits for response before proceeding","Caller never waits","Always faster","Less reliable"],"correct_answer":"Caller waits for response before proceeding","tags":["communication"]},
  {"id":215,"section":"System Design","difficulty":"medium","question":"Circuit breaker pattern prevents?","options":["Cascading failures when a service is down","DB connection pool exhaustion","API rate limit violations","Load balancer misconfiguration"],"correct_answer":"Cascading failures when a service is down","tags":["microservices"]},
  {"id":216,"section":"System Design","difficulty":"medium","question":"Primary advantage of event-driven architecture?","options":["Loose coupling between services","Always faster responses","Simpler code","Zero message loss"],"correct_answer":"Loose coupling between services","tags":["architecture"]},
  {"id":217,"section":"System Design","difficulty":"medium","question":"For Twitter-scale tweet storage, best choice?","options":["NoSQL (Cassandra) for write-heavy scale","Normalized SQL only","In-memory only","File system with index"],"correct_answer":"NoSQL (Cassandra) for write-heavy scale","tags":["databases"]},
  {"id":218,"section":"System Design","difficulty":"medium","question":"Database replication serves to?","options":["Improve availability and read scalability","Horizontally partition data","Cache query results","Normalize tables"],"correct_answer":"Improve availability and read scalability","tags":["databases"]},
  {"id":219,"section":"System Design","difficulty":"medium","question":"Heartbeat signals in distributed systems are used for?","options":["Detecting node failures quickly","Encrypting communication","Routing requests","Caching sessions"],"correct_answer":"Detecting node failures quickly","tags":["distributed"]},
  {"id":220,"section":"System Design","difficulty":"medium","question":"Rate limiting is implemented to?","options":["Prevent abuse and protect from overload","Speed up responses","Encrypt traffic","Balance load"],"correct_answer":"Prevent abuse and protect from overload","tags":["api"]},
  {"id":221,"section":"System Design","difficulty":"hard","question":"For 1B user notifications, the core bottleneck is?","options":["Fan-out: write-time vs read-time tradeoff","Database engine choice","REST API design","Frontend rendering"],"correct_answer":"Fan-out: write-time vs read-time tradeoff","tags":["system-design"]},
  {"id":222,"section":"System Design","difficulty":"hard","question":"Eventual consistency guarantees?","options":["All nodes converge to same state eventually","Immediate consistency","Zero data loss always","Full ACID compliance"],"correct_answer":"All nodes converge to same state eventually","tags":["distributed"]},
  {"id":223,"section":"System Design","difficulty":"hard","question":"Two-phase commit (2PC) is used for?","options":["Atomic transactions across distributed nodes","Caching strategies","Load balancing","API versioning"],"correct_answer":"Atomic transactions across distributed nodes","tags":["distributed"]},
  {"id":224,"section":"System Design","difficulty":"hard","question":"Core challenge in a ride-sharing system?","options":["Geospatial indexing and low-latency driver matching","Database selection","Payment processing","Authentication flow"],"correct_answer":"Geospatial indexing and low-latency driver matching","tags":["system-design"]},
  {"id":225,"section":"System Design","difficulty":"hard","question":"A Bloom filter provides?","options":["Probabilistic membership testing with no false negatives","Exact duplicate detection","Distributed sorting","Consistent indexing"],"correct_answer":"Probabilistic membership testing with no false negatives","tags":["bloom-filter"]},
  {"id":226,"section":"System Design","difficulty":"hard","question":"Redis Cluster default sharding uses?","options":["Hash slot-based consistent hashing (16384 slots)","Range-based partitioning","Random distribution","Round-robin assignment"],"correct_answer":"Hash slot-based consistent hashing (16384 slots)","tags":["redis","caching"]},
  {"id":227,"section":"System Design","difficulty":"hard","question":"Leader election in distributed systems uses?","options":["Consensus algorithms (Raft or Paxos)","Simple majority voting","Database record locking","Heartbeat detection alone"],"correct_answer":"Consensus algorithms (Raft or Paxos)","tags":["distributed"]},
  {"id":228,"section":"System Design","difficulty":"hard","question":"Biggest challenge for a YouTube-like platform?","options":["Video encoding pipeline, petabyte storage, CDN distribution","User authentication","Comment system","Full-text search"],"correct_answer":"Video encoding pipeline, petabyte storage, CDN distribution","tags":["system-design"]},
  {"id":229,"section":"System Design","difficulty":"hard","question":"Saga pattern manages?","options":["Distributed transactions via local txns + compensating events","Application monitoring","Blue-green deployment","API gateway routing"],"correct_answer":"Distributed transactions via local txns + compensating events","tags":["microservices"]},
  {"id":230,"section":"System Design","difficulty":"hard","question":"Write-back caching risks?","options":["Data loss if cache crashes before flushing to DB","Slower writes","Higher cache miss rates","Increased read latency"],"correct_answer":"Data loss if cache crashes before flushing to DB","tags":["caching"]},
]

ALL_QUESTIONS = DSA_QUESTIONS + CS_QUESTIONS + SD_QUESTIONS


# ─────────────────────────────────────────────────────────────────
#  LEARNING CONTENT  —  total = len(problems) always
# ─────────────────────────────────────────────────────────────────
def p(name, lc="", blog=""):
    return {"name": name, "leetcode": lc, "blog": blog, "done": False}

LEARNING_CONTENT = {
  "DSA": [
    {"id":"dsa-1","title":"Learn the Basics","problems":[
      p("Time and Space Complexity", blog=f"{GFG}/time-complexity-and-space-complexity/"),
      p("Recursion Basics", blog=f"{GFG}/introduction-to-recursion-data-structure-and-algorithm-tutorials/"),
      p("Pattern Problems", f"{LC}/print-words-vertically/", f"{GFG}/pattern-printing-gfg/"),
      p("Math: Palindrome and Digits", f"{LC}/palindrome-number/", f"{GFG}/program-for-nth-fibonacci-number/"),
      p("Math: GCD, LCM, Primes", f"{LC}/count-primes/", f"{GFG}/c-program-find-gcd-hcf-two-numbers/"),
      p("Recursion on Arrays", f"{LC}/power-of-two/", f"{GFG}/recursive-programs-to-find-minimum-maximum-elements-of-array/"),
      p("Hashing Basics", f"{LC}/two-sum/", f"{GFG}/hashing-data-structure/"),
      p("Java / C++ / Python STL Basics", blog="https://takeuforward.org/strivers-a2z-dsa-course/"),
    ]},
    {"id":"dsa-2","title":"Sorting Techniques","problems":[
      p("Selection Sort", blog=f"{GFG}/selection-sort/"),
      p("Bubble Sort", blog=f"{GFG}/bubble-sort/"),
      p("Insertion Sort", blog=f"{GFG}/insertion-sort/"),
      p("Merge Sort", f"{LC}/sort-an-array/", f"{GFG}/merge-sort/"),
      p("Quick Sort", f"{LC}/sort-an-array/", f"{GFG}/quick-sort/"),
      p("Recursive Bubble and Insertion Sort", blog=f"{GFG}/recursive-bubble-sort/"),
      p("Count Inversions", f"{LC}/count-of-smaller-numbers-after-self/", f"{GFG}/counting-inversions/"),
    ]},
    {"id":"dsa-3","title":"Arrays","problems":[
      p("Largest Element in Array", f"{LC}/find-the-maximum-achievable-number/", f"{GFG}/largest-element-in-an-array-using-stl/"),
      p("Second Largest Element", blog=f"{GFG}/find-second-largest-element-in-array/"),
      p("Check if Array is Sorted", f"{LC}/check-if-array-is-sorted-and-rotated/"),
      p("Remove Duplicates from Sorted Array", f"{LC}/remove-duplicates-from-sorted-array/"),
      p("Rotate Array by K", f"{LC}/rotate-array/"),
      p("Move Zeros to End", f"{LC}/move-zeroes/"),
      p("Union of Two Sorted Arrays", blog=f"{GFG}/union-and-intersection-of-two-sorted-arrays-2/"),
      p("Missing Number", f"{LC}/missing-number/"),
      p("Max Consecutive Ones", f"{LC}/max-consecutive-ones/"),
      p("Single Number (XOR)", f"{LC}/single-number/"),
      p("Two Sum", f"{LC}/two-sum/"),
      p("Sort 0s 1s 2s - Dutch National Flag", f"{LC}/sort-colors/"),
      p("Majority Element (Boyer-Moore)", f"{LC}/majority-element/"),
      p("Maximum Subarray - Kadane's", f"{LC}/maximum-subarray/"),
      p("Best Time to Buy and Sell Stock", f"{LC}/best-time-to-buy-and-sell-stock/"),
      p("Leaders in an Array", blog=f"{GFG}/leaders-in-an-array/"),
      p("Next Permutation", f"{LC}/next-permutation/"),
      p("Longest Consecutive Sequence", f"{LC}/longest-consecutive-sequence/"),
      p("Set Matrix Zeroes", f"{LC}/set-matrix-zeroes/"),
      p("Rearrange Elements by Sign", f"{LC}/rearrange-array-elements-by-sign/"),
    ]},
    {"id":"dsa-4","title":"Binary Search","problems":[
      p("Binary Search Basics", f"{LC}/binary-search/"),
      p("Lower and Upper Bound", f"{LC}/find-first-and-last-position-of-element-in-sorted-array/"),
      p("Search in Rotated Sorted Array", f"{LC}/search-in-rotated-sorted-array/"),
      p("Find Peak Element", f"{LC}/find-peak-element/"),
      p("Square Root via Binary Search", f"{LC}/sqrtx/"),
      p("Find Minimum in Rotated Array", f"{LC}/find-minimum-in-rotated-sorted-array/"),
      p("Koko Eating Bananas", f"{LC}/koko-eating-bananas/"),
      p("Capacity to Ship Packages", f"{LC}/capacity-to-ship-packages-within-d-days/"),
    ]},
    {"id":"dsa-5","title":"Strings","problems":[
      p("Reverse Words in a String", f"{LC}/reverse-words-in-a-string/"),
      p("Longest Palindromic Substring", f"{LC}/longest-palindromic-substring/"),
      p("Roman to Integer", f"{LC}/roman-to-integer/"),
      p("Valid Anagram", f"{LC}/valid-anagram/"),
      p("Count and Say", f"{LC}/count-and-say/"),
      p("Implement strStr - KMP", f"{LC}/find-the-index-of-the-first-occurrence-in-a-string/", f"{GFG}/kmp-algorithm-for-pattern-searching/"),
      p("String to Integer atoi", f"{LC}/string-to-integer-atoi/"),
    ]},
    {"id":"dsa-6","title":"Linked List","problems":[
      p("Reverse a Linked List", f"{LC}/reverse-linked-list/"),
      p("Middle of Linked List", f"{LC}/middle-of-the-linked-list/"),
      p("Merge Two Sorted Lists", f"{LC}/merge-two-sorted-lists/"),
      p("Detect Cycle - Floyd's Algorithm", f"{LC}/linked-list-cycle/", f"{GFG}/detect-loop-in-a-linked-list/"),
      p("Remove Nth Node from End", f"{LC}/remove-nth-node-from-end-of-list/"),
      p("Add Two Numbers", f"{LC}/add-two-numbers/"),
      p("Copy List with Random Pointer", f"{LC}/copy-list-with-random-pointer/"),
    ]},
    {"id":"dsa-7","title":"Recursion and Backtracking","problems":[
      p("Combination Sum", f"{LC}/combination-sum/"),
      p("Subsets - Power Set", f"{LC}/subsets/"),
      p("Permutations", f"{LC}/permutations/"),
      p("N-Queens", f"{LC}/n-queens/"),
      p("Sudoku Solver", f"{LC}/sudoku-solver/"),
      p("Word Search", f"{LC}/word-search/"),
    ]},
    {"id":"dsa-8","title":"Bit Manipulation","problems":[
      p("Check if a Bit is Set", blog=f"{GFG}/check-whether-k-th-bit-set-or-not/"),
      p("Set and Unset a Bit", blog=f"{GFG}/set-unset-bit/"),
      p("Power of 2 Check", f"{LC}/power-of-two/", f"{GFG}/program-to-find-whether-a-no-is-power-of-two/"),
      p("Count Set Bits - Hamming Weight", f"{LC}/number-of-1-bits/"),
      p("Single Number via XOR", f"{LC}/single-number/"),
      p("XOR of Numbers in a Range", blog=f"{GFG}/find-xor-of-all-elements-in-an-array/"),
    ]},
    {"id":"dsa-9","title":"Stack and Queue","problems":[
      p("Valid Parentheses", f"{LC}/valid-parentheses/"),
      p("Min Stack", f"{LC}/min-stack/"),
      p("Next Greater Element", f"{LC}/next-greater-element-i/"),
      p("Largest Rectangle in Histogram", f"{LC}/largest-rectangle-in-histogram/"),
      p("Sliding Window Maximum", f"{LC}/sliding-window-maximum/"),
      p("Implement Queue using Stacks", f"{LC}/implement-queue-using-stacks/"),
    ]},
    {"id":"dsa-10","title":"Trees - Binary and BST","problems":[
      p("Inorder, Preorder, Postorder Traversal", f"{LC}/binary-tree-inorder-traversal/"),
      p("Height of Binary Tree", f"{LC}/maximum-depth-of-binary-tree/"),
      p("Diameter of Binary Tree", f"{LC}/diameter-of-binary-tree/"),
      p("Check Balanced Binary Tree", f"{LC}/balanced-binary-tree/"),
      p("Same Tree", f"{LC}/same-tree/"),
      p("Invert Binary Tree", f"{LC}/invert-binary-tree/"),
      p("LCA of Binary Tree", f"{LC}/lowest-common-ancestor-of-a-binary-tree/"),
      p("Zigzag Level Order Traversal", f"{LC}/binary-tree-zigzag-level-order-traversal/"),
      p("Binary Tree Maximum Path Sum", f"{LC}/binary-tree-maximum-path-sum/"),
      p("Construct Tree from Inorder and Preorder", f"{LC}/construct-binary-tree-from-preorder-and-inorder-traversal/"),
    ]},
    {"id":"dsa-11","title":"Graphs","problems":[
      p("BFS of Graph", f"{LC}/number-of-islands/", f"{GFG}/breadth-first-search-or-bfs-for-a-graph/"),
      p("DFS of Graph", f"{LC}/number-of-islands/", f"{GFG}/depth-first-search-or-dfs-for-a-graph/"),
      p("Cycle Detection in Undirected Graph", f"{LC}/course-schedule/", f"{GFG}/detect-cycle-undirected-graph/"),
      p("Topological Sort - Kahn and DFS", f"{LC}/course-schedule-ii/", f"{GFG}/topological-sorting/"),
      p("Dijkstra's Shortest Path", f"{LC}/network-delay-time/", f"{GFG}/dijkstras-shortest-path-algorithm-greedy-algo-7/"),
      p("Bellman-Ford Algorithm", f"{LC}/cheapest-flights-within-k-stops/", f"{GFG}/bellman-ford-algorithm-dp-23/"),
      p("Floyd Warshall All-Pairs Shortest Path", f"{LC}/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance/", f"{GFG}/floyd-warshall-algorithm-dp-16/"),
      p("Kruskal's MST with Union-Find", f"{LC}/min-cost-to-connect-all-points/", f"{GFG}/kruskals-minimum-spanning-tree-algorithm-greedy-algo-2/"),
    ]},
    {"id":"dsa-12","title":"Dynamic Programming","problems":[
      p("Fibonacci - Memoization and Tabulation", f"{LC}/fibonacci-number/", f"{GFG}/program-for-nth-fibonacci-number/"),
      p("Climbing Stairs", f"{LC}/climbing-stairs/"),
      p("0 or 1 Knapsack", blog=f"{GFG}/0-1-knapsack-problem-dp-10/"),
      p("Longest Common Subsequence", f"{LC}/longest-common-subsequence/"),
      p("Longest Increasing Subsequence", f"{LC}/longest-increasing-subsequence/"),
      p("Coin Change - Minimum Coins", f"{LC}/coin-change/"),
      p("Edit Distance", f"{LC}/edit-distance/"),
      p("House Robber", f"{LC}/house-robber/"),
      p("Partition Equal Subset Sum", f"{LC}/partition-equal-subset-sum/"),
      p("Matrix Chain Multiplication", blog=f"{GFG}/matrix-chain-multiplication-dp-8/"),
    ]},
    {"id":"dsa-13","title":"Greedy Algorithms","problems":[
      p("Activity Selection and Non-Overlapping Intervals", f"{LC}/non-overlapping-intervals/", f"{GFG}/activity-selection-problem-greedy-algo-1/"),
      p("Fractional Knapsack", blog=f"{GFG}/fractional-knapsack-problem/"),
      p("Job Sequencing with Deadlines", blog=f"{GFG}/job-sequencing-problem/"),
      p("Minimum Platforms Required", blog=f"{GFG}/minimum-number-platforms-required-railwaybus-station/"),
      p("Jump Game", f"{LC}/jump-game/"),
    ]},
    {"id":"dsa-14","title":"Tries","problems":[
      p("Implement Trie - Insert, Search, StartsWith", f"{LC}/implement-trie-prefix-tree/"),
      p("Longest Common Prefix", f"{LC}/longest-common-prefix/", f"{GFG}/longest-common-prefix-using-trie/"),
      p("Maximum XOR of Two Numbers", f"{LC}/maximum-xor-of-two-numbers-in-an-array/"),
      p("Word Search II - Trie and Backtracking", f"{LC}/word-search-ii/"),
    ]},
    {"id":"dsa-15","title":"Heaps and Priority Queue","problems":[
      p("Kth Largest Element in Array", f"{LC}/kth-largest-element-in-an-array/"),
      p("Top K Frequent Elements", f"{LC}/top-k-frequent-elements/"),
      p("Merge K Sorted Lists", f"{LC}/merge-k-sorted-lists/"),
      p("Find Median from Data Stream", f"{LC}/find-median-from-data-stream/"),
    ]},
  ],
  "CS Fundamentals": [
    {"id":"cs-1","title":"Operating Systems","problems":[
      p("Process vs Thread", blog=f"{GFG}/difference-between-process-and-thread/"),
      p("CPU Scheduling Algorithms", blog=f"{GFG}/cpu-scheduling-in-operating-systems/"),
      p("Deadlock Conditions and Prevention", blog=f"{GFG}/introduction-of-deadlock-in-operating-system/"),
      p("Semaphore vs Mutex", blog=f"{GFG}/semaphores-in-operating-system/"),
      p("Virtual Memory and Paging", blog=f"{GFG}/virtual-memory-in-operating-system/"),
      p("Page Replacement Algorithms LRU FIFO Optimal", blog=f"{GFG}/page-replacement-algorithms-in-operating-systems/"),
      p("Inter-Process Communication IPC", blog=f"{GFG}/inter-process-communication-ipc/"),
      p("System Calls", blog=f"{GFG}/introduction-of-system-call/"),
    ]},
    {"id":"cs-2","title":"Database Management Systems","problems":[
      p("ER Diagrams and Schema Design", blog=f"{GFG}/introduction-of-er-model/"),
      p("SQL - SELECT JOIN GROUP BY", f"{LC}/combine-two-tables/", f"{GFG}/sql-join-set-1-inner-left-right-and-full-joins/"),
      p("Normalization 1NF 2NF 3NF BCNF", blog=f"{GFG}/normal-forms-in-dbms/"),
      p("ACID Properties", blog=f"{GFG}/acid-properties-in-dbms/"),
      p("Indexing B-Tree and Hash", blog=f"{GFG}/indexing-in-databases-set-1/"),
      p("Transactions and Isolation Levels", blog=f"{GFG}/transaction-isolation-levels-dbms/"),
      p("SQL Aggregate Functions", f"{LC}/department-highest-salary/"),
      p("NoSQL vs SQL Decision Guide", blog=f"{GFG}/difference-between-sql-and-nosql/"),
    ]},
    {"id":"cs-3","title":"Computer Networks","problems":[
      p("OSI Model 7 Layers", blog=f"{GFG}/layers-of-osi-model/"),
      p("TCP vs UDP", blog=f"{GFG}/differences-between-tcp-and-udp/"),
      p("HTTP and HTTPS Methods and Status Codes", blog=f"{GFG}/http-full-form/"),
      p("DNS Resolution Process", blog=f"{GFG}/domain-name-system-dns-in-application-layer/"),
      p("IP Addressing and Subnetting", blog=f"{GFG}/introduction-classful-ip-addressing/"),
      p("Routing Protocols RIP OSPF BGP", blog=f"{GFG}/routing-protocols-set-2-distance-vector-routing/"),
      p("Sockets and Port Numbers", blog=f"{GFG}/socket-programming-cc/"),
    ]},
    {"id":"cs-4","title":"OOP and Design Concepts","problems":[
      p("4 Pillars of OOP", blog=f"{GFG}/object-oriented-programming-oops-concept-in-java/"),
      p("SOLID Principles", blog=f"{GFG}/solid-principle-in-programming-understand-with-real-life-examples/"),
      p("Design Patterns Overview", blog=f"{GFG}/software-design-patterns/"),
      p("Composition vs Inheritance", blog=f"{GFG}/favoring-composition-over-inheritance-in-java-with-examples/"),
      p("Abstract Class vs Interface", blog=f"{GFG}/difference-between-abstract-class-and-interface-in-java/"),
    ]},
  ],
  "System Design": [
    {"id":"sd-1","title":"System Design Fundamentals","problems":[
      p("Scalability Vertical vs Horizontal", blog=f"{GFG}/system-design-horizontal-and-vertical-scaling/"),
      p("Load Balancing Algorithms", blog=f"{GFG}/load-balancing-algorithms/"),
      p("CAP Theorem", blog=f"{GFG}/the-cap-theorem-in-dbms/"),
      p("Latency vs Throughput", blog="https://systemdesign.one/latency-vs-throughput/"),
      p("Availability and SLA SLO SLI", blog="https://sre.google/sre-book/service-level-objectives/"),
    ]},
    {"id":"sd-2","title":"Database and Storage Design","problems":[
      p("SQL vs NoSQL Decision Guide", blog=f"{GFG}/difference-between-sql-and-nosql/"),
      p("Database Sharding Strategies", blog=f"{GFG}/database-sharding/"),
      p("Database Replication Primary and Replica", blog="https://architecturenotes.co/database-sharding-explained/"),
      p("Consistent Hashing", blog=f"{GFG}/consistent-hashing/"),
    ]},
    {"id":"sd-3","title":"Caching Strategies","problems":[
      p("Cache Aside Write-Through Write-Back Patterns", blog=f"{GFG}/caching-strategies/"),
      p("Redis vs Memcached", blog="https://aws.amazon.com/elasticache/redis-vs-memcached/"),
      p("Cache Invalidation TTL and Event-Based", blog="https://codeahoy.com/2017/08/11/caching-strategies-and-how-to-choose-the-right-one/"),
      p("CDN and Edge Caching", blog=f"{GFG}/content-delivery-network-cdn/"),
    ]},
    {"id":"sd-4","title":"Message Queues and Async","problems":[
      p("Kafka vs RabbitMQ", blog=f"{GFG}/kafka-vs-rabbitmq/"),
      p("Event-Driven Architecture", blog="https://aws.amazon.com/event-driven-architecture/"),
      p("Dead Letter Queues DLQ", blog="https://www.cloudamqp.com/blog/when-and-how-to-use-the-rabbitmq-dead-letter-exchange.html"),
    ]},
    {"id":"sd-5","title":"Microservices and APIs","problems":[
      p("Monolith vs Microservices", blog=f"{GFG}/monolithic-vs-microservices-architecture/"),
      p("API Gateway Pattern", blog="https://microservices.io/patterns/apigateway.html"),
      p("Service Discovery", blog="https://microservices.io/patterns/client-side-discovery.html"),
      p("Circuit Breaker Pattern", blog="https://martinfowler.com/bliki/CircuitBreaker.html"),
      p("Saga Pattern for Distributed Transactions", blog="https://microservices.io/patterns/data/saga.html"),
    ]},
    {"id":"sd-6","title":"Real-World Case Studies","problems":[
      p("Design URL Shortener TinyURL", blog=f"{GFG}/system-design-url-shortening-service/"),
      p("Design Twitter News Feed", blog=f"{GFG}/design-twitter-a-system-design-interview-question/"),
      p("Design Uber Ride Sharing", blog="https://highscalability.com/uber-architecture-and-system-design/"),
      p("Design YouTube Video Platform", blog=f"{GFG}/design-video-sharing-system-like-youtube/"),
      p("Design WhatsApp Chat System", blog="https://highscalability.com/whatsapp-architecture-facebook-bought-for-19-billion/"),
      p("Design Google Drive Cloud Storage", blog=f"{GFG}/design-dropbox-a-system-design-interview-question/"),
    ]},
  ]
}

# Set total = actual number of problems listed
for section_topics in LEARNING_CONTENT.values():
    for topic in section_topics:
        topic["total"] = len(topic["problems"])


def main():
    os.makedirs(DATA_DIR, exist_ok=True)

    q_path = os.path.join(DATA_DIR, "questions.json")
    with open(q_path, "w") as f:
        json.dump(ALL_QUESTIONS, f, indent=2)
    print(f"Generated {len(ALL_QUESTIONS)} questions -> {q_path}")

    lc_path = os.path.join(DATA_DIR, "learning_content.json")
    with open(lc_path, "w") as f:
        json.dump(LEARNING_CONTENT, f, indent=2)

    total_topics = sum(len(v) for v in LEARNING_CONTENT.values())
    total_probs  = sum(len(t["problems"]) for v in LEARNING_CONTENT.values() for t in v)
    no_link = [(sec, t["title"], pr["name"])
               for sec, topics in LEARNING_CONTENT.items()
               for t in topics
               for pr in t["problems"]
               if not pr.get("leetcode") and not pr.get("blog")]

    print(f"Generated {total_topics} topic groups, {total_probs} problems -> {lc_path}")
    if no_link:
        print(f"WARNING: {len(no_link)} problems still have no links!")
        for x in no_link:
            print(f"  {x}")
    else:
        print("All problems have at least one link.")


if __name__ == "__main__":
    main()
