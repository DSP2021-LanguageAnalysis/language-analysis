rank_categories = {
    'Fine-grained': {
        'Royalty': ['R'],
        'Nobility': ['N'],
        'Gentry, upper': ['GU'],
        'Gentry, lower': ['GL', 'G'],
        'Clergy, upper': ['CU'],
        'Clergy, lower': ['CL'],
        'Professional': ['P'],
        'Merchant': ['M'],
        'Other': ['O']
    },
    'Regular': {
        'Royalty': ['R'],
        'Nobility': ['N'],
        'Gentry': ['GU', 'GL', 'G'],
        'Clergy': ['CU', 'CL'],
        'Professional': ['P'],
        'Merchant': ['M'],
        'Other': ['O']
    },
    'Tripartite': {
        'Upper': ['R', 'N', 'GU', 'GL', 'G', 'CU'],
        'Middle': ['CL', 'P', 'M'],
        'Lower': ['O']
    },
    'Bipartite': {
        'Gentry': ['R', 'N', 'GU', 'GL', 'G', 'CU'],
        'Non-gentry': ['CL', 'P', 'M', 'O']
    }
}

relationship_categories = {
    'Fine-grained': {
        'Nuclear family': ['FN'], 
        'Other family': ['FO'], 
        'Family servant': ['FS'],
        'Close friend': ['TC'], 
        'Other acquaintance': ['T']
    },
    'Grouped': {
        'Family': ['FN', 'FO', 'FS'], 
        'Friends': ['TC'], 
        'Other relationships': ['T']
    }
}