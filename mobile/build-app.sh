docker run --rm -it -v $PWD/mobile:/application -v $PWD/.cache:/root packsdkandroiddocker.image sh -c "bash scripts/compile-debug.sh"
