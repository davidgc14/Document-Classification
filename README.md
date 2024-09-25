# Document analysis

This is a simple example of an API Dockerized. It allows you to analyze documents using any model you want (and for any purpose).
Here I have used a simple example trained on films reviews (view the `model/training.py` file).

## How it works

Simply run `docker compose up` on the directory where you cloned the project. Then you are able to manage your containers.

The API is listening at http://localhost:5000/analysis on your machine.

To sent files, simply type on your terminal:

```
curl -X POST http://localhost:5000/analysis -F "file=@/path/to/your/file.pdf"
```

Currently only available for digital pdf's.
