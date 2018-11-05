## 1. 商品科学分类

## ****接口(添加)：
* desc: 新科学分类添加

* url: /m/basicdata/system_class/add

* method: post

* param:

    ```
    {
        "code": "A4",
        "title": "测试分类",
        "level": 1,
        "top_code": "",
        "rank": 1
    }
    ```

* return:

    success
    
    ```
    {
        "code": 0,
        "data": {
            "code": "A4",
            "created": "2018-09-11 11:07:58",
            "level": 1,
            "rank": 1,
            "remark": "",
            "title": "测试分类",
            "top_code": "",
            "updated": "2018-09-11 11:07:58"
        }
    }
    ```
    
    fail
    
    ```
    {
        "code": 100,
        "data": null,
        "massage": "已存在此科学分类信息" 
    }
    ```
    
    ```
    {
        "code": 100,
        "data": null,
        "massage": "此科学分类层级有误" 
    }
    ```
    
    ```
    {
        "code": 100,
        "data": null,
        "massage": "此科学分类父层信息有误" 
    }
    ```
    
## ****接口(修改)：
* desc: 新科学分类修改

* url: /m/basicdata/system_class/add

* method: post

* param:

    ```
    {
        "code": "A4",
        "title": "测试分类(名称修改)",
        "level": 1,
        "top_code": "",
        "rank": 1
    }
    ```
* return:
    
    success
    
    ```
    {
        "code": 0,
        "data": {
            "code": "A4",
            "created": "2018-09-11 11:07:58",
            "level": 1,
            "rank": 1,
            "remark": "",
            "title": "测试分类",
            "top_code": "",
            "updated": "2018-09-11 11:07:58"
        }
    }
    ```
    
    fail
    
    ```
    {
        "code": 100,
        "data": null,
        "massage": "不存在此科学分类信息" 
    }
    ```
    
    ```
    {
        "code": 100,
        "data": null,
        "massage": "修改后的科学分类层级信息有误" 
    }
    ```
    
    ```
    {
        "code": 100,
        "data": null,
        "massage": "修改后的科学分类父层信息有误" 
    }
    ```
    
## ****接口(列表)：
* desc: 新科学分类列表

* url: /m/basicdata/system_class/list

* method: get

* param:

* return:

  success
  
  ```
    {
        "code": 0,
        "data": {
            "code": "A4",
            "created": "2018-09-11 11:07:58",
            "level": 1,
            "rank": 1,
            "remark": "",
            "title": "测试分类",
            "top_code": "",
            "updated": "2018-09-11 11:07:58"
        }
    }
  ```


