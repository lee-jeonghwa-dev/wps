# Install Program
## for dev
```
pip install -r requirements.txt
```
## for production
```
pip install -r requirements_production.txt
```

### 추가로 할 일
- .secrets폴더를 app과 같은 level에 만들어서 , DB, AWS 관련 정보를 지정해 주어야함
- base.json, dev.json, production.json 3개의 파일이 필요
1. base.json


`{
  "SECRET_KEY" : <Django Secret key>
}`

2. dev.json

`
{
 "DATABASE": {
   "default": {
       "ENGINE": <content>,
       "HOST": <content>,
       "NAME": <content>,
       "USER": <content>,
       "PASSWORD": <content>,
       "PORT": <content>
   }
 },
  "AWS_ACCESS_KEY_ID": <content>,
  "AWS_SECRET_ACCESS_KEY": <content>,
  "AWS_STORAGE_BUCKET_NAME": <content>
}
`

3. production.json

`
{
 "DATABASE": {
   "default": {
       "ENGINE": <content>,
       "HOST": <content>,
       "NAME": <content>,
       "USER": <content>,
       "PASSWORD": <content>,
       "PORT": <content>
   }
 },
  "AWS_ACCESS_KEY_ID": <content>,
  "AWS_SECRET_ACCESS_KEY": <content>,
  "AWS_STORAGE_BUCKET_NAME": <content>
}
`

# API document
https://baeminchan-project.gitbook.io/project/

# Git Repository
https://github.com/lee-jeonghwa-dev/wps

(forked from https://github.com/ElegantSiblings/wps)


