API 说明文档

Answer:

* GET /api/answers/: 获取所有答案
* GET /api/answers/[pk]/: 获取id为pk的答案
* PUT /api/answers/[pk]/upload_image/:向id为pk的答案添加图片
* GET /api/answers/[pk]/agree_answer/:赞同答案
* GET /api/answers/[pk]/against_answer/:反对答案
* GET /api/answers/my_answers/:获取当前登陆用户的所有回答

Question:

* GET /api/questions/:获取所有问题
* GET /api/questions/[pk]/:获取id为pk的问题
* GET /api/questions/[pk]/add_search_times/:为id为pk的问题增加搜索次数
* GET /api/questions/my_questions/:获取当前用户的所有问题
* GET /api/questions/[pk]/get_answers/:获取id为pk的问题的所有答案
* GET /api/questions/[pk]/follow_questions/:为当前登陆用户关注id为pk的问题
* GET /api/questions/[pk]/cancel_follow/:为当前登陆用户取消关注此问题
* GET /api/questions/search/?title=xxx:搜索title为xxx的问题
* GET /api/questions/get_hot_question/:返回搜索次数排名前十的问题
* POST /api/questions/: 添加问题
* PUT /api/questions/[pk]/: 更新问题

Topic

* GET /api/topics/:获取所有话题
* GET /api/topics/[pk]/:获取id为pk的话题
* GET /api/topics/[pk]/follow_topic/: 为当前用户关注id为pk的话题
* GET /api/topics/[pk]/cancel_follow/:为当前用户取消关注id为pk的话题
* GET /api/topics/my_topics/:获取当前用户提出的所有话题
* GET /api/topics/[pk]/get_questions/:获取当前话题下的所有问题
* GET /api/topics/search/?title=xxx:搜索title为xxx的话题
* GET /api/topics/get_sel_topic/:获取添加问题时可以选择的话题
* GET /api/topics/get_hot_topic/:返回搜索次数排名前十的话题

Message

* GET /api/messages/:获取所有消息
* GET /api/messages/[pk]/: 获取id为pk的消息
* GET /api/messages/my_send_messsages/:获取所有当前用户发送过的消息
* GET /api/messages/my_receive_messages/:获取当前用户收到的所有消息

Userinfo

* PUT /api/userinfos/[pk]/upload_image/:为id为pk的用户上传头像
* GET /api/userinfos/[pk]/:获取id为pk的用户的信息
* GET /api/userinfos/[pk]/my_follow_topics/:获取id为pk的用户关注的话题
* GET /api/userinfos/[pk]/my_follow_questions/:获取id为pk的用户关注 的问题

User

* POST /api/login/: 登陆
* POST /api/login/: 注册

