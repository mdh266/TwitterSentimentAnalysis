
# Creating & Connecting To The Hadoop Cluster
---------------------------------------------
Run

	source s1_create_cluster.sh 

Wait until the cluster has fully started.  Then create the ssh tunnel by running the command from same terminal:

	source s2_ssh_tunnel.sh

The program will continue to run in this terminal so you will have to open a new terminal.  Once you have a new terminal session run

	source s3_chrome_proxy.sh

This was set up to work on my Mac and should launch a Chrome session.  In that chrome session go to <code>http://mikescluster-m:8080</code> to access the notebook.  Note that YARN runs on <code>http://mikescluster-m:8088</code>.

Once your are ready to shut down the cluster run

	gcloud dataproc clusters delete mikescluster
	