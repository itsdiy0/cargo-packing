def get_simple_instance():
    return {
        'name': 'Simple Instance',
        'container': {'width': 20, 'depth': 15, 'max_weight': 1000},
        'cylinders': [
            {'diameter': 2.0, 'weight': 100},
            {'diameter': 2.0, 'weight': 100},
            {'diameter': 2.0, 'weight': 100},
            {'diameter': 2.0, 'weight': 100}
        ],
        'ga_params': {'population_size': 50, 'mutation_rate': 0.05, 'step_size': 0.5, 'max_generations': 100}
    }


def get_medium_instance():
    return {
        'name': 'Medium Instance',
        'container': {'width': 20, 'depth': 15, 'max_weight': 2000},
        'cylinders': [
            {'diameter': 3.0, 'weight': 200},
            {'diameter': 2.5, 'weight': 150},
            {'diameter': 2.0, 'weight': 100},
            {'diameter': 2.0, 'weight': 100},
            {'diameter': 1.5, 'weight': 80},
            {'diameter': 1.5, 'weight': 80}
        ],
        'ga_params': {'population_size': 100, 'mutation_rate': 0.02, 'step_size': 0.5, 'max_generations': 200}
    }


def get_challenging_instance():
    return {
        'name': 'Challenging Instance',
        'container': {'width': 18, 'depth': 12, 'max_weight': 2000},
        'cylinders': [
            {'diameter': 3.0, 'weight': 200},
            {'diameter': 2.5, 'weight': 150},
            {'diameter': 2.5, 'weight': 150},
            {'diameter': 2.0, 'weight': 100},
            {'diameter': 2.0, 'weight': 100},
            {'diameter': 2.0, 'weight': 100},
            {'diameter': 1.5, 'weight': 80},
            {'diameter': 1.5, 'weight': 80}
        ],
        'ga_params': {'population_size': 150, 'mutation_rate': 0.1, 'step_size': 0.2, 'max_generations': 300}
    }


def get_very_challenging_instance():
    return {
        'name': 'Very Challenging Instance',
        'container': {'width': 15, 'depth': 12, 'max_weight': 1800},
        'cylinders': [
            {'diameter': 2.5, 'weight': 150},
            {'diameter': 2.2, 'weight': 120},
            {'diameter': 2.0, 'weight': 100},
            {'diameter': 2.0, 'weight': 100},
            {'diameter': 1.8, 'weight': 90},
            {'diameter': 1.8, 'weight': 90},
            {'diameter': 1.5, 'weight': 80},
            {'diameter': 1.5, 'weight': 80},
            {'diameter': 1.5, 'weight': 80},
            {'diameter': 1.2, 'weight': 60}
        ],
        'ga_params': {'population_size': 200, 'mutation_rate': 0.1, 'step_size': 0.15, 'max_generations': 400}
    }


def get_all_test_instances():
    return [
        get_simple_instance(),
        get_medium_instance(),
        get_challenging_instance(),
        get_very_challenging_instance()
    ]