import click
from pathlib import Path
import sys
import pandas as pd
from .selector import generate_tmy

@click.command()
@click.option("--weather", "-w", type=click.Path(exists=True, dir_okay=False),
              required=True, help="CSV with multi-year hourly weather.")
@click.option("--weights", "-f", type=click.Path(exists=True, dir_okay=False),
              required=True, help="CSV of monthly weight factors.")
@click.option("--out", "-o", type=click.Path(dir_okay=False),
              default="tmy.csv", show_default=True,
              help="Output CSV for the generated TMY.")
def main(weather, weights, out):
    """Generate a Typical Meteorological Year using FS ranking."""
    df = generate_tmy(weather, weights)
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    click.echo(f"✅  Wrote {out} with {len(df):,} hourly rows.")


if __name__ == "__main__":
    sys.exit(main())
