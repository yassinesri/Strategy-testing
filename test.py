import data

tickers_list = ["AAPL"]
interval = "1d"
start_date = "2024-01-01"
end_date = "2024-12-31"
data.import_data(tickers_list[0], "Close", interval, start_date, end_date)
print(data.prices_data.index[0].date().day==2)