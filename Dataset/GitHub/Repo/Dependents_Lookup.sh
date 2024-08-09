#! /bin/sh

curl -L https://sourcegraph.com/.api/src-cli/src_linux_amd64 -o src
chmod +x src

src search -json "context:global /import sagemaker|from sagemaker.* import |#include <aws\/sagemaker.*\.h>|\"github\.com\/aws\/aws-sdk-go\/service\/sagemaker\"|package com\.amazonaws\.services\.sagemaker.*;|using Amazon\.SageMaker.*;|namespace Aws\\SageMaker\.*;|import .* from (\"@aws-sdk\/client-sagemaker\"|'@aws-sdk\/client-sagemaker');|require\((\"@aws-sdk\/client-sagemaker\"|'@aws-sdk\/client-sagemaker')\);|require_relative ('aws-sdk-sagemaker\/.*'|\"aws-sdk-sagemaker\/.*\")/ select:repo count:all patternType:standard case:yes" > "Amazon SageMaker.json" # Amazon SageMaker
src search -json "context:global /import azureml\.core|from azureml\.core.* import / count:all select:repo patternType:standard case:yes" > "Azure Machine Learning.json"                                                                                                                                                                                                                                                                                                                                                                                                           # Azure Machine Learning
src search -json "context:global /import cnvrgv2|from cnvrgv2.* import / count:all select:repo patternType:standard case:yes" > "cnvrg.io.json"                                                                                                                                                                                                                                                                                                                                                                                                                                     # cnvrg.io
src search -json "context:global /import comet_m(l|pm)|from comet_m(l|pm).* import |import ml\.comet\.experiment.*;|library\(cometr\)/ count:all select:repo patternType:standard case:yes" > "Comet.json"                                                                                                                                                                                                                                                                                                                                                                          # Comet
src search -json "context:global /import determined|from determined.* import / count:all select:repo patternType:standard case:yes" > "Determined.json"                                                                                                                                                                                                                                                                                                                                                                                                                             # Determined
src search -json "context:global /import mlflow|from mlflow.* import |library\(mlflow\)|import org\.mlflow.*;/ count:all select:repo patternType:standard case:yes" > "MLflow.json"                                                                                                                                                                                                                                                                                                                                                                                                 # MLflow
src search -json "context:global /import verta|from verta.* import / count:all select:repo patternType:standard case:yes" > "Verta.json"                                                                                                                                                                                                                                                                                                                                                                                                                                            # Verta
src search -json "context:global /import neptune|from neptune.* import |library\(neptune\)/ count:all select:repo patternType:standard case:yes" > "Neptune.json"                                                                                                                                                                                                                                                                                                                                                                                                                   # Neptune
src search -json "context:global /import polyaxon|from polyaxon.* import |\"github\.com\/polyaxon\/sdks\/go\/http_client\/v1\/.*\"|require\(('polyaxon-sdk'|\"polyaxon-sdk\")\);|require\(('@polyaxon\/sdk@1\.20\.0'|\"@polyaxon\/sdk@1\.20\.0\")\);|import .* from ('polyaxon-sdk'|\"polyaxon-sdk\");|import .* from ('@polyaxon\/sdk@1\.20\.0'|\"@polyaxon\/sdk@1\.20\.0\");/ count:all select:repo patternType:standard case:yes" > "Polyaxon.json"                                                                                                                              # Polyaxon
src search -json "context:global /import sigopt|from sigopt.* import |library\(SigOptR\)|import com\.sigopt.*;/ count:all select:repo patternType:standard case:yes" > "SigOpt.json"                                                                                                                                                                                                                                                                                                                                                                                                # SigOpt
src search -json "context:global file:valohai\.y(a)?ml or /import valohai_yaml|from valohai_yaml.* import / count:all select:repo patternType:standard case:yes" > "Valohai.json"                                                                                                                                                                                                                                                                                                                                                                                                   # Valohai
src search -json "context:global /import google\.cloud\.aiplatform|from google\.cloud import aiplatform|import com\.google\.cloud\.aiplatform.*;|require\((\"@google-cloud\/aiplatform\"|'@google-cloud\/aiplatform')\);|import .* from (\"@google-cloud\/aiplatform\"|'@google-cloud\/aiplatform');/ count:all select:repo patternType:standard case:yes" > "Vertex AI.json"                                                                                                                                                                                                       # Vertex AI

github-dependents-info --repo aimhubio/aim -p -j > "Aim.json"                   # Aim
github-dependents-info --repo allegroai/clearml -p -j > "ClearML.json"          # ClearML
github-dependents-info --repo codalab/codalab-worksheets -p -j > "Codalab.json" # Codalab
github-dependents-info --repo dominodatalab/python-domino -p -j > "Domino.json" # Domino
github-dependents-info --repo iterative/dvc -p -j > "DVC.json"                  # DVC
github-dependents-info --repo guildai/guildai -p -j > "Guild AI.json"           # Guild AI
github-dependents-info --repo kedro-org/kedro -p -j > "Kedro.json"              # Kedro
github-dependents-info --repo mlrun/mlrun -p -j > "MLRun.json"                  # MLRun
github-dependents-info --repo optuna/optuna -p -j > "Optuna.json"               # Optuna
github-dependents-info --repo IDSIA/sacred -p -j > "Sacred.json"                # Sacred
github-dependents-info --repo wandb/wandb -p -j > "Weights & Biases.json"       # Weights & Biases
