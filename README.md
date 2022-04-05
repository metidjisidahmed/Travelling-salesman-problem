# Travelling salesman problem

##Introducing The problem
The travelling salesman problem (also called the travelling salesperson problem or TSP) asks the following question: "Given a list of cities and the distances between each pair of cities, what is the shortest possible route that visits each city exactly once and returns to the origin city?" It is an NP-hard problem in combinatorial optimization, important in theoretical computer science and operations research.

## Illustration 

![alt text](https://blog.psyquation.com/wp-content/uploads/2019/12/salesman-problem.png "Logo Title Text 1")

## Dependencies
> The installation of these libraries is a must to run the program 

1. [Pandas](https://pandas.pydata.org/)
2. [Graphviz](https://graphviz.org/)
3. [NetworkX](https://networkx.org/)
4. [Matplotlib](https://matplotlib.org/)
5. [Pytest](https://docs.pytest.org/en/7.1.x/)

## How to Run ? 

In [tests.py](https://github.com/metidjisidahmed/TPGO_TP_4/blob/main/tests.py) : you will find The unit Tests to run for either The complete Algorithm or the greedy Algorithm 
> Note that the execution of the complete Algorithm will consume much time comparing to the greedy one


## Inputs

File | Description | Remark
--- | --- | ---
`data.xlsx`| An Excel Sheet which contains a symetric array defining the distance between the cities  | You have to fill only the lower half of the table
`starting_node` in [tests.py](https://github.com/metidjisidahmed/TPGO_TP_4/blob/main/tests.py)  | The node where our salesman will start his travel | Go to [tests.py](https://github.com/metidjisidahmed/TPGO_TP_4/blob/main/tests.py) and specify the desired starting node in the 9th line

### Inputs -Example-

![alt text](https://github.com/metidjisidahmed/TPGO_TP_4/blob/main/demo_data_sheet.png?raw=true "Logo Title Text 1")

### Outputs 

File | Description | Remark
--- | --- | ---
`myplot.svg`| A vectorized Image representing the **complete probability** tree generated using the library **NetworkX** and visalized using **Matplotlib**   | Open The Image in the Navigator for better visualization 
`myplot_greedy.svg`| A vectorized Image representing  the **greedy** tree  generated using the library **NetworkX** and visalized using **Matplotlib**   | Open The Image in the Navigator for better visualization
`result.txt` | a generated .txt file containing JSON object with two fields : *path*  and *final_distance* | path represents the optimized path and final_distance represents the cost of the optimized path

### Outputs -Example-

- `myplot.svg` 

  ![image](https://user-images.githubusercontent.com/43441621/161795582-e1a9f384-bd39-45c4-b946-21f614784ec8.png)
  
- `myplot_greedy.svg` 

  ![image](https://user-images.githubusercontent.com/43441621/161794426-34341728-0914-46b4-9e6c-eb0ef5fea74a.png)  
  
- `result.txt`

  ```javascript
  {"final_distance": 100.0, "path": ["1", "4", "2", "5", "3", "6"]}
  ``` 
