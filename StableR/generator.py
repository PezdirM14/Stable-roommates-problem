import csv
def generator(n):
    a=list(range(1,n+1))
    with open('sostanovalci.csv', 'w', newline='') as csvfile:
        for item in a:
            csv.writer(csvfile).writerow([item])


    
