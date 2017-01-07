


class IDManager:
    """
        define some behaviour to be applied over the table uid
    """ 

    
    title = "url" 

    extract = lambda url : int( url.split('/')[-1] ) 

    reconstruct = lambda n : 'http://X/view_record/' + str(n) 
