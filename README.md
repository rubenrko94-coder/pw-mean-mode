# px-mean-mode

Algoritmo simple para calcular media y moda por columna de un dataset (JSON/CSV/Parquet).

## Construir
```
docker build -t <tu_usuario_dh>/px-mean-mode:1.0.0 .
```

## Run
```
docker run --rm \
  -v "$PWD/mi_dataset.json:/data/input.json:ro" \
  -v "$PWD/out:/out" \
  docker.io/<tu_usuario_dh>/px-mean-mode:1.0.0 \
  --input /data/input.json --output /out/stats.json
```

## Subir a docker hub (dh)
```
docker login
docker tag <tu_usuario_dh>/px-mean-mode:1.0.0 <tu_usuario_dh>/px-mean-mode:latest
docker push <tu_usuario_dh>/px-mean-mode:1.0.0
docker push <tu_usuario_dh>/px-mean-mode:latest
```