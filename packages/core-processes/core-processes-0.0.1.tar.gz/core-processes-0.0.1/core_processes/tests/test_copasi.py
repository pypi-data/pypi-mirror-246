from process_bigraph import Composite, pf


def test_process():

    # this is the instance for the composite process to run
    initial_sim_state = {
        'odeint': {
            '_type': 'process',
            'address': 'local:copasi',  # using a local toy process
            'config': {
                'model_file': 'core_processes/tests/model_files/Caravagna2010.xml'  #
            },
            'wires': {
                'time': ['time_store'],
                'floating_species': ['floating_species_store'],
                # 'boundary_species': ['boundary_species_store'],
                'model_parameters': ['model_parameters_store'],
                'reactions': ['reactions_store'],
            }
        },
        'emitter': {
            '_type': 'step',
            'address': 'local:ram-emitter',
            'config': {
                'ports': {
                    'inputs': {
                        'floating_species': 'tree[float]'
                    }
                }
            },
            'wires': {
                'inputs': {
                    'floating_species': ['floating_species_store'],
                }
            }
        }
    }

    # make the composite
    workflow = Composite({
        'state': initial_sim_state
    })

    # workflow.export_composite(filename='cobra_template')

    # run
    workflow.run(10)

    # gather results
    results = workflow.gather_results()
    print(f'RESULTS: {pf(results)}')


if __name__ == '__main__':
    test_process()
