from aiida.plugins import DataFactory, WorkflowFactory
from aiida import orm
from aiida.engine import submit

from aiida_common_workflows.common import ElectronicType, RelaxType, SpinType
from aiida_common_workflows.plugins import get_entry_point_name_from_class
from aiida_common_workflows.plugins import load_workflow_entry_point

PLUGIN_NAME = 'castep'
CODE_LABEL = 'castep-20.1.1@thomas'
SET_NAME = 'set2'

STRUCTURES_GROUP_LABEL = f'commonwf-oxides/{SET_NAME}/structures/{PLUGIN_NAME}'
WORKFLOWS_GROUP_LABEL = f'commonwf-oxides/{SET_NAME}/workflows/{PLUGIN_NAME}'

Structure = DataFactory('structure')

query = orm.QueryBuilder()
query.append(Structure, tag='structure', project=['extras', '*'])
query.append(orm.Group, tag='group', filters={'label': STRUCTURES_GROUP_LABEL}, with_node='structure')
all_structures = {(res[0]['element'], res[0]['configuration']): res[1] for res in query.all()}

structure = all_structures[('Ag', 'X2O')]
print(f'Structure PK: {structure.pk}')

sub_process_cls = load_workflow_entry_point('relax', 'castep')
sub_process_cls_name = get_entry_point_name_from_class(sub_process_cls).name
generator = sub_process_cls.get_input_generator()

# There should be only one
engine_types = generator.spec().inputs['engines']
engines = {}
for engine in engine_types:
    engines[engine] = {
        'code': CODE_LABEL,
         'options': {
            'resources': {
                'tot_num_mpiprocs': 24,
                'parallel_env': 'mpi',
            },
            'max_wallclock_seconds': 8 * 3600
        }
    }

inputs = {
    'structure': structure,
    'generator_inputs': {  # code-agnostic inputs for the relaxation
        'engines': engines,
        'protocol': 'oxides_validation',
        'relax_type': RelaxType.NONE,
        'electronic_type': ElectronicType.METAL,
        'spin_type': SpinType.NONE,
    },
    'sub_process_class': sub_process_cls_name,
}

cls = WorkflowFactory('common_workflows.eos')
submit(cls, **inputs)
