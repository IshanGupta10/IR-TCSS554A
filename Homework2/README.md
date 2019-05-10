---- Python Code -----

For this assignment, download the graph.txt and IR_HW_2.py files, and place them in a same folder.

You'll require python 3.7+ installed in your system, and will require pandas and numpy modules.

To run the file, goto the downloaded folder of two files via terminal and run - 

python3 IR_HW_2.py

-------------------------------------------------------------------------------

---- C++ Code -----

For this assignment, download the graph.txt and ir_hw_2.cpp files, and place them in a same folder.

You'll require C++14 installed on your system in form of g++ (Linux or MacOS) for Windows use cygwin or some C++ windows compiler..

To run the file, goto the downloaded folder of two files via terminal and run - 

g++ ir_hw_2.cpp -o ir_hw_2 -w

./ir_hw_2


The C++ code only generates M matrix, A matrix, and original vector. Due to C++ limitations over
decimal comparisons the code cannot check decimal absolute comparisons and hence produces incorrect
computations in its convergence of two rank vectors or M and A respectively.

-------------------------------------------------------------------------------
For this assignment, I've considered following equations for M and A matrices -

M : r(t+1) = M*R(t) PageRank presentation, Page 37

A : r(t+1) = Sigma(damp_factor * M Matrix * r(t) + r(t+1) = Sigma(beta * M Matrix * r(t) + ((1-beta)/(total_nodes)))) PageRank equation [Brin-Page, 98] PageRank presentation, Page 43
