# nyc_prop_prediction
This is a library designed for quick prediciton of housing prices in nyc

## Example
Suppose I want to find companies that have filed either an S-1, 10-K or 10-Q between January 2021 and March 2023
```python
predictor = predict()
sqft = 500
year_built = 1970
year_sold = 2023
num_libraries = 1
num_parks = 5
num_schools = 0
zipcode = 10037
mod = nyc_prop_prediction.predict()
input = [[sqft,year_built,year_sold,num_libraries,num_parks,num_schools]]

print(predictor.predict_price(input_type='zipcode',model='gradient',inputs=input))

```

## Installation
`nyc_prop_prediction` can be installed via PyPi by running:
```python
pip install nyc_prop_prediction
```
