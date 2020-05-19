## 问题描述
模拟通过学校的身份认证系统登录学校应用，前后要进行三次请求。参数正常，请求头完全模仿浏览器，浏览器可以正常登录，但是脚本第三次请求服务器却毫无响应，猜测学校对爬虫进行了限制，手段为在服务端对请求进行筛查。进而猜测可能是脚本第三次请求时cookie不对所致。（之前我的脚本可用，但是前两天突然不行了）


**问题:如果用浏览器登录，第三次请求时请求头的cookie的sessionid与第一次请求服务器响应头中set cookie的完全不同，且找不到它是怎么来的，想问这是为什么，有什么办法可以找到第三次的cookie是谁set的？（第二次响应没有setcookie）**

## 猜测


## 请求过程


#### ——第一次请求 获取cookie-——
get `https://iaaa.pku.edu.cn/iaaa/oauth.jsp?appID=portal2017&appName=%E5%8C%97%E4%BA%AC%E5%A4%A7%E5%AD%A6%E6%A0%A1%E5%86%85%E4%BF%A1%E6%81%AF%E9%97%A8%E6%88%B7%E6%96%B0%E7%89%88&redirectUrl=https://portal.pku.edu.cn/portal2017/ssoLogin.do`

请求头=`{'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'max-age=0', 'Connection': 'keep-alive', 'Host': 'iaaa.pku.edu.cn', 'Referer': 'https://portal.pku.edu.cn/portal2017/', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'same-site', 'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}`

响应头=`{'Server': 'nginx', 'Date': 'Tue, 19 May 2020 00:02:53 GMT', 'Content-Type': 'text/html; charset=UTF-8', 'Transfer-Encoding': 'chunked', 'Connection': 'keep-alive', 'Keep-Alive': 'timeout=60', 'Vary': 'Accept-Encoding', 'Cache-Control': 'max-age=86400', 'Set-Cookie': 'JSESSIONID=9jpNpDvNGfWBl8sN1JLBvCTM2NsVSG5ZJnyvzdf19y21Wbv6fXYZ!969989034; path=/', 'X-Powered-By': 'Servlet/2.5 JSP/2.1', 'Expires': 'Wed, 20 May 2020 00:02:53 GMT', 'Content-Encoding': 'gzip'}`

#### ——第二次请求 拿第一次获取的cookie请求，post密码换token——
post  `https://iaaa.pku.edu.cn/iaaa/oauthlogin.do`外加密码用户名等数据

请求头=`{‘Host': 'iaaa.pku.edu.cn', 'Connection': 'keep-alive', 'Content-Length': '155', 'Accept': 'application/json, text/javascript, */*; q=0.01', 'X-Requested-With': 'XMLHttpRequest',  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Origin': 'https://iaaa.pku.edu.cn', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Dest': 'empty', 'Cookie’:第一个请求头中的setcookie, 'Referer': 'https://iaaa.pku.edu.cn/iaaa/oauth.jsp?appID=portal2017&appName=%E5%8C%97%E4%BA%AC%E5%A4%A7%E5%AD%A6%E6%A0%A1%E5%86%85%E4%BF%A1%E6%81%AF%E9%97%A8%E6%88%B7%E6%96%B0%E7%89%88&redirectUrl=https://portal.pku.edu.cn/portal2017/ssoLogin.do', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US,en;q=0.9'}`

响应头=`{'Server': 'nginx', 'Date': 'Tue, 19 May 2020 00:02:53 GMT', 'Content-Type': 'text/html; charset=UTF-8', 'Transfer-Encoding': 'chunked', 'Connection': 'keep-alive', 'Keep-Alive': 'timeout=60', 'Vary': 'Accept-Encoding', 'X-Powered-By': 'Servlet/2.5 JSP/2.1', 'Expires': 'Wed, 20 May 2020 00:02:53 GMT', 'Cache-Control': 'max-age=86400', 'Content-Encoding': 'gzip'}`

响应内容=`{"success":true,"token”:”xxxxxxx”}`

#### ——第三次请求 拿token换cookie，从而进一步操作——
get `https://portal.pku.edu.cn/portal2017/ssoLogin.do?_rand=“+前端js脚本生成的随机数+"&token=" + 第二次响应的token`

请求头（参考浏览器中的）=`{'Host': 'portal.pku.edu.cn', 'Connection': 'keep-alive', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Sec-Fetch-Site': 'same-site', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-User': '?1', 'Sec-Fetch-Dest': 'document', 'Referer': 'https://iaaa.pku.edu.cn/iaaa/oauth.jsp?appID=portal2017&appName=%E5%8C%97%E4%BA%AC%E5%A4%A7%E5%AD%A6%E6%A0%A1%E5%86%85%E4%BF%A1%E6%81%AF%E9%97%A8%E6%88%B7%E6%96%B0%E7%89%88&redirectUrl=https://portal.pku.edu.cn/portal2017/ssoLogin.do', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US,en;q=0.9','cookie':与前两次不同}`

请求头中好像有cookie参数（jsesionid），但是cookie的值与之前的不同，不知道是从哪生成的

第三次请求服务器没响应

