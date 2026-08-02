import data
import indicator
import visualisation
import matplotlib.pyplot as plt


def main():
    ticker = "AAPL"
    interval = "1d"
    start_date = "2024-01-01"
    end_date = "2024-12-31"

    try:
        # import data
        # pour chaque data, appliquer une stratégie (qui donne un signal de trading 
        # Buy tel truc ou sell tel truc), qui s'applique localement (donc dans la boucle for data in datas)
        pass
        
    except Exception as e:
        print(f"Error: {e}")

main()