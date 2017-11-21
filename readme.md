# Usage

    docker run -v `pwd`:/work klamar/compress
    docker run -v `pwd`:/work klamar/compress --verbose

The compressor inside the docker image is compressing everything in the **/work** directory. So mount the directory you want to run the compressor against into the /work directory.

## Command line flags

* **-v|--verbose** Enable debug output
* **-h|--help** Shows some help information
* **--follow-symlinks** follows symbolic links (default=no follow)
* **--no-png** Skip png optimization
* **--no-gzip** Skip gzip compression
* **--no-brotli** Skip brotli compression

## Compressions perfomed

### gzip

Every file will get a gzip counterpart compressed with highest compression level (gzip -9)

    foo.css -> foo.css.gz

### brotli

Every file will get a brotli counterpart compressed with highest compression level (brotli --quality 11)

    foo.css -> foo.css.br

### png

PNG files are getting optimized using optipng with optimization level 5.

    foo.png -> foo.png.orig (original)
    foo.png (optimized using optipng)

