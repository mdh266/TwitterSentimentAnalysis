#!/usr/bin/env bash

ROLE=$(/usr/share/google/get_metadata_value attributes/dataproc-role)


if [[ "${ROLE}" == 'Master' ]]; then
	CLONE_DIR=/datalab/
else
	CLONE_DIR=/tmp/
fi

mkdir -p $CLONE_DIR
cd $CLONE_DIR

sudo git clone https://github.com/mdh266/SentimentAnalysis.git

cd /tmp/

gsutil -m cp -r gs://dataproc-initialization-actions/conda/bootstrap-conda.sh .
gsutil -m cp -r gs://dataproc-initialization-actions/conda/install-conda-env.sh .


export MINICONDA_VERSION="4.2.12"

chmod 755 ./*conda*.sh

# Install Miniconda / conda
./bootstrap-conda.sh
# Create / Update conda environment via conda yaml
./install-conda-env.sh

if [[ -f /etc/profile.d/effective-python.sh ]]; then
    PROFILE_SCRIPT_PATH=/etc/profile.d/effective-python.sh
else
    PROFILE_SCRIPT_PATH=/etc/profile.d/conda.sh
fi
source $PROFILE_SCRIPT_PATH
conda activate base

pip install -r ${CLONE_DIR}SentimentAnalysis/requirements.txt
