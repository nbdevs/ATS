# [Algorithmic Trading: Machine Learning in Complex Adaptive Markets](https://drive.google.com/drive/u/1/folders/1DPy4UjKC6Qoqmo3NNMyVQoGcqyxk-WmP)

![image](https://user-images.githubusercontent.com/75015699/158418219-28257172-616b-484e-b0bf-e6e9ce9c59a1.png)


This repository stores the Python development for the algorithmic trading system.

---
## Summary

Machine learning models have become too complex as a result of closely following the entities within the sample set, and so although more observations can be accounted for the overfitting nature means that the model will fail to replicate its performance on an unseen dataset i.e. the real world. On a macro level, an investor will lose their portfolio value if this is the case. *Thus a way to **successfully** reduce the inherent complexity of ML models and thereby improve the potential return of the investor's portfolio is critical to long-term success for investors*. Hence the metaheuristic algorithm **Particle Swarm Optimisation** (PSO) was developed in order to enhance the classification accuracy of the baseline machine learning model - **Random Forest**. For further insight you can read the thesis for this project **[here](https://drive.google.com/drive/u/1/folders/1DPy4UjKC6Qoqmo3NNMyVQoGcqyxk-WmP)**.

The program also has further functionality as a filesystem which manages the results of user testing by providing two distinct user views of the system with different abilities granted to the two types of users: 

1. Trader can
- Evaluate the performance of stocks
- View reports
- Create reports

2. Software Operator can
- Delete reports
- View reports
- Clear reports
- Create reports

This project utilises:
1. Machine learning concepts written in Python via the [**scikit-learn** ](https://github.com/scikit-learn/scikit-learn) library.
2. N-dimensional arrays via the [**NumPy**](https://github.com/numpy/numpy) library.
3. Data manipulation and analysis library [**pandas**](https://github.com/pandas-dev/pandas).
4. Outlier detection and management with the [**SciPy**](https://github.com/scipy/scipy) library.
5. Stock data from the **Yahoo Finance API** through the yfinance library.

---
## Environment set up (MacOS)
```
$ mkdir project_run                             # create a new folder to store the virtual environment
```
```
$ python3 -m venv project_run/project_env       # create a new python virtual environment inside the new folder
```
```
$ source project_run/project_env/bin/activate               # activate the virtual environment you have just created
```
```
$ pip install -r requirements.txt               # install the requirements required for the project within the virtual environment
```

## Stock collection

![image](https://user-images.githubusercontent.com/75015699/158699712-66897304-a2e8-4490-96c1-d0122752c535.png)

All stock data used within this program must be from the **Nasdaq100 index**. 

An example of stock symbols and the formats required in the program are listed in the table below:
|Stock symbol|Stock Name|
|:---:|---|
|[AMZN](https://www.nasdaq.com/market-activity/stocks/amzn)|Amazon.com, Inc. Common Stock|
|[AAPL](https://www.nasdaq.com/market-activity/stocks/aapl)|Apple Inc. Common Stock|
|[MSFT](https://www.nasdaq.com/market-activity/stocks/msft)|Microsoft Inc. Common Stock|


## Demonstration

A demonstration of the project in action as well as an overview of the process and commentary on results can be viewed [here](https://drive.google.com/file/d/10a4GH36GuvdEJifNrvaxQ8-XLMe5CELd/view?usp=sharing).



