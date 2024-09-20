import click
from db import insert_data, view_summary

@click.group()
def cli():
    """Personal Finance Tracker CLI."""
    pass

@cli.command()
def seed():
    """Seed the database with sample data."""
    insert_data()
    click.echo("Sample data inserted successfully.")

@cli.command()
@click.argument('user_id', type=int)
@click.argument('month', type=int)
def summary(user_id, month):
    """View summary of income and expenses for a given user and month."""
    total_income, total_expenses, net_balance = view_summary(user_id, month)
    click.echo(f"Total Income: {total_income}")
    click.echo(f"Total Expenses: {total_expenses}")
    click.echo(f"Net Balance: {net_balance}")

if __name__ == '__main__':
    cli()
