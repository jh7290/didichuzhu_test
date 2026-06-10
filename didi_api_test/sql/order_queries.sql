-- 查询所有订单
select * from orders;

-- 查询某个用户的所有订单
select * from orders where user_id = 1001;

-- 查询已支付订单
select * from orders where status = 'paid';

-- 按订单状态统计数量
select status, count(*) from orders group by status;

-- 查询用户和订单关联信息
select
    u.id,
    u.phone,
    o.order_id,
    o.status,
    o.price
from users u
join orders o on u.id = o.user_id;

-- 查询某个时间段内创建的订单
select * from orders
where created_at >= '2026-06-01 00:00:00'
  and created_at < '2026-06-02 00:00:00';
