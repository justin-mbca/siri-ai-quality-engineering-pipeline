#!/bin/bash

# Uninstall Spark 4.x (if installed via Homebrew)
brew list apache-spark &>/dev/null && brew uninstall apache-spark

# Download Spark 3.4.2
echo "Downloading Spark 3.4.2..."
curl -O https://archive.apache.org/dist/spark/spark-3.4.2/spark-3.4.2-bin-hadoop3.tgz

# Extract Spark
mkdir -p ~/opt
tar -xzf spark-3.4.2-bin-hadoop3.tgz -C ~/opt/

# Set environment variables in ~/.bash_profile
if ! grep -q "SPARK_HOME=~/opt/spark-3.4.2-bin-hadoop3" ~/.bash_profile; then
  echo 'export SPARK_HOME=~/opt/spark-3.4.2-bin-hadoop3' >> ~/.bash_profile
  echo 'export PATH=$SPARK_HOME/bin:$PATH' >> ~/.bash_profile
fi

# Reload shell
source ~/.bash_profile

# Verify Spark version
spark-submit --version

echo "Spark 3.4.2 setup complete. You can now run:"
echo "spark-submit --jars ~/Downloads/iceberg-spark-runtime-3.4_2.12-1.5.0.jar src/deliver.py"
