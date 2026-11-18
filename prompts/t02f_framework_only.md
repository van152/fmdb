# t02-f:只做行框架(5 分钟任务)

> 交给 pi devseek。**任务极小:只恢复行框架,不做字段。**
> 规则:只读输入、不启动游戏/编辑器/IDA、不 pip install、`py -V:3.12 -I`。

## 唯一目标

给定 type-id,恢复 `<archive>/table_<TID>.dat` 的**行框架**:
- payload 头 `03 01 74 61 64 2e f1 0d`,count 在 payload+8(u32le)
- 行起、stride(定长)或变长公式
- **closure 必须成立**:client `14 + count*stride + 8 == payload_len`(server 用它的 stride)

## 铁律:第 1 步就落盘

立刻写 `<OUTDIR>/framework.json`:
```json
{"type_id": TID, "status": "in_progress", "client": null, "server": null}
```
每拿到一边(先 client,再 server)就重写一次。**全部完成后 status 改 "complete"。**

## 不要做的事

- 不要解字段、不要看反汇编、不要找 getter
- 不要写 helper 库、不要做全局设计
- 不要读 t01 的大文件(只读 `scratch/t01/inbox/t01h/output.json` 里 `type_id==TID` 的项即可,或干脆不读)

## 交付

`<OUTDIR>/framework.json`,字段:
```json
{
  "type_id": N, "status": "complete",
  "client": {"member": "client_db/table_N.dat", "count": ..., "stride": ..., "rows_offset": "0xe",
             "payload_len": ..., "closure": "14 + count*stride + 8 == payload_len"},
  "server": {...},
  "relation": "server[0:k]==client[0:k] 之类,若已核对就写,没核对写 null"
}
```

完成后打印一行:`DONE type=N client_stride=.. server_stride=..`
