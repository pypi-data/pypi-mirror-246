import click
from . import features
from ..output.table import output_entry
from .. import billing


@click.command(name="list-features")
@click.pass_context
def cli_command_list_features(ctx, **kwargs):
    results = features.list_features(ctx, **kwargs)
    print(features.format_features(ctx, results))


@click.command(name="add-feature")
@click.argument("name")
@click.argument("key")
@click.option("--priority", default=None, type=int)
@click.option("--description", default=None)
@click.option("--min", type=int, default=None)
@click.option("--max", type=int, default=None)
@click.option("--enabled", type=bool, default=None)
@click.pass_context
def cli_command_add_feature(ctx, **kwargs):
    result = features.add_feature(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@click.command(name="delete-feature")
@click.argument("feature-id")
@click.pass_context
def cli_command_delete_feature(ctx, *args, **kwargs):
    features.delete_feature(ctx, *args, **kwargs)


@click.command(name="show-feature")
@click.argument("feature_id")
@click.pass_context
def cli_command_show_features(ctx, *args, **kwargs):
    result = features.get_features(ctx, *args, **kwargs)
    output_entry(ctx, result.to_dict())


@click.command(name="update-feature")
@click.argument("feature_id")
@click.option("--name", default=None)
@click.option("--priority", default=None, type=int)
@click.option("--description", default=None)
@click.option("--min", type=int, default=None)
@click.option("--max", type=int, default=None)
@click.option("--enabled", type=bool, default=None)
@click.pass_context
def cli_command_update_feature(ctx, *args, **kwargs):
    result = features.update_feature(ctx, *args, **kwargs)
    output_entry(ctx, result.to_dict())


@click.command(name="list-feature-subscriptions")
@click.argument("feature_id")
@click.pass_context
def cli_command_list_feature_subscriptions(ctx, **kwargs):
    results = features.list_feature_subscriptions(ctx, **kwargs)
    print(billing.format_subscriptions(ctx, results))


all_funcs = [func for func in dir() if "cli_command_" in func]


def add_commands(cli):
    glob = globals()
    for func in all_funcs:
        cli.add_command(glob[func])
