# heuristics
Define *l*<sub>*ij,t*</sub> has the shortest path from cell *ij* to target cell *t*.  
For each cell the Heuristic Value is the sum of heuristic function on the paths from the cell to each to the target state cell.  
If target state (t<sub>1</sub>, t<sub>2</sub>, t<sub>3</sub>) then 

Heuristic Value(*ij*) = 
h(*l*<sub>*ij,t<sub>1</sub>*</sub>) + h(*l*<sub>*ij,t<sub>2</sub>*</sub>)  + h(*l*<sub>*ij,t<sub>3</sub>*</sub>).

### Heuristic functions(*h*)
- Find the shortest path using Dijkstra, weight 1 for each cell and sum the path weights.  
h = *-1&middot;&sum;<sup>|l|</sup><sub>1</sub>1*
- Find the shortest path using Dijkstra, weight  *-log(probability<sub>*ij*</sub>)* and sum the path rewards.  
h = *&sum;<sub>c&isin; l</sub>-log(probability(c))*
- Find the shortest path using Dijkstra, weight 1 for each cell and sum the path rewards.  
h = *&sum;<sub>c&isin; l</sub>R(c)*
- Find the shortest path using Dijkstra, weight *-log(probability<sub>*ij*</sub>)*  
and add the probability to destruction multiply  by sink reward and probability to reach the target multiply  by target reward.  
h = *&prod;<sub>c&isin; l</sub> (probability(c))&middot;R(sink) + &prod;<sub>c&isin; l</sub> (1 - probability(c))&middot;R(target)*  
