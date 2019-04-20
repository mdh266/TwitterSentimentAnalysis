gcloud dataproc clusters create \
     --image-version=1.3 \
     --num-workers=2 \
     --scopes=cloud-platform \
     --worker-machine-type=n1-standard-2 \
     --master-machine-type=n1-standard-4 \
     --zone=us-central1-a \
     --metadata 'CONDA_PACKAGES="python==3.5"' \
     --metadata '^#^spark-packages=org.mongodb.spark:mongo-spark-connector_2.11:2.3.0' \
     --initialization-actions gs://mikesparkinitializer/sparkenvprep.sh,gs://mikesparkinitializer/datalab.sh \
     mikescluster
