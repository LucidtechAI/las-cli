from las import Client

from lascli.util import NotProvided, nullable, json_path


def create_model(las_client: Client, field_config, **optional_args):
    if optional_args.get('base_model'):
        base_model = optional_args.pop('base_model')
        *organization_id, model_id = base_model.split('/')
        base_model = {'modelId': model_id}
        if organization_id:
            base_model['organizationId'] = organization_id[0]
        optional_args['base_model'] = base_model

    return las_client.create_model(field_config=field_config, **optional_args)


def list_models(las_client: Client, owner, max_results, next_token):
    return las_client.list_models(owner=owner, max_results=max_results, next_token=next_token)


def delete_model(las_client: Client, model_id):
    return las_client.delete_model(model_id=model_id)


def get_model(las_client: Client, model_id):
    return las_client.get_model(model_id=model_id)


def update_model(las_client: Client, model_id, **optional_args):
    if 'training_id' in optional_args:
        training_id = optional_args.pop('training_id')
        optional_args['trainingId'] = training_id
    return las_client.update_model(model_id=model_id, **optional_args)


def create_data_bundle(las_client: Client, model_id, dataset_ids, **optional_args):
    return las_client.create_data_bundle(model_id=model_id, dataset_ids=dataset_ids, **optional_args)


def list_data_bundles(las_client: Client, model_id, max_results, next_token):
    return las_client.list_data_bundles(model_id, max_results=max_results, next_token=next_token)


def list_all_data_bundles(las_client: Client):
    print('Getting models...')
    models = las_client.list_models()['models']
    print(f'Found {len(models)} models')
    return {model['modelId']: las_client.list_data_bundles(model['modelId']) for model in models}


def delete_data_bundle(las_client: Client, model_id, data_bundle_id):
    return las_client.delete_data_bundle(model_id, data_bundle_id)


def update_data_bundle(las_client: Client, model_id, data_bundle_id, **optional_args):
    return las_client.update_data_bundle(model_id, data_bundle_id, **optional_args)

def create_training(las_client: Client, model_id, data_bundle_ids, instance_type, **optional_args):
    return las_client.create_training(
        model_id=model_id,
        data_bundle_ids=data_bundle_ids,
        instance_type=instance_type,
        **optional_args,
    )


def list_trainings(las_client: Client, model_id, max_results, next_token):
    return las_client.list_trainings(model_id, max_results=max_results, next_token=next_token)


def update_training(las_client: Client, model_id, training_id, **optional_args):
    if optional_args.pop('cancel'):
        optional_args['status'] = 'cancelled'
    return las_client.update_training(model_id, training_id, **optional_args)


def create_models_parser(subparsers):
    parser = subparsers.add_parser('models')
    subparsers = parser.add_subparsers()
    create_parser = subparsers.add_parser('create')
    create_parser.add_argument(
        'field_config',
        type=json_path,
        help='path to configuration of the fields that the model will predict',
    )
    create_parser.add_argument(
        '--preprocess-config',
        '-p',
        type=json_path,
        help='path to configuration of the step before the prediction',
    )
    create_parser.add_argument(
        '--metadata',
        type=json_path,
        help='path to json file with whatever you need, maximum limit 4kB',
    )
    create_parser.add_argument('--name')
    create_parser.add_argument('--description')
    create_parser.add_argument(
        '--base-model',
        help='Specify which model to use as base model. Example: las:organization:cradl/las:model:invoice',
    )
    create_parser.set_defaults(cmd=create_model)

    get_parser = subparsers.add_parser('get')
    get_parser.add_argument('model_id')
    get_parser.set_defaults(cmd=get_model)

    update_parser = subparsers.add_parser('update')
    update_parser.add_argument('model_id')
    update_parser.add_argument(
        '--field-config',
        '-f',
        type=json_path,
        help='path to configuration of the fields that the model will predict',
    )
    update_parser.add_argument(
        '--preprocess-config',
        '-p',
        type=json_path,
        help='path to configuration of the step before the prediction',
    )
    update_parser.add_argument('--name', type=nullable(str), default=NotProvided)
    update_parser.add_argument('--description', type=nullable(str), default=NotProvided)
    update_parser.add_argument(
        '--metadata',
        type=json_path,
        help='path to json file with whatever you need, maximum limit 4kB',
    )
    update_parser.add_argument(
        '--training-id',
        type=nullable(str),
        default=NotProvided,
        help='Use training_id for model inference in POST /predictions. Specify "null" to make model inactive.',
    )
    update_parser.set_defaults(cmd=update_model)

    delete_parser = subparsers.add_parser('delete')
    delete_parser.add_argument('model_id')
    delete_parser.set_defaults(cmd=delete_model)

    list_parser = subparsers.add_parser('list')
    list_parser.add_argument('--owner', '-o', nargs='+', help='Organizations whose models to list')
    list_parser.add_argument('--max-results', '-m', type=int, default=None)
    list_parser.add_argument('--next-token', '-n', type=str, default=None)
    list_parser.set_defaults(cmd=list_models)

    create_data_bundle_parser = subparsers.add_parser('create-data-bundle')
    create_data_bundle_parser.add_argument('model_id')
    create_data_bundle_parser.add_argument('dataset_ids', nargs='+')
    create_data_bundle_parser.add_argument('--name')
    create_data_bundle_parser.add_argument('--description')
    create_data_bundle_parser.set_defaults(cmd=create_data_bundle)

    list_data_bundles_parser = subparsers.add_parser('list-data-bundles')
    list_data_bundles_parser.add_argument('model_id')
    list_data_bundles_parser.add_argument('--max-results', '-m', type=int, default=None)
    list_data_bundles_parser.add_argument('--next-token', '-n', type=str, default=None)
    list_data_bundles_parser.set_defaults(cmd=list_data_bundles)

    list_all_data_bundles_parser = subparsers.add_parser('list-all-data-bundles')
    list_all_data_bundles_parser.set_defaults(cmd=list_all_data_bundles)

    update_data_bundles_parser = subparsers.add_parser('update-data-bundle')
    update_data_bundles_parser.add_argument('model_id')
    update_data_bundles_parser.add_argument('data_bundle_id')
    update_data_bundles_parser.add_argument('--name', type=nullable(str), default=NotProvided)
    update_data_bundles_parser.add_argument('--description', type=nullable(str), default=NotProvided)
    update_data_bundles_parser.set_defaults(cmd=update_data_bundle)

    delete_data_bundles_parser = subparsers.add_parser('delete-data-bundle')
    delete_data_bundles_parser.add_argument('model_id')
    delete_data_bundles_parser.add_argument('data_bundle_id')
    delete_data_bundles_parser.set_defaults(cmd=delete_data_bundle)

    create_training_parser = subparsers.add_parser('create-training')
    create_training_parser.add_argument('model_id')
    create_training_parser.add_argument('data_bundle_ids', nargs='+')
    create_training_parser.add_argument('--instance-type')
    create_training_parser.add_argument('--name')
    create_training_parser.add_argument('--description')
    create_training_parser.add_argument(
        '--metadata',
        type=json_path,
        help='path to json file with whatever you need, maximum limit 4kB',
    )
    create_training_parser.set_defaults(cmd=create_training)

    list_trainings_parser = subparsers.add_parser('list-trainings')
    list_trainings_parser.add_argument('model_id')
    list_trainings_parser.add_argument('--max-results', '-m', type=int, default=None)
    list_trainings_parser.add_argument('--next-token', '-n', type=str, default=None)
    list_trainings_parser.set_defaults(cmd=list_trainings)

    update_training_parser = subparsers.add_parser('update-training')
    update_training_parser.add_argument('model_id')
    update_training_parser.add_argument('training_id')
    update_training_parser.add_argument('--cancel', action='store_true', default=False)
    update_training_parser.add_argument('--name')
    update_training_parser.add_argument('--description', type=nullable(str), default=NotProvided)
    update_training_parser.add_argument(
        '--metadata',
        type=json_path,
        help='path to json file with whatever you need, maximum limit 4kB',
    )
    update_training_parser.set_defaults(cmd=update_training)

    return parser
