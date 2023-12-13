from random import randint, choices

def __is_sorted(arr):
    return all(arr[i] <= arr[i+1] for i in range(len(arr) - 1))

def __votes(n):
    return sum(choices([0,1],k = n))

def sussy_sort(arr):
    """
    List of passengers is sussy sorted and imposters are ejected.
    
    Parameters:
    - arr (list): List of passengers.

    Returns:
    None
    
    """
    try:
        n = len(arr)    
        while n >= 1 and not __is_sorted(arr):
            sus = randint(0,n-1)
            if __votes(n-1) > (n-1) // 2:
                arr.pop(sus) 
                n -=1
    except:
        print("Your list is kinda sussy ඞ")
