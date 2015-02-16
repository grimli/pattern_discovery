#!/usr/bin/python3

def FrequentElements( elements = [], transactions = [], minSup = 0.5 , minConf = 0.5 ):
    """ Questa funzione prende gli elementi di elements, suppomendo che si tratti di liste, e conta 
        quante volte compaiono nelle transazioni riportate in itemlist.
	Restituisce un dizionario che ha per chiave gli elementi di elements e valori i rispettivi conteggi 

        Per ogni elemento di elements 
            se è una una stringa
                conta in quanti elementi di itemlist è presente
                costruisci la voce del dizionario
            se è una lista
                prendi il primo elemento
                per ogni elemento di itemlist che lo contienen
                    verifica se ci sono tutti gli elementi della lista
                        se si
                            crea voce dizionario
                        se no
                            vai all'elemento successivo
        pulisci il dizionario da elementi non frequenti
        restituisci il dizionario
    """
    frequencies = {};
    allFrequencies = {};
    label = '';
    numTransactions = len(transactions);

    for element in elements:
        if isinstance( element, str ):
            for transaction in transactions:
                try:
                    allFrequencies[ element ] += transaction.count( element );
                except:
                    allFrequencies[ element ] = transaction.count( element );
        else:
            label = '';
            for a in element:
                label += ','+a;

            label=label.lstrip(',');
            print( label );

            for transaction in transactions:
                flag = 0;
                for field in element:
                    if ( transaction.count( field ) == 0 ):
                        flag -= 1;
                        break;

                if flag >= 0:
                    try:
                        allFrequencies[ label ] += 1;
                    except:
                        allFrequencies[ label ] = 1;

    for element in elements:
        if isinstance( element, str ):
            if allFrequencies[ element ] / numTransactions >= minSup:
                frequencies[ element ] = allFrequencies[ element ];
        else:
            label = '';
            for a in element:
                label += ','+a;

            label=label.lstrip(',');

            if allFrequencies[ label ] / numTransactions >= minSup:
                frequencies[ label ] = allFrequencies[ label ];

    return frequencies;
         
def generateOneItemesetList ( itemset = [] ):
    """ Questa funzione genera la lista degli 1-itemsets a partire dalla tabella delle transazioni 
        Per il momento restituisco una lista ordinata
    """
    elements = [];
    for transaction in itemset:
        for element in transaction:
           try: 
               elements.index(element);
               break;
           except:
               elements.append(element);
    return sorted(elements);

# parto da file fisso elenco.txt con righe come
file = 'elenco.txt';
sep= ',';
minSup = 0.1;
minConf = 0.2;

a = open(file, 'r')
itemList = a.readlines()
a.close()

# used sorted for simplicity, so that same 2 items but in different order
# won't be added to 2-itemsets (i.e. Beer,Diaper and Diaper,Beed)
itemList = [sorted(item.rstrip('\n').split(sep)) for item in itemList]
elementList = generateOneItemesetList( itemList );

elencoDebug=[ ['biscotto','cioccolatino'], ['patata','banana'], ['broccolo', 'nutella', 'pane']];
#frequencies = FrequentElements( elementList, itemList , minSup, minConf );
frequencies = FrequentElements( elencoDebug, itemList , minSup, minConf );

#for rule in itemList:
#    print ( str(rule)) ;

print( frequencies );
