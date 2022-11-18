export RAW_DIR=../Dataset/Raw

if [ ! -d $RAW_DIR ]; then
    mkdir $RAW_DIR
fi

curl -L https://sourcegraph.com/.api/src-cli/src_linux_amd64 -o src
chmod +x src

src search -json "/import mlflow|from mlflow.* import |library\(mlflow\)|import org\.mlflow.*;/ case:yes count:all select:repo" > "$RAW_DIR/MLflow.json"
src search -json "file:dvc\.y(a)?ml or /import dvc|from dvc.* import / case:yes count:all select:repo" > "$RAW_DIR/DVC.json"
src search -json "/import clearml|from clearml.* import / case:yes count:all select:repo" > "$RAW_DIR/ClearML.json"
src search -json "/import python_pachyderm|from python_pachyderm.* import |require ('pachyderm'|"pachyderm")|import .* from ("@pachyderm\/node-pachyderm"|'@pachyderm\/node-pachyderm');|require\(("@pachyderm\/node-pachyderm"|'@pachyderm\/node-pachyderm')\);/ case:yes count:all select:repo" > "$RAW_DIR/Pachyderm.json"
src search -json "/import lakefs_client|from lakefs_client.* import |import io\.lakefs\.clients\.api.*;/ case:yes count:all select:repo" > "$RAW_DIR/LakeFS.json"
src search -json "/import aim|from aim.* import / case:yes count:all select:repo" > "$RAW_DIR/Aim.json"
src search -json "/import sacred|from sacred.* import / case:yes count:all select:repo" > "$RAW_DIR/Sacred.json"
src search -json "/import guild|from guild.* import / case:yes count:all select:repo" > "$RAW_DIR/Guild AI.json"
src search -json "/import verta|from verta.* import / case:yes count:all select:repo" > "$RAW_DIR/ModelDB.json"
src search -json "/import polyaxon|from polyaxon.* import |"github\.com\/polyaxon\/sdks\/go\/http_client\/v1\/.*"|require\(('polyaxon-sdk'|"polyaxon-sdk")\);|require\(('@polyaxon\/sdk@1\.20\.0'|"@polyaxon\/sdk@1\.20\.0")\);|import .* from ('polyaxon-sdk'|"polyaxon-sdk");|import .* from ('@polyaxon\/sdk@1\.20\.0'|"@polyaxon\/sdk@1\.20\.0");|import org\.openapitools\.client.*;/ case:yes count:all select:repo" > "$RAW_DIR/Polyaxon.json"
src search -json "/import quilt3|from quilt3.* import / case:yes count:all select:repo" > "$RAW_DIR/Quilt.json"
src search -json "/import d6tflow|from d6tflow.* import / case:yes count:all select:repo" > "$RAW_DIR/D6tflow.json"
src search -json "/import deeplake|from deeplake.* import / case:yes count:all select:repo" > "$RAW_DIR/Deep Lake.json"
src search -json "/import keepsake|from keepsake.* import |"github\.com\/replicate\/keepsake\/go\/pkg\/.*"/ case:yes count:all select:repo" > "$RAW_DIR/Keepsake.json"
src search -json "/import determined|from determined.* import / case:yes count:all select:repo" > "$RAW_DIR/Determined.json"
src search -json "/import codalab|from codalab.* import / case:yes count:all select:repo" > "$RAW_DIR/Codalab.json"
src search -json "/import wandb|from wandb.* import |import com\.wandb.*;/ case:yes count:all select:repo" > "$RAW_DIR/Weights & Biases.json"
src search -json "/import neptune|from neptune.* import |library\(neptune\)/ case:yes count:all select:repo" > "$RAW_DIR/Neptune.json"
src search -json "/import sagemaker|from sagemaker.* import |#include <aws\/sagemaker.*\.h>|"github.com\/aws\/aws-sdk-go\/.*"|import software\.amazon\.awssdk.*;|require\(("@aws-sdk\/client-sagemaker"|'@aws-sdk\/client-sagemaker')\);|import .* from ("@aws-sdk\/client-sagemaker"|'@aws-sdk\/client-sagemaker');|namespace Aws\\SageMaker|require_relative ('aws-sdk-sagemaker\/.*'|"aws-sdk-sagemaker\/.*")|using Amazon\.SageMaker.*;/ case:yes count:all select:repo" > "$RAW_DIR/Amazon SageMaker.json"
src search -json "/import azureml\.core|from azureml\.core.* import / case:yes count:all select:repo" > "$RAW_DIR/Azure Machine Learning.json"
src search -json "file:domino\.y(a)?ml or /import domino|from domino.* import |library\(domino\)/ case:yes count:all select:repo" > "$RAW_DIR/Domino.json"
src search -json "file:valohai\.y(a)?ml or /import valohai_yaml|from valohai_yaml.* import / case:yes count:all select:repo" > "$RAW_DIR/Valohai.json"
src search -json "/import comet_m(l|pm)|from comet_m(l|pm).* import |import ml\.comet\.experiment.*;|library\(cometr\)/ case:yes count:all select:repo" > "$RAW_DIR/Comet.json"
src search -json "/import spell|from spell.* import / case:yes count:all select:repo" > "$RAW_DIR/Spell.json"
src search -json "/import google\.cloud\.aiplatform|from google\.cloud import aiplatform|import com\.google\.cloud\.aiplatform.*;|require\(("@google-cloud\/aiplatform"|'@google-cloud\/aiplatform')\);|import .* from ("@google-cloud\/aiplatform"|'@google-cloud\/aiplatform');/ case:yes count:all select:repo" > "$RAW_DIR/Vertex AI.json"
src search -json "/from databricks\.feature_store import FeatureStoreClient/ case:yes count:all select:repo" > "$RAW_DIR/Databricks.json"
