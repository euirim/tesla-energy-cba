docker build -t cs25050 .
docker run -v $(pwd)/code:/root -it -p 8888:8888 cs25050 jupyter notebook --no-browser --ip=0.0.0.0 --allow-root --NotebookApp.token= --notebook-dir='/root'
