# 认证接口 (Authentication)

## 概述

认证接口用于用户登录、登出和更新密码。

## API 列表

| 函数名 | 描述 | 输入参数 | 输出参数 |
|--------|------|----------|----------|
| `login()` | 用户登录 | username, password, host, port | bool |
| `logout()` | 用户登出 | 无 | bool |
| `update_password()` | 更新密码 | old_password, new_password | bool |

---

## login

### 功能描述

用户登录到 AmazingData 金融数据服务。

### 函数签名

```python
ad.login(username: str, password: str, host: str, port: int) -> bool
```

### 输入参数

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `username` | str | 是 | 用户名 |
| `password` | str | 是 | 密码 |
| `host` | str | 是 | 服务器主机地址，例如 `***.***.***.***` |
| `port` | int | 是 | 服务器端口号 |

### 输出参数

| 类型 | 描述 |
|------|------|
| bool | 登录成功返回 True，失败返回 False |

### 使用示例

```python
import AmazingData as ad

# 登录
success = ad.login(
    username='your_username',
    password='your_password',
    host='192.168.1.100',
    port=8080
)

if success:
    print("登录成功")
else:
    print("登录失败")
```

---

## logout

### 功能描述

用户登出 AmazingData 金融数据服务。

### 函数签名

```python
ad.logout() -> bool
```

### 输入参数

无

### 输出参数

| 类型 | 描述 |
|------|------|
| bool | 登出成功返回 True，失败返回 False |

### 使用示例

```python
import AmazingData as ad

# 登出
success = ad.logout()
```

---

## update_password

### 功能描述

更新用户登录密码。

### 函数签名

```python
ad.update_password(old_password: str, new_password: str) -> bool
```

### 输入参数

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `old_password` | str | 是 | 旧密码 |
| `new_password` | str | 是 | 新密码 |

### 输出参数

| 类型 | 描述 |
|------|------|
| bool | 更新成功返回 True，失败返回 False |

### 使用示例

```python
import AmazingData as ad

# 先登录
ad.login(username='your_username', password='your_password', host='192.168.1.100', port=8080)

# 更新密码
success = ad.update_password('old_password', 'new_password')
```

---

## 注意事项

1. 所有数据接口调用前必须先登录
2. 登录信息在整个会话期间有效
3. 建议在使用完毕后调用 `logout()` 登出
