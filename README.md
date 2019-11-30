# Circular Trade and Fraud Detection

The objective of the project is to identify instances of circular trading in a given set of
transactions. A dataset containing 32449 unique buyers and sellers containing a total of 102256
transactions was used.

For analysis of transactions, we construct a “trade-network” in the form of a directed graph using
the provided dataset. Each trader who bought/sold commodities enters the graph network as a
node. For each transaction in the dataset, we construct a directed edge originating from the
buyer’s node to the seller’s node. A weight is also attributed with each edge in the graph which
is equal to the amount of money involved in the corresponding transaction.

Our approach is based on using heuristics from existing graph clustering algorithms to identify potentially fraudulent clusters.

Some examples of potential candidates for circular trade networks identified by our algorithm are given below. The number on the nodes indicates the buyer/seller ID.

![](https://raw.githubusercontent.com/ninadakolekar/fraud-detection/master/example_img1.png)
![](https://raw.githubusercontent.com/ninadakolekar/fraud-detection/master/example_img2.png)
![](https://raw.githubusercontent.com/ninadakolekar/fraud-detection/master/example_img3.png)

# Contributors
Ninad Akolekar

Faizul Haq

Ayush Pateria

# Guide
Dr. Sobhan Babu

Associate Professor

Department of Computer Science & Engineering

IIT Hyderabad

