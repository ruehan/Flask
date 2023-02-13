
# Keticloud API Document
### Version : 1.0.2
### Last Update : 2022-12-09
---


## **SignUp User**
### **사용자 회원가입을 위한 API**
- URL : /auth/sign_up
- Method : POST
- Content-Type : application/json
- URL Params  
    ***Required :***  
        - **username** = [string] : 사용자 아이디  
        - **nickname** = [string] : 화면에서 보여지는 이름 (유저 아이디와 일치시켜도 됨)  
        - **password** = [string] : 사용자 패스워드  
        - **email** = [string] : 사용자 이메일  
        - **gender** = [integer] : 사용자 성별 (남 - 0, 여 - 1)  
        - **height** = [float] : 사용자 신장(키)  
        - **datetimes** = [integer] : 사용자 생년월일 (unixtimestamp)
        
- Success Resoponse :  
  
    |||  
    |-------------|----------------------------|     
    | Code        | 200                        |   
    | Content     | { msg : Already exist. }   |  
    | Description | 사용자 아이디가 이미 존재하는 경우. |  

    |||  
    |-------------|---------------------------|     
    | Code        | 200                       |   
    | Content     | { msg : Signup Success. } |  
    | Description | 사용자 등록에 성공한 경우.      |  
  
<br><br>

## **Check User**
### **사용자 아이디 및 닉네임 체크를 위한 API**
- URL : /auth/is_exist
- Method : POST
- Content-Type : application/json
- URL Params  
    ***Required :***  
        - **username** = [string] : 사용자 아이디  
        - **nickname** = [string] : 화면에서 보여지는 이름 

- Success Resoponse :  
  
    |||  
    |-------------|-------------------------------------------------------------|     
    | Code        | 200                                                         |   
    | Content     | { username : "Already exist.", nickname: "Already exist." } |  
    | Description | 사용자 아이디 또는 닉네임이 이미 존재하는 경우.                        |  

    |||  
    |-------------|-----------------------------------------------------|     
    | Code        | 200                                                 |   
    | Content     | { username : “Not exist.”, Nickname : “Not exist.” }|  
    | Description | 사용자 아이디 또는 닉네임이 존재하지 않는 경우.                |  
  
<br><br>

## **Check Stride**
### **사용자의 보폭 정보를 검색하는 API**
- URL : /dev/get_stride
- Method : POST
- Content-Type : application/json
- URL Params  
    ***Required :***  
        - **username** = [string] : 사용자 아이디  

- Success Resoponse :  
  
    |||  
    |-------------|----------------------------------------|     
    | Code        | 200                                    |   
    | Content     | { username : "user1", stride: "67.7" } |  
    | Description | 해당 사용자에 대한 보폭 데이터가 있는 경우.      |  

    |||  
    |-------------|---------------------------- |     
    | Code        | 200                         |   
    | Content     | { msg : “Not found user.” } |  
    | Description | 해당 사용자가 없는 경우          |  
  
<br><br>

## **Check Device**
### **Serial number를 전송하여 DB Server에 등록된 Device 인지 확인하고 등록이 되었으면 해당 Device에 대한 소유자와 사용자 정보를 반환한다.**
### **옵션값에 따라서 사용자의 일부 신상정보(나이, 키, 보폭)을 추가로 요청을 할 수 있다.**
- URL : /dev/check
- Method : POST
- Content-Type : application/json
- URL Params  
    ***Required :***  
        - **dev_type** = [string] : "aifit", "dumbbell", "wrist_band"  
        - **serial** = [integer] : BLE Mac Address의 뒤에서 4byte  
    ***Optional :***  
        - **user_req** = [Boolean] : DB에 등록된 Device의 사용자 일부 신상정보를 요청할 여부 (요청 안할 경우 해당 키가 없어도 됨)
        
- Success Resoponse :  
  
    |||  
    |-------------|-------------------------------------------------------------------------|     
    | Code        | 200                                                                     |   
    | Content     | { owner : "user1", user : "user2" }                                     |  
    | Description | owner는 device 소유자, user는 device 사용자이며, owner와 같을 수도 다를 수도 있음. |  

    |||   
    |-------------|-----------------------------------------------------------------------------------------|     
    | Code        | 200                                                                                     |   
    | Content     | { owner : "user1", user: "user2", age : 30, gender : 1, height : 175.2, stride : 60.5 } |  
    | Description | Data Params의 user_req 값이 True 인 경우                                                    |  

    |||   
    |-------------|----------------------------------|     
    | Code        | 200                              |   
    | Content     | { msg : null }                   |  
    | Description | DB에 등록된 owner나 user가 없을 경우. | 

- Error Resoponse :  
  
    |||  
    |-------------|-----------------------------------------------|     
    | Code        | 200                                           |   
    | Content     | { msg : "wrong json format" }                 |  
    | Description | Data params에서 필수요소가 잘못되었거나 누락되었을 경우. |  

    |||   
    |-------------|-----------------------------------------------------------------------------------------|     
    | Code        | 200                                                                                     |   
    | Content     | { msg : "There is no device" } |  
    | Description | Data Params의 dev_type이 DB에 없는 값인 경우                                                    |  

<br><br>

## **Register User**
### **소유자가 등록되지 않은 Serial number에 대해서 OTP 번호로 인증하여 소유자 등록. 만약 먼저 등록된 소유자가 있는 경우 거부 메시지를 반환**
- URL : /dev/check
- Method : POST
- Content-Type : application/json
- URL Params  
    ***Required :***  
        - **dev_type** = [string] : "aifit", "dumbbell", "wrist_band"  
        - **serial** = [integer] : BLE Mac Address의 뒤에서 4byte  
    ***Optional :***  
        - **user_req** = [Boolean] : DB에 등록된 Device의 사용자 일부 신상정보를 요청할 여부 (요청 안할 경우 해당 키가 없어도 됨)
        
- Success Resoponse :  
  
    |||  
    |-------------|-------------------------------------------------------------------------|     
    | Code        | 200                                                                     |   
    | Content     | { owner : "user1", user : "user2" }                                     |  
    | Description | owner는 device 소유자, user는 device 사용자이며, owner와 같을 수도 다를 수도 있음. |  

    |||   
    |-------------|-----------------------------------------------------------------------------------------|     
    | Code        | 200                                                                                     |   
    | Content     | { owner : "user1", user: "user2", age : 30, gender : 1, height : 175.2, stride : 60.5 } |  
    | Description | Data Params의 user_req 값이 True 인 경우                                                    |  

    |||   
    |-------------|----------------------------------|     
    | Code        | 200                              |   
    | Content     | { msg : null }                   |  
    | Description | DB에 등록된 owner나 user가 없을 경우. | 

- Error Resoponse :  
  
    |||  
    |-------------|-----------------------------------------------|     
    | Code        | 200                                           |   
    | Content     | { msg : "wrong json format" }                 |  
    | Description | Data params에서 필수요소가 잘못되었거나 누락되었을 경우. |  

    |||   
    |-------------|-----------------------------------------------------------------------------------------|     
    | Code        | 200                                                                                     |   
    | Content     | { msg : "There is no device" } |  
    | Description | Data Params의 dev_type이 DB에 없는 값인 경우                                                    |  

<br><br>

