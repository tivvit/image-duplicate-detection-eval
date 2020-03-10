# image-duplicate-detection-eval

More info in the [PDF](image_near_duplicate_detection_for_spam_detection_using_CNN.pdf)

# dataset
* Open Images Dataset V5
* https://github.com/cvdfoundation/open-images-dataset
* `aws s3 --no-sign-request cp s3://open-images-dataset/tar/train_0.tar.gz .`
* `tar -xzvf train_0.tar.gz -C data-all`
* `find data-all -maxdepth 1 -type f |head -1000|xargs cp -t data`
