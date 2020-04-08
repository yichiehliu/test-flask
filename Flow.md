Part 1
正常功能
Model --> CreateDB --> Add New Cars to carlist and carstatus
QueryRequest --> OrderConfirm

其他功能
Revise car storage/ car status
cancel order

Stage 1
2 tables
1.OrderRecord
2.CarStatus(date,location,carType)
Stage 2
3 tables 3. Realtime order management(assign carID)

Part 2
Query for cars(with condition date, location, cartype)

---

During the date period
for all location
for all cartype
return cartypelist

---

Part 3
Carstatus

# sid 自動增加

# 先創 DB, 增加車, 才進 flak_register

## Flask --> Model --> createDB --> AddnewCar

# 架構先後
