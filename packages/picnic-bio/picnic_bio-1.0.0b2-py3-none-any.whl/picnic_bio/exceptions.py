"""Custom exceptions for Picnic."""


class NoGoAnnotationFoundError(Exception):
    """Exception for cases when no GO annotation could be fetched from UniProt."""

    def __init__(self, uniprot_id):
        self.uniprot_id = uniprot_id
        self.message = (
            f"Could not find any GO annotations for protein {self.uniprot_id}! Therefore it is not "
            f"possible to calculate Picnic GO. Please use the default Picnic model (set boolean "
            f"flag <is_go> to False) for the score calculation."
        )
        super(Exception, self).__init__(self.message)
