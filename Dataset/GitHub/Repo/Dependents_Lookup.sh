#! /bin/sh

export RAW_DIR="Raw"

if [ ! -d $RAW_DIR ]; then
    mkdir $RAW_DIR
fi

#curl -L https://sourcegraph.com/.api/src-cli/src_linux_amd64 -o src
#chmod +x src

#src search -json "context:global /import aim|from aim.* import / count:all select:repo patternType:standard case:yes" >"$RAW_DIR/Aim.json" # Aim
src search -json "context:global /import sagemaker|from sagemaker.* import |#include <aws\/sagemaker.*\.h>|\"github\.com\/aws\/aws-sdk-go\/service\/sagemaker\"|package com\.amazonaws\.services\.sagemaker.*;|using Amazon\.SageMaker.*;|namespace Aws\\SageMaker\.*;|import .* from (\"@aws-sdk\/client-sagemaker\"|'@aws-sdk\/client-sagemaker');|require\((\"@aws-sdk\/client-sagemaker\"|'@aws-sdk\/client-sagemaker')\);|require_relative ('aws-sdk-sagemaker\/.*'|\"aws-sdk-sagemaker\/.*\")/ select:repo count:all patternType:standard case:yes" >"$RAW_DIR/Amazon SageMaker.json" # Amazon SageMaker
src search -json "context:global /import azureml\.core|from azureml\.core.* import / count:all select:repo patternType:standard case:yes" >"$RAW_DIR/Azure Machine Learning.json"                                                                                                                                                                                                                                                                                                                                                                                                           # Azure Machine Learning
#src search -json "context:global /import clearml|from clearml.* import / count:all select:repo patternType:standard case:yes" >"$RAW_DIR/ClearML.json" # ClearML
#src search -json "context:global /import codalab|from codalab.* import / count:all select:repo patternType:standard case:yes" >"$RAW_DIR/Codalab.json" # Codalab
src search -json "context:global /from cnvrgv2 import / count:all select:repo patternType:standard case:yes" >"$RAW_DIR/cnvrg.io.json"                                                                             # cnvrg.io
src search -json "context:global /import comet_m(l|pm)|from comet_m(l|pm).* import |import ml\.comet\.experiment.*;|library\(cometr\)/ count:all select:repo patternType:standard case:yes" >"$RAW_DIR/Comet.json" # Comet
src search -json "context:global /import d6tflow|from d6tflow.* import / count:all select:repo patternType:standard case:yes" >"$RAW_DIR/D6tflow.json"                                                             # D6tflow
src search -json "context:global /import deeplake|from deeplake.* import / count:all select:repo patternType:standard case:yes" >"$RAW_DIR/Deep Lake.json"                                                         # Deep Lake
src search -json "context:global /import determined|from determined.* import / count:all select:repo patternType:standard case:yes" >"$RAW_DIR/Determined.json"                                                    # Determined
#src search -json "context:global file:domino\.y(a)?ml or /import domino|from domino.* import |library\(domino\)/ count:all select:repo patternType:standard case:yes" >"$RAW_DIR/Domino.json" # Domino
#src search -json "context:global file:dvc\.y(a)?ml or /import dvc|from dvc.* import / count:all select:repo patternType:standard case:yes" >"$RAW_DIR/DVC.json" # DVC
#src search -json "context:global /import guild|from guild.* import / count:all select:repo patternType:standard case:yes" >"$RAW_DIR/Guild AI.json" # Guild AI
src search -json "context:global /import keepsake|from keepsake.* import |\"github\.com\/replicate\/keepsake\/go\/pkg\/.*\"/ count:all select:repo patternType:standard case:yes" >"$RAW_DIR/Keepsake.json" # Keepsake
src search -json "context:global /import lakefs_client|from lakefs_client.* import |import io\.lakefs\.clients\.api.*;/ count:all select:repo patternType:standard case:yes" >"$RAW_DIR/LakeFS.json"        # LakeFS
src search -json "context:global /import mlflow|from mlflow.* import |library\(mlflow\)|import org\.mlflow.*;/ count:all select:repo patternType:standard case:yes" >"$RAW_DIR/MLflow.json"                 # MLflow
src search -json "context:global /import verta|from verta.* import / count:all select:repo patternType:standard case:yes" >"$RAW_DIR/ModelDB.json"                                                          # ModelDB
src search -json "context:global /import neptune|from neptune.* import |library\(neptune\)/ count:all select:repo patternType:standard case:yes" >"$RAW_DIR/Neptune.json"                                   # Neptune
#src search -json "context:global /import python_pachyderm|from python_pachyderm.* import |require ('pachyderm'|\"pachyderm\")|import .* from (\"@pachyderm\/node-pachyderm\"|'@pachyderm\/node-pachyderm');|require\((\"@pachyderm\/node-pachyderm\"|'@pachyderm\/node-pachyderm')\);/ count:all select:repo patternType:standard case:yes" >"$RAW_DIR/Pachyderm.json" # Pachyderm
src search -json "context:global /import polyaxon|from polyaxon.* import |\"github\.com\/polyaxon\/sdks\/go\/http_client\/v1\/.*\"|require\(('polyaxon-sdk'|\"polyaxon-sdk\")\);|require\(('@polyaxon\/sdk@1\.20\.0'|\"@polyaxon\/sdk@1\.20\.0\")\);|import .* from ('polyaxon-sdk'|\"polyaxon-sdk\");|import .* from ('@polyaxon\/sdk@1\.20\.0'|\"@polyaxon\/sdk@1\.20\.0\");/ count:all select:repo patternType:standard case:yes" >"$RAW_DIR/Polyaxon.json" # Polyaxon
#src search -json "context:global /import quilt3|from quilt3.* import / count:all select:repo patternType:standard case:yes" >"$RAW_DIR/Quilt.json" # Quilt
#src search -json "context:global /import sacred|from sacred.* import / count:all select:repo patternType:standard case:yes" >"$RAW_DIR/Sacred.json"                                                                                                                                                                                                                                   # Sacred
src search -json "context:global /import sigopt|from sigopt.* import |library\(SigOptR\)|import com\.sigopt.*;/ count:all select:repo patternType:standard case:yes" >"$RAW_DIR/SigOpt.json"                                                                                                                                                                                          # SigOpt
src search -json "context:global /import spell|from spell.* import / count:all select:repo patternType:standard case:yes" >"$RAW_DIR/Spell.json"                                                                                                                                                                                                                                      # Spell
src search -json "context:global file:valohai\.y(a)?ml or /import valohai_yaml|from valohai_yaml.* import / count:all select:repo patternType:standard case:yes" >"$RAW_DIR/Valohai.json"                                                                                                                                                                                             # Valohai
src search -json "context:global /import google\.cloud\.aiplatform|from google\.cloud import aiplatform|import com\.google\.cloud\.aiplatform.*;|require\((\"@google-cloud\/aiplatform\"|'@google-cloud\/aiplatform')\);|import .* from (\"@google-cloud\/aiplatform\"|'@google-cloud\/aiplatform');/ count:all select:repo patternType:standard case:yes" >"$RAW_DIR/Vertex AI.json" # Vertex AI
#src search -json "context:global /import wandb|from wandb.* import |import com\.wandb.*;/ count:all select:repo patternType:standard case:yes" >"$RAW_DIR/Weights & Biases.json" # Weights & Biases

github-dependents-info --repo aimhubio/aim -p -j >"$RAW_DIR/Aim.json"                   # Aim
github-dependents-info --repo allegroai/clearml -p -j >"$RAW_DIR/ClearML.json"          # ClearML
github-dependents-info --repo codalab/codalab-worksheets -p -j >"$RAW_DIR/Codalab.json" # Codalab
github-dependents-info --repo dominodatalab/python-domino -p -j >"$RAW_DIR/Domino.json" # Domino
github-dependents-info --repo iterative/dvc -p -j >"$RAW_DIR/DVC.json"                  # DVC
github-dependents-info --repo guildai/guildai -p -j >"$RAW_DIR/Guild AI.json"           # Guild AI
github-dependents-info --repo pachyderm/pachyderm -p -j >"$RAW_DIR/Pachyderm.json"      # Pachyderm
github-dependents-info --repo quiltdata/quilt -p -j >"$RAW_DIR/Quilt.json"              # Quilt
github-dependents-info --repo IDSIA/sacred -p -j >"$RAW_DIR/Sacred.json"                # Sacred
github-dependents-info --repo wandb/wandb -p -j >"$RAW_DIR/Weights & Biases.json"       # Weights & Biases
