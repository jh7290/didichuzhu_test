# Linux / 日志常用命令

```bash
pwd
ls
cd /path/to/project
grep "order_id=1001" app.log
tail -f app.log
ps -ef | grep python
curl http://127.0.0.1:8000/health
```

## 面试表达

如果接口返回 500，我会先复现问题，再看请求参数和响应内容。如果有服务日志，我会用 grep 搜索订单号或错误关键字，用 tail -f 查看实时日志，再结合数据库订单状态判断问题位置。
