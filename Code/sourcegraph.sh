export RAW_DIR=../Dataset/Raw

if [ ! -d $RAW_DIR ]; then
    mkdir $RAW_DIR
fi

#curl -L https://sourcegraph.com/.api/src-cli/src_linux_amd64 -o src
#chmod +x src

src search -json "context:global /import sagemaker|from sagemaker.* import |#include <aws\/sagemaker.*\.h>|\"github\.com\/aws\/aws-sdk-go\/service\/sagemaker\"|package com\.amazonaws\.services\.sagemaker.*;|using Amazon\.SageMaker.*;|namespace Aws\\SageMaker\.*;|import .* from (\"@aws-sdk\/client-sagemaker\"|'@aws-sdk\/client-sagemaker');|require\((\"@aws-sdk\/client-sagemaker\"|'@aws-sdk\/client-sagemaker')\);|require_relative ('aws-sdk-sagemaker\/.*'|\"aws-sdk-sagemaker\/.*\")/ select:repo count:all patternType:standard case:yes" >"$RAW_DIR/Amazon SageMaker.json"
src search -json "context:global /import sigopt\.Connection|library\(SigOptR\)|import com\.sigopt.*;|from sigopt.* import |import sigopt|https:\/\/api\.sigopt\.com\/v1\/experiments/ count:all select:repo patternType:standard case:yes" >"$RAW_DIR/SigOpt.json"
src search -json "context:global /import mlflow|from mlflow.* import |library\(mlflow\)|import org\.mlflow.*;/ count:all select:repo patternType:standard case:yes" >"$RAW_DIR/MLflow.json"
src search -json "context:global file:dvc\.y(a)?ml or /import dvc|from dvc.* import / count:all select:repo patternType:standard case:yes" >"$RAW_DIR/DVC.json"
src search -json "context:global /import clearml|from clearml.* import / count:all select:repo patternType:standard case:yes" >"$RAW_DIR/ClearML.json"
src search -json "context:global /import python_pachyderm|from python_pachyderm.* import |require ('pachyderm'|\"pachyderm\")|import .* from (\"@pachyderm\/node-pachyderm\"|'@pachyderm\/node-pachyderm');|require\((\"@pachyderm\/node-pachyderm\"|'@pachyderm\/node-pachyderm')\);/ count:all select:repo patternType:standard case:yes" >"$RAW_DIR/Pachyderm.json"
src search -json "context:global /import lakefs_client|from lakefs_client.* import |import io\.lakefs\.clients\.api.*;/ count:all select:repo patternType:standard case:yes" >"$RAW_DIR/LakeFS.json"
src search -json "context:global /import aim|from aim.* import / count:all select:repo patternType:standard case:yes" >"$RAW_DIR/Aim.json"
src search -json "context:global /import sacred|from sacred.* import / count:all select:repo patternType:standard case:yes" >"$RAW_DIR/Sacred.json"
src search -json "context:global /import guild|from guild.* import / count:all select:repo patternType:standard case:yes" >"$RAW_DIR/Guild AI.json"
src search -json "context:global /import verta|from verta.* import / count:all select:repo patternType:standard case:yes" >"$RAW_DIR/ModelDB.json"
src search -json "context:global /import polyaxon|from polyaxon.* import |\"github\.com\/polyaxon\/sdks\/go\/http_client\/v1\/.*\"|require\(('polyaxon-sdk'|\"polyaxon-sdk\")\);|require\(('@polyaxon\/sdk@1\.20\.0'|\"@polyaxon\/sdk@1\.20\.0\")\);|import .* from ('polyaxon-sdk'|\"polyaxon-sdk\");|import .* from ('@polyaxon\/sdk@1\.20\.0'|\"@polyaxon\/sdk@1\.20\.0\");/ count:all select:repo patternType:standard case:yes" >"$RAW_DIR/Polyaxon.json"
src search -json "context:global /import quilt3|from quilt3.* import / count:all select:repo patternType:standard case:yes" >"$RAW_DIR/Quilt.json"
src search -json "context:global /import d6tflow|from d6tflow.* import / count:all select:repo patternType:standard case:yes" >"$RAW_DIR/D6tflow.json"
src search -json "context:global /import deeplake|from deeplake.* import / count:all select:repo patternType:standard case:yes" >"$RAW_DIR/Deep Lake.json"
src search -json "context:global /import keepsake|from keepsake.* import |\"github\.com\/replicate\/keepsake\/go\/pkg\/.*\"/ count:all select:repo patternType:standard case:yes" >"$RAW_DIR/Keepsake.json"
src search -json "context:global /import determined|from determined.* import / count:all select:repo patternType:standard case:yes" >"$RAW_DIR/Determined.json"
src search -json "context:global /import codalab|from codalab.* import / count:all select:repo patternType:standard case:yes" >"$RAW_DIR/Codalab.json"
src search -json "context:global /import wandb|from wandb.* import |import com\.wandb.*;/ count:all select:repo patternType:standard case:yes" >"$RAW_DIR/Weights & Biases.json"
src search -json "context:global /import neptune|from neptune.* import |library\(neptune\)/ count:all select:repo patternType:standard case:yes" >"$RAW_DIR/Neptune.json"
src search -json "context:global /import azureml\.core|from azureml\.core.* import / count:all select:repo patternType:standard case:yes" >"$RAW_DIR/Azure Machine Learning.json"
src search -json "context:global file:domino\.y(a)?ml or /import domino|from domino.* import |library\(domino\)/ count:all select:repo patternType:standard case:yes" >"$RAW_DIR/Domino.json"
src search -json "context:global file:valohai\.y(a)?ml or /import valohai_yaml|from valohai_yaml.* import / count:all select:repo patternType:standard case:yes" >"$RAW_DIR/Valohai.json"
src search -json "context:global /import comet_m(l|pm)|from comet_m(l|pm).* import |import ml\.comet\.experiment.*;|library\(cometr\)/ count:all select:repo patternType:standard case:yes" >"$RAW_DIR/Comet.json"
src search -json "context:global /import spell|from spell.* import / count:all select:repo patternType:standard case:yes" >"$RAW_DIR/Spell.json"
src search -json "context:global /import google\.cloud\.aiplatform|from google\.cloud import aiplatform|import com\.google\.cloud\.aiplatform.*;|require\((\"@google-cloud\/aiplatform\"|'@google-cloud\/aiplatform')\);|import .* from (\"@google-cloud\/aiplatform\"|'@google-cloud\/aiplatform');/ count:all select:repo patternType:standard case:yes" >"$RAW_DIR/Vertex AI.json"
src search -json "context:global /from databricks\.feature_store import FeatureStoreClient/ count:all select:repo patternType:standard case:yes" >"$RAW_DIR/Databricks.json"
