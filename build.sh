docker stop xiaov2.0
docker rm xiaov2.0
docker rmi $(docker images septnn/xiaov:2.0 -q)
docker build -t septnn/xiaov:2.0 .
docker run --name xiaov2.0 -itd \
-p 8140-8150:8140-8150 \
--cap-add=SYS_PTRACE \
--dns=114.114.114.114 \
-v /c/Users/JWD/Documents/git/github/septnn/xiaov:/home/app/ \
septnn/xiaov:2.0
