
def do_number(numb:int):
    if numb < 1000:
        return numb
    elif numb>=1000 and numb < 1000000:
        new_numb = numb/1000
        if type(new_numb) == float:
            refactored = str(new_numb).split('.')
            if len(refactored[1]) >  1:
                refactored = '.'.join([refactored[0], refactored[1][:2]])
            else:
                refactored = '.'.join([refactored[0], refactored[1]+'0'])
        else:
            refactored = str(new_numb)

        return new_numb + 'K'
    
    elif numb>=1000000 and numb < 1000000000:
        new_numb = numb/1000000
        if type(new_numb) == float:
            refactored = str(new_numb).split('.')
            refactored = '.'.join([refactored[0], refactored[1][:1]])
        else:
            refactored = str(new_numb)

        return new_numb + 'M'
    
    elif numb>=1000000000 and numb < 1000000000000:
        new_numb = numb/1000000000
        if type(new_numb) == float:
            refactored = str(new_numb).split('.')
            if len(refactored[1]) >  1:
                refactored = '.'.join([refactored[0], refactored[1][:2]])
            else:
                refactored = '.'.join([refactored[0], refactored[1]+'0'])
        else:
            refactored = str(new_numb)

        return new_numb + 'B'
    
    else:
        new_numb = numb/1000000000000
        if type(new_numb) == float:
            refactored = str(new_numb).split('.')
            if len(refactored[1]) >  1:
                refactored = '.'.join([refactored[0], refactored[1][:2]])
            else:
                refactored = '.'.join([refactored[0], refactored[1]+'0'])
        else:
            refactored = str(new_numb)

        return new_numb + 'T'
    
    

    
    
            