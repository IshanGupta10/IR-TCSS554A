For this assignment, download the graph.txt and IR_HW_2.py files, and place them in a same folder.

You'll require pandas ans numpy installed to execute the python script.

To run the file, goto the downloaded folder of two files via terminal and run - 
python3 IR_HW_2.py

For this assignment, I've considered following equations for M and A matrices -

M : r(t+1) = M*R(t) PageRank presentation, Page 37
A : r(t+1) = Sigma(damp_factor * M Matrix * r(t) + leap_probability) PageRank equation [Brin-Page, 98] PageRank presentation, Page 43