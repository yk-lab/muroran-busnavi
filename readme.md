## python モジュールの update
```bash:確認
$ docker run -it --rm --volume $PWD:/app kennethreitz/pipenv pipenv update --outdated
```

```bash:更新
$ docker run -it --rm --volume $PWD:/app kennethreitz/pipenv pipenv update [names]
```
