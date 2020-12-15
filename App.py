def getDataFromFile(filename):
    print(filename)

    dict1 = {}

    with open(filename) as f:
        for line in f:
            print(line)



getDataFromFile("historicalPrices/historicalPriceAZEK.txt")