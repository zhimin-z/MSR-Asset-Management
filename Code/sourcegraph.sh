export RAW_DIR=Dataset/Raw
export CODE_DIR=Code

mkdir $RAW_DIR

curl -L https://sourcegraph.com/.api/src-cli/src_linux_amd64 -o ./$CODE_DIR/src
chmod +x ./$CODE_DIR/src

./$CODE_DIR/src search -json "/import sagemaker|from sagemaker.* import / case:yes count:all" > "$RAW_DIR/Amazon SageMaker.json"
./$CODE_DIR/src search -json "/import mlflow|from mlflow.* import |library\(mlflow\)|mlflow run / case:yes count:all" > "$RAW_DIR/MLflow.json"
./$CODE_DIR/src search -json "/import dvc|from dvc.* import |dvc (exp )?init/ case:yes count:all" > "$RAW_DIR/DVC.json"
./$CODE_DIR/src search -json "/import wandb|from wandb.* import / case:yes count:all" > "$RAW_DIR/Weights & Biases.json"
./$CODE_DIR/src search -json "/import clearml|from clearml.* import / case:yes count:all" > "$RAW_DIR/ClearML.json"
./$CODE_DIR/src search -json "/import neptune|from neptune.* import / case:yes count:all" > "$RAW_DIR/Neptune.json"
./$CODE_DIR/src search -json "/import comet_ml|from comet_ml.* import " > "$RAW_DIR/Comet.json"
./$CODE_DIR/src search -json "/pachctl create repo / case:yes count:all" > "$RAW_DIR/Pachyderm.json"
./$CODE_DIR/src search -json "/import lakefs_client|from lakefs_client.* import|import io\.lakefs\.clients\.api\.|lakectl commit / case:yes count:all" > "$RAW_DIR/LakeFS.json"
./$CODE_DIR/src search -json "/import spell|from spell.* import |spell run / case:yes count:all" > "$RAW_DIR/Spell.json"
./$CODE_DIR/src search -json "/import aim|from aim.* import |aim init/ case:yes count:all" > "$RAW_DIR/Aim.json"
./$CODE_DIR/src search -json "/import sacred|from sacred.* import / case:yes count:all" > "$RAW_DIR/Sacred.json"
./$CODE_DIR/src search -json "/guild run / case:yes count:all" > "$RAW_DIR/Guild AI.json"
./$CODE_DIR/src search -json "/import verta|from verta.* import / case:yes count:all" > "$RAW_DIR/ModelDB.json"
./$CODE_DIR/src search -json "/import polyaxon|from polyaxon.* import |polyaxon project create / case:yes count:all" > "$RAW_DIR/Polyaxon.json"
./$CODE_DIR/src search -json "/import quilt3|from quilt3.* import / case:yes count:all" > "$RAW_DIR/Quilt.json"
./$CODE_DIR/src search -json "/import mlflow|import d6tflow|from d6tflow.* import / case:yes count:all" > "$RAW_DIR/D6tflow.json"
./$CODE_DIR/src search -json "/import deeplake|from deeplake.* import / case:yes count:all" > "$RAW_DIR/Deep Lake.json"
./$CODE_DIR/src search -json "/import keepsake|from keepsake.* import " > "$RAW_DIR/Keepsake.json"
./$CODE_DIR/src search -json "/cl run / case:yes count:all" > "$RAW_DIR/Codalab.json"
./$CODE_DIR/src search -json "/det experiment create / case:yes count:all" > "$RAW_DIR/Determined.json"
