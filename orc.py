from pathlib import Path

import click

import orc_parser

@click.group()
def cli():
    pass

@cli.command()
@click.argument("orc_path", type=Path)
def debug(orc_path):
    orc = orc_parser.parse(orc_path)
    breakpoint()

@cli.command()
@click.argument("orc_path", type=Path)
def headers(orc_path):
    orc = orc_parser.parse(orc_path)
    print("ORC Header:", orc_path)
    print("Symbols:", len(orc.symbols))
    print("Relocations:", len(orc.relocations))
    print("Sections:", len(orc.sections))
    print("Segments:", len(orc.segments))
    print("Contents:", len(orc.data))

@cli.command()
@click.argument("orc_path", type=Path)
def symbols(orc_path):
    orc = orc_parser.parse(orc_path)
    print("ORC Symbols:", orc_path)

    for i, symbol in enumerate(orc.symbols):
        print(i, symbol)

@cli.command()
@click.argument("orc_path", type=Path)
def relocations(orc_path):
    orc = orc_parser.parse(orc_path)
    print("ORC Relocations:", orc_path)

    for i, relocation in enumerate(orc.relocations):
        print(i, relocation)

@cli.command()
@click.argument("orc_path", type=Path)
def sections(orc_path):
    orc = orc_parser.parse(orc_path)
    print("ORC Sections:", orc_path)

    for i, section in enumerate(orc.sections):
        print(i, section)

@cli.command()
@click.argument("orc_path", type=Path)
def segments(orc_path):
    orc = orc_parser.parse(orc_path)
    print("ORC Segments:", orc_path)

    for i, segment in enumerate(orc.segments):
        print(i, segment)

if __name__ == "__main__":
    cli()
