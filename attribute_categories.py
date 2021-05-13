rank_categories = {
    'Fine-grained': {
        'Royalty': ['R'],
        'Nobility': ['N'],
        'Gentry, upper': ['GU'],
        'Gentry, lower': ['GL', 'GL?', 'G'],
        'Clergy, upper': ['CU'],
        'Clergy, lower': ['CL'],
        'Professional': ['P'],
        'Merchant': ['M'],
        'Other': ['O', 'O?']
    },
    'Regular': {
        'Royalty': ['R'],
        'Nobility': ['N'],
        'Gentry': ['GU', 'GL', 'GL?', 'G'],
        'Clergy': ['CU', 'CL'],
        'Professional': ['P'],
        'Merchant': ['M'],
        'Other': ['O', 'O?']
    },
    'Tripartite': {
        'Upper': ['R', 'N', 'GU', 'GL', 'GL?', 'G', 'CU'],
        'Middle': ['CL', 'P', 'M'],
        'Lower': ['O', 'O?']
    },
    'Bipartite': {
        'Gentry': ['R', 'N', 'GU', 'GL', 'GL?', 'G', 'CU'],
        'Non-gentry': ['CL', 'P', 'M', 'O', 'O?']
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
    'Bipartite': {
        'Family': ['FN', 'FO', 'FS'], 
        'Other': ['TC', 'T']
    }
}

relationship_labels = {
    'FN' : 'Nuclear Family Members',
    'FO' : 'Other Family Member',
    'FS' : 'Family Servant',
    'TC' : 'Close Friend',
    'T'  : 'Other Acquaintance'
}
