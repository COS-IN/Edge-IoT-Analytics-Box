

class DataAnalyzer(object):

    """
        Analyzes given window of data to generate a new window 
    """

    def __init__(self):
        pass

    def analyze(self, df):
        def add_one(row):
            return row + 1.0
        tagi = '_time' 
        df = df.set_index(tagi)
        df = df.apply( add_one )
        df = df.reset_index()
        return df

