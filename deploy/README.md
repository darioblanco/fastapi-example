# Deploy

This folder contains [kustomize](https://kustomize.io/) resources that allow its
deployment into a Kubernetes cluster.

## Validate

Navigate to the directory that involves the target environment (either `staging/` or `production/`)

```sh
kustomize build .
# or to a .gitignored file
kustomize build . > output.yaml
```

`kustomize build` does not validate the output against the Kubernetes API, it only processes the Kustomize configuration.
To validate the output:

```sh
kustomize build . | kubectl apply --dry-run=client -f - -o yaml
```
