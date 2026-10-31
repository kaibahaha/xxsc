# R15 F5｜独立Python复算证据（2026-11-01）
## 范围
读取WorkBuddy报告§④完整源码逻辑，在独立Python执行环境以同样冻结参数生成确定性WAV/SRT；对报告中的validate()函数按原逻辑直接重放5既定负例及4个相邻负例。未登录远端、不读取远端/tmp；不能证明远端文件真实性或商用TTS/视频。
## 冻结输入与结果
SR=8000, DUR=8.0, FREQ=440.0, AMP=int(0.3*32767), PCM16 mono；两个字幕cue为0–4秒、4–8秒，文本与报告一致。
独立生成：
- WAV size=**128044** SHA256=**d5e639d3ee20c29cde0e710b7f9df9f77fb9f825fe9705009895385f2c6fac76**（匹配远端报告）。
- SRT size=**159** SHA256=**8c477ec992ccb9f3829cb8d0dd44d766bdad9025e053717ca8a2d3854adde5d4**（匹配远端报告）。
- 直接函数负例：no_auth (False,authorization missing,4); neg_time (False,negative timestamp,3); bad_dur (False,illegal/zero duration,2); empty_sub (False,empty subtitle,5); oob_index (False,cue index out of bounds,6)；5/5拒绝。
- 新增独立相邻输入：auth_string_false=**(True,accepted,0)**；timestamp_beyond_audio(end=8000, WAV duration=8)=**(True,accepted,0)**；NaN_start=**(True,accepted,0)**；NaN_end=**(True,accepted,0)**。**4/4 fail-open**。
## 根因与整改验收
1. validate()用 `if not c.authorized`，对字符串"false"及整数1都放行。需严格类型验证+不可伪造的授权证据；单个bool不能证明实际素材权利。
2. 未使用math.isfinite检查start/end，NaN比较为False导致绕过。
3. 未比较字幕结束时间与真实WAV时长，8000s字幕可通过8s音频门禁。
4. 当前MVE只验证内存Cue，未解析生成的SRT并核真实WAV长度；必须用解析器和真实音频时长做端到端边界测试。
## 独立复算限制
完整mve.py subprocess执行尝试在当前Python运行环境被60s自动中断，未得到该完整命令的独立exit/stdout；因此不能写“全脚本独立重放PASS”。本报告只声明**文件内容字节哈希与Cue逻辑独立复算**。运行环境为ChatGPT独立Python，标准库wave/struct/math/hashlib，未安装第三方包。源码全文和远端自述日志位于同轮WORKBUDDY_REPORT.md §④；此处记录新增输入/观察，不篡改原始WorkBuddy报告。
## 新增最小回归测试规格
```python
# 预期：所有测试必须拒绝，不允许返回 (True,...,0)
cases = [
    Cue(0,0,8,"valid","false"),
    Cue(0,0,8000,"valid",True),  # media_duration=8s
    Cue(0,float("nan"),8,"valid",True),
    Cue(0,0,float("nan"),"valid",True),
]
# 修复后需要显式：type(authorized) is bool、math.isfinite、end<=media_duration
```
