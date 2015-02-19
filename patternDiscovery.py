#!/usr/bin/python3
from pprint import pprint

def FrequentElements( elements = [], transactions = [], minSup = 0.5, debug = False ):
    """ This function get as input the list of the element to be tested, the list of transactions and the values of minimun support e minimum Confidence.
        The function returns a dictionary that has as keys the frequent elements and values a list with the count and the support
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
            #print( 'flag' );
            label = '';
            for a in element:
                label += ','+a;
                #label += a;

            label=label.lstrip(',');
            #print( label );

            for transaction in transactions:
                flag = 0;
                #print( "transaction = "+str(transaction) );
                #print( "flag = "+str(flag) );
                for field in element:
                    if ( transaction.count( field ) == 0 ):
                        flag -= 1;
                        break;

                if flag >= 0:
                    #print( "transaction = "+str(transaction) );
                    try:
                        allFrequencies[ label ] += 1;
                    except:
                        allFrequencies[ label ] = 1;
                    #print( allFrequencies );

    # purging dictionary
    for element in elements:
        if isinstance( element, str ):
            if allFrequencies[ element ] / numTransactions >= minSup:
                frequencies[ element ] = [ allFrequencies[ element ], allFrequencies[ element ] / numTransactions ];
        else:
            label = '';
            for a in element:
                label += ','+a;

            label=label.lstrip(',');

            if label in allFrequencies and allFrequencies[ label ] / numTransactions >= minSup:
                frequencies[ label ] = [ allFrequencies[ label ], allFrequencies[ label ] / numTransactions ];

    return frequencies;

def generateNextItemsetList( previousList = [], transactions = [] , debug = False ):
    """ This function generates (k+1)-itemset candidates starting from k-itemset
	if the previousList is empty the function generates the 1-itemset
        The function requires a sorted list as input and generate a sorted list for a new call of this function
    """
    if debug: print( previousList );
    k = len(previousList);
    #print( k );
    elements = [];
    # if the list is empty i generate all the possible 1-itemset
    if ( k == 0 ):
        for transaction in transactions:
            for element in transaction:
               try:
                   elements.index( [element] );
                   break;
               except:
                   elements.append( [element] );
    # if the itemset is not empty join as for apriori
    else:
        count = 0;
        for i in range( 0, k ):
            for j in range ( 0, i ):
                if (i != j):
                    for l in range ( 0, len(previousList[i])-1 ):
                        if ( previousList[i][l] != previousList[j][l] ):
                            break;
                    else:
                        elements.append( [] );
                        if debug : print( elements[count] );
                        if debug : print( previousList[i][0] );
                        for l in range ( 0, len(previousList[i])-1 ):
                            elements[count].append( previousList[i][l] );
                            #print( "pippo\n" );
                        elements[count].append( previousList[i][len(previousList[i])-1] );
                        elements[count].append( previousList[j][len(previousList[j])-1] );
                        elements[count] = sorted( elements[count] );
                        if debug : print( elements[count] );
                        count += 1;

    if debug : print( sorted(elements) );
    return sorted(elements);

# parto da file fisso elenco.txt con righe come
debug = False;
file = 'elenco.txt';
sep= ',';
minSup = 0.07;
minConf = 0.2;

a = open(file, 'r')
itemList = a.readlines()
a.close()

# used sorted for simplicity, so that same 2 items but in different order
# won't be added to 2-itemsets (i.e. Beer,Diaper and Diaper,Beed)
itemList = [sorted(item.rstrip('\n').split(sep)) for item in itemList]
elementList = generateNextItemsetList( [], itemList );
#print ( elementList );

frequencies = FrequentElements( elementList, itemList , minSup );
print( frequencies );

while ( True ):
    elementList = [];
    for a in frequencies.keys():
        elementList.append( a.split(',') );
    if debug : print ( elementList );

    elementList = generateNextItemsetList( elementList, itemList, debug );
    if debug : print ( elementList );

    frequencies = FrequentElements( elementList, itemList , minSup );
    pprint( frequencies );
 
    if len( frequencies ) == 0:
        break;

