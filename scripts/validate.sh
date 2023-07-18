#!/usr/bin/env bash

# This script validates the kustomize overlays using kubeconform.
# This script is meant to be run locally and in CI before the changes
# are merged on the main branch.
# This script is adapted from the original one provided by the Flux authors.

# Copyright 2023 The Flux authors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Prerequisites
# - yq v4.34
# - kustomize v5.0
# - kubeconform v0.6

set -o errexit
set -o pipefail

# Get the directory of the current script
script_dir="$(dirname "${BASH_SOURCE[0]}")"

# shellcheck disable=SC1091
source "${script_dir}"/utils.sh

# mirror kustomize-controller build options
kustomize_flags=("--load-restrictor=LoadRestrictionsNone")
kustomize_config="kustomization.yaml"

# skip Kubernetes Secrets due to SOPS fields failing validation
kubeconform_flags=("-skip=Secret")
kubeconform_config=("-strict" "-ignore-missing-schemas" "-verbose")

find deploy -type f -name '*.yaml' -print0 | while IFS= read -r -d $'\0' file;
do
	print_blue "Validating YAML format for $file"
	yq e 'true' "$file" > /dev/null
done

print_blue "Validating kustomize overlays"
find . -type f -name $kustomize_config -print0 | while IFS= read -r -d $'\0' file;
do
	print_blue "Validating kustomization ${file/%$kustomize_config}"
	kustomize build "${file/%$kustomize_config}" "${kustomize_flags[@]}" | \
	  kubeconform "${kubeconform_flags[@]}" "${kubeconform_config[@]}"
	if [[ ${PIPESTATUS[0]} != 0 ]]; then
	  exit 1
	fi
done
