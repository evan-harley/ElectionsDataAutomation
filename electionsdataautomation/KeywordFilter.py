import yake

class KeywordFilter:
    def __init__(self) -> None:
        self.main_topics = [
            'Transportation',
            'Infrastructure',
            'Transit',
            'Public Transit'
        ]
        self.subtopics = [
            'Policies',
            'Plans',
            'Proposals',
            'Projects',
            'Investments',
            'Funding',
            'Initiatives',

        ]
        self.political_parties = [
            'BC NDP',
            'BC United',
            'BC Green Party',
            'BC Conservative Party',
        ]

        self.people = [
            'David Eby',
            'Kevin Falcon',
            'Sonia Furstenau',
            'John Rustad',
            'Trevor Halford'
        ]

        self.specific_projects = [
            'Broadway Subway Project',
            'Pattullo Bridge',
            'Highway 1',
        ]

        self.extractor = yake.KeywordExtractor(n=4)

