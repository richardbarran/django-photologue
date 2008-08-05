def get_response(msg, func=int, default=None):
    while True:
        resp = raw_input(msg)
        if not resp and default is not None:
            return default            
        try:
            return func(resp)
        except:
            print 'Invalid input.'