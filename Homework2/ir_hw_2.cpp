#include <fstream>
#include <string>
#include <iostream>
#include <map>
#include <vector>
#include <cmath>

using namespace std;

vector<vector<double> > generate_m_matrix(map<char, vector<char> > &adjacencyList){
	vector<vector<double> > m_matrix;
	for(auto i: adjacencyList){
		vector<double> row;
		for(int j = 0; j < adjacencyList.size(); ++j)
			row.push_back(0.0);
		m_matrix.push_back(row);
	}

	for(auto i: adjacencyList){
		for(auto j : i.second){
			m_matrix[j - 'A'][i.first - 'A'] = 1.0 / i.second.size();
		}
	}
	return m_matrix;
}


vector<vector<double> > getOriginalRankVector(map<char, vector<char> > &adjacencyList){
	vector<vector<double> > rank_vector;

	for (int i = 0; i < adjacencyList.size(); ++i)
	{
		vector<double> row;
		row.push_back(1.0/adjacencyList.size());
		rank_vector.push_back(row);
	}

	return rank_vector;
}

vector<vector<double> > generate_a_matrix(vector<vector<double> > &a_matrix, double beta, map<char, vector<char> > &adjacencyList){

	for (int i = 0; i < a_matrix.size(); ++i)
		for (int j = 0; j < a_matrix[i].size(); ++j)
			a_matrix[i][j] = beta * a_matrix[i][j] + ((1.0 - beta) / adjacencyList.size()); 
	return a_matrix;
}


bool checkThreshold(vector<vector<double> > &r_t, vector<vector<double> > &r_t_plus_1){

	for (int i = 0; i < r_t.size(); ++i){
		if(fabs(r_t[i][0] - r_t_plus_1[i][0]) < 1e-06){
			return true;
		}
	}
	return false;
}


void powerConvergeMatrixA(vector<vector<double> > &m_matrix, vector<vector<double> > &original_rank_vector, vector<vector<double> > &converged_vector_a, int &iterations_a){
	int power = 0;

	vector<vector<double> > r_t, r_t_plus_1;
	r_t = original_rank_vector;
	r_t_plus_1 = original_rank_vector;


	for (int i = 0; i < r_t_plus_1.size(); ++i)
		for (int j = 0; j < r_t_plus_1[i].size(); ++j)
			r_t_plus_1[i][j] = 0.0;

	while(!(checkThreshold(r_t, r_t_plus_1))){

		r_t = original_rank_vector;

    	for(int i = 0; i < m_matrix.size(); ++i){
		    for(int k = 0; k < m_matrix.size(); ++k)
		       r_t_plus_1[i][0] += m_matrix[i][k] * r_t[k][0]; 
			r_t_plus_1[i][0] = 0.85 * r_t_plus_1[i][0] + 0.025;
		}
		original_rank_vector = r_t_plus_1;
		power++;
	}
	iterations_a = power;
	converged_vector_a = r_t_plus_1;
	return;
}


void powerConvergeMatrixM(vector<vector<double> > &m_matrix, vector<vector<double> > &original_rank_vector, vector<vector<double> > &converged_vector_m, int &iterations_m){
	int power = 0;

	vector<vector<double> > r_t, r_t_plus_1;
	r_t = original_rank_vector;
	r_t_plus_1 = original_rank_vector;


	for (int i = 0; i < r_t_plus_1.size(); ++i)
			r_t_plus_1[i][0] = 0.0;

	while(!(checkThreshold(r_t, r_t_plus_1))){

		r_t = original_rank_vector;

    	for(int i = 0; i < m_matrix.size(); ++i){
		    for(int k = 0; k < m_matrix.size(); ++k){
		       r_t_plus_1[i][0] += m_matrix[i][k] * r_t[k][0]; 
		   }
		}
		original_rank_vector = r_t_plus_1;

		power++;
	}
	iterations_m = power;
	converged_vector_m = r_t_plus_1;
	return;
}


int main(){
	std::ifstream infile("./graph.txt");
	double beta = 0.85;
	map<char, vector<char> > adjacencyList;
	vector<vector<double> > m_matrix;
	vector<vector<double> > original_rank_vector, converged_vector_m, converged_vector_a;
	int iterations_a, iterations_m;

	if (infile.is_open()) {
	    std::string line;
	    char a, b;
	    int c;
	    while(infile>>a>>b>>c){
	    	if(adjacencyList.find(a) == adjacencyList.end()){
	    		vector<char> links;
	    		adjacencyList[a] = links;
	    		if(c == 1)
	    			adjacencyList[a].push_back(b);
	    	} else{
	    		if(c == 1)
	    			adjacencyList[a].push_back(b);
	    	}
	    }
	    infile.close();
	}

	m_matrix = generate_m_matrix(adjacencyList);

	original_rank_vector = getOriginalRankVector(adjacencyList);

	vector<vector<double> > a_matrix = m_matrix;

	a_matrix = generate_a_matrix(a_matrix, beta, adjacencyList);


	// powerConvergeMatrixA(m_matrix, original_rank_vector, converged_vector_a, iterations_a);
	// powerConvergeMatrixM(m_matrix, original_rank_vector, converged_vector_m, iterations_m);

	cout<<"M Matrix : "<<endl;
	for(auto i: m_matrix){
		for(auto j: i)
			cout<<j<<" ";
		cout<<endl;
	}

	cout<<endl<<"A Matrix : "<<endl;
	for(auto i: a_matrix){
		for(auto j: i)
			cout<<j<<" ";
		cout<<endl;
	}

	cout<<endl<<"Original Rank Vector : "<<endl;
	for(auto i: original_rank_vector){
		for(auto j: i)
			cout<<j<<" ";
		cout<<endl;
	}

	return 0;
}