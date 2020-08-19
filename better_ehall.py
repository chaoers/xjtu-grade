import click
from pathlib import Path
from colorama import Fore, Style
from core.grade import GPACalculator, GradeParser


@click.group()
def cli():
    pass


@click.command(help='fetch grades')
@click.option('--update', default=False, is_flag=True, help='force update the grade file')
@click.option('--output', default='result/grade.csv', help='grade file output dir')
def fetch_grade(update, output):
    output_file = Path(output)
    if not output_file.parent.exists():
        output_file.parent.mkdir()

    if output_file.exists() and not update:
        print(
            f'{Fore.RED}Grade file already exist, setting update to true to update the file!')

    if update or not output_file.exists():
        grade = GradeParser()
        grade.save_csv(output_file)
        print(f'Fetching...')
        print(f'Done...')


@click.command(help='calculate your gpa using the grade file')
@click.option('--data-file', default='result/grade.csv', help='grade file dir')
def get_gpa(data_file):
    data_file = Path(data_file)
    if data_file.exists():
        gpa = GPACalculator(data_file)
        print(f'{Fore.BLUE}METHOD', '\t', f'{Fore.WHITE}GPA')
        print('-'*14)
        for method, gpa in gpa.get_gpa().items():
            print(f'{Fore.BLUE}{method}:', end=' ')
            print(f'{Fore.WHITE}{gpa}')
    else:
        print(f'{Fore.RED}Please run grade fetch first!')


cli.add_command(fetch_grade)
cli.add_command(get_gpa)


if __name__ == "__main__":
    cli()
