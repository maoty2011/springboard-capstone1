## Problem

Algorithmic trading of securities is one of the modern approaches to financial investment. This project attempts to obtain an effective strategy for trading a collection of stocks/futures. In other words, our goal is to make a machine learning model to predict the returns and volatilities of these target instruments, then construct and maintain a portfolio based on the model. The instrument collection will potentially cover US, Europe and China markets. The measures to be used includes basic price/volume data, factors from the fundamental side, and (hopefully) some sentiment facts parsed from Twitter and other similar medias.

## Client

This project would come out in a form similar to brokerage research reports. The (virtual) clients would be trading firms.

## Data

The main data for this project comes from Quandl, Yahoo Finance (US & Europe markets), Wind.com.cn and other data providers (China market). 

## Modeling Approach

The model shall predict the expected return and a risk measure (like volatility) for an instrument on a given day. A supervised machine learning algorithm will be the first candidate to try out. One shall be cautious that markets in different countries may have different styles. Efforts shall be made to investigate the common points and differences between these markets, and to compare model performances in different environments.

## Deliverables

1. Python codes for data cleaning, exploratory analysis and modeling
2. Capstone project report (with backtest result)
3. Capstone project presentation
