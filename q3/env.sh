#!/usr/bin/env bash
#
# env.sh: Minimal script to install required Python libraries for your project.

echo "Installing required Python libraries..." 
pip install python-igraph numpy pandas scikit-learn

echo "Done! All required libraries should now be installed."
