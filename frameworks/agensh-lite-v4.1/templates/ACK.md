# ACK 参考

- event_id: EV-UNIQUE
- recipient_agent: B
- ack_type: DELIVERY_ACK
- observed_at: ISO8601
- source_commit: REPLACE
- target_ref: REPLACE
- hash_verified: false
- business_accepted: false

Git 提交、Library 源件、Drive 目标是不同 ACK 作用域，不得共用一个 SUCCESS 字段。
