import argparse, json, sys
import pandas as pd
from pathlib import Path

def load_any(path: Path) -> pd.DataFrame:
    p = str(path)
    if p.endswith((".json", ".jsonl")):
        # JSON array o JSON lines
        try:
            return pd.read_json(p, orient="records", lines=p.endswith(".jsonl"))
        except ValueError:
            # fallback: intentar normalizar
            with open(p, "r", encoding="utf-8") as f:
                obj = json.load(f)
            return pd.json_normalize(obj)
    if p.endswith(".csv"):
        return pd.read_csv(p)
    if p.endswith((".parquet", ".pq")):
        return pd.read_parquet(p)
    raise ValueError(f"Formato no soportado: {p}")

def mode_with_count(series: pd.Series):
    # Devuelve (valor_moda, frecuencia). Si hay varias modas, toma la primera ordenada por frecuencia y valor.
    vc = series.value_counts(dropna=True)
    if vc.empty:
        return None, 0
    top_count = vc.iloc[0]
    # Posibles empatadas
    candidates = vc[vc == top_count].index
    val = sorted(candidates)[0] if len(candidates) > 1 else candidates[0]
    # Convertir tipos no JSON-serializables
    if pd.isna(val):
        val = None
    if hasattr(val, "item"):
        try:
            val = val.item()
        except Exception:
            val = str(val)
    return val, int(top_count)

def summarize(df: pd.DataFrame):
    out = []
    for col in df.columns:
        s = df[col]
        dtype = str(s.dtype)
        nulls = int(s.isna().sum())
        uniques = int(s.nunique(dropna=True))
        # media solo para numéricos
        mean = float(s.mean()) if pd.api.types.is_numeric_dtype(s) else None
        mval, mcount = mode_with_count(s)
        out.append({
            "column": col,
            "dtype": dtype,
            "mean": mean,
            "mode": mval,
            "mode_count": mcount,
            "null_count": nulls,
            "unique_count": uniques,
            "non_null_count": int(s.notna().sum()),
        })
    return {"rows": int(len(df)), "cols": int(df.shape[1]), "summary": out}

def main():
    ap = argparse.ArgumentParser(description="Calcula media y moda por columna")
    ap.add_argument("--input", required=True, help="Ruta de entrada (json/csv/parquet)")
    ap.add_argument("--output", required=True, help="Ruta de salida JSON")
    args = ap.parse_args()

    try:
        df = load_any(Path(args.input))
        result = summarize(df)
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"OK - guardado en {args.output}")
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
