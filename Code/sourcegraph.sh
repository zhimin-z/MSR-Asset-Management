export RAW_DIR=../Dataset/Raw

if [ ! -d $RAW_DIR ]; then
    mkdir $RAW_DIR
fi

curl -L https://sourcegraph.com/.api/src-cli/src_linux_amd64 -o src
chmod +x src

src search -json "/import sagemaker|from sagemaker.* import / case:yes count:all select:repo" > "$RAW_DIR/Amazon SageMaker.json"
src search -json "/import mlflow|from mlflow.* import |library\(mlflow\)|mlflow run / case:yes count:all select:repo" > "$RAW_DIR/MLflow.json"
src search -json "/import dvc|from dvc.* import |dvc (exp )?init/ case:yes count:all select:repo" > "$RAW_DIR/DVC.json"
src search -json "/import wandb|from wandb.* import / case:yes count:all select:repo" > "$RAW_DIR/Weights & Biases.json"
src search -json "/import clearml|from clearml.* import / case:yes count:all select:repo" > "$RAW_DIR/ClearML.json"
src search -json "/import neptune|from neptune.* import / case:yes count:all select:repo" > "$RAW_DIR/Neptune.json"
src search -json "/import comet_ml|from comet_ml.* import / case:yes count:all select:repo" > "$RAW_DIR/Comet.json"
src search -json "/import python_pachyderm|from python_pachyderm.* import |pachctl create repo / case:yes count:all select:repo" > "$RAW_DIR/Pachyderm.json"
src search -json "/import lakefs_client|from lakefs_client.* import|import io\.lakefs\.clients\.api\.|lakectl commit / case:yes count:all select:repo" > "$RAW_DIR/LakeFS.json"
src search -json "/import spell|from spell.* import |spell run / case:yes count:all select:repo" > "$RAW_DIR/Spell.json"
src search -json "/import aim|from aim.* import |aim init/ case:yes count:all select:repo" > "$RAW_DIR/Aim.json"
src search -json "/import sacred|from sacred.* import / case:yes count:all select:repo" > "$RAW_DIR/Sacred.json"
src search -json "/import guild|from guild.* import |guild run / case:yes count:all select:repo" > "$RAW_DIR/Guild AI.json"
src search -json "/import verta|from verta.* import / case:yes count:all select:repo" > "$RAW_DIR/ModelDB.json"
src search -json "/import polyaxon|from polyaxon.* import |polyaxon project create / case:yes count:all select:repo" > "$RAW_DIR/Polyaxon.json"
src search -json "/import quilt3|from quilt3.* import / case:yes count:all select:repo" > "$RAW_DIR/Quilt.json"
src search -json "/import d6tflow|from d6tflow.* import / case:yes count:all select:repo" > "$RAW_DIR/D6tflow.json"
src search -json "/import deeplake|from deeplake.* import / case:yes count:all select:repo" > "$RAW_DIR/Deep Lake.json"
src search -json "/import keepsake|from keepsake.* import / case:yes count:all select:repo" > "$RAW_DIR/Keepsake.json"
src search -json "/import codalab|from codalab.* import |cl run / case:yes count:all select:repo" > "$RAW_DIR/Codalab.json"
src search -json "/import determined|from determined.* import |det experiment create / case:yes count:all select:repo" > "$RAW_DIR/Determined.json"
