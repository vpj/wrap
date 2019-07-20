class Options:
    def __init__(self):
        # Log call signature
        self.signature = True
        # Log dimensions if they are tensors
        self.dimensions = True
        # Log every nth call
        self.log_every = 1
        # Log every multiplier
        self.log_every_multiplier = 1
