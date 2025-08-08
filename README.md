# tmygen

Generate **Typical Meteorological Year** (TMY) weather files *automatically tuned to building-energy simulation results*, following the method in **[Seyed Salehi, 2024]**.

## Why this exists

Traditional TMY builders are very old. Newer versions weight climate variables subjectively.  
`tmygen` skips that step: it picks months whose **simulation loads**
(best predict annual heating/cooling) -- removing guesswork.

See examples/sweep_weight_factors.ipynb for a parameter study.

## API/function usage
```python

	from tmygen import generate_tmy
	df = generate_tmy("multi_year.csv", "weights.csv")```
	
License
MIT. The implementation draws on concepts from ISO 15927-4,

but contains no copyrighted content from the standard.
## Quick-start

```bash
pip install -e .
tmygen --weather ./examples/city_1990-2020.csv \
       --weights ./examples/weight_factors.csv \
       --out ./outputs/tartu_tmy.csv```
