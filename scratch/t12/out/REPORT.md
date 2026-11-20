# t12 形态完整 4CC 抽取报告

状态：`complete_with_club_coverage_gap`（平表与反汇编核验通过；club 覆盖验收未通过）。

## 扫描来源与规模

- editor.exe SHA-256：`b82ebe8e032f20171e813c02f53084dc0ac2c43bc8346beb742418efaadadab4`（只读）。
- 反序 ASCII 四字节搜寻后逐处 Capstone 回验：19,640 个 cmp；其中带条件分支 19,254，JE/JNE 形态 14,752；任务给定规模约 14,171。
- 输出 2,600 个有实例的 4CC，保留 4,278 条实例（每码最多 6）。

## 形态计数

| 形态 | 有该形态的码数 | 实例数 |
|---|---:|---:|
| `read` | 1244 | 1956 |
| `ref_ptr` | 516 | 791 |
| `write` | 127 | 164 |
| `path_descend` | 75 | 90 |
| `remote` | 1084 | 1277 |

## club 路径分类与覆盖

| 类别 | 码数 |
|---|---:|
| `offset` | 185 |
| `path` | 5 |
| `remote` | 76 |
| `absent` | 189 |
| `unresolved` | 120 |

- 按任务口径 `offset + path + remote`：**266/483 = 55.07%**；验收线 420/483，未达标。
- 本次对完整 exe 做严格反序字节重数：386 个码字节存在、189 个不存在；任务给定 E48 基线为 483/92，当前严格重数与之相差 -97。因此将“字节确实不存在”与“字节存在但形态未解”分开，未伪造 remote/offset，也未把后者写成 absent。
- `club_paths.json` 给 575 个 schema 码逐码记录 kind、置信度、证据指令/地址或未解析原因。由于严格字节重数与 E48 给定 483/92 冲突，不能将这次实测的 189 个 absent 静默改成 92。

## club 未定位码逐码归因

下表逐码列出所有未达到 offset/path/remote 的字段码。完整机器记录（含各 CMP 位置、分支类型、目标 VA）见 `club_paths.json -> codes`。

| code | 本次分类 | 字节存在 | cmp 位置 / 分支 | 归因 |
|---|---|---|---|---|
| `2sbc` | `unresolved` | 是 | 0xe89c6c jne | 分支块未发现五类形态之一的直接访问 |
| `2tbc` | `unresolved` | 是 | 0xe8c816 jne | 分支块未发现五类形态之一的直接访问 |
| `3scl` | `unresolved` | 是 | 0xe8bf90 jne | 分支块未发现五类形态之一的直接访问 |
| `3tcl` | `unresolved` | 是 | 0xe8ac73 jne | 分支块未发现五类形态之一的直接访问 |
| `CAAa` | `unresolved` | 是 | 0xe83586 jne; 0xe8a2a4 jne; 0xec1738 jne; 0xecb429 je | 分支块未发现五类形态之一的直接访问 |
| `CBDa` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CBDc` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CBDd` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CBDf` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CBDo` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CBWa` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CBWc` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CBWd` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CBWf` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CBWo` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CFGd` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CFGm` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CFGn` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CFGo` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CFGp` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CFGs` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CGLc` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CGLd` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CGLg` | `unresolved` | 是 | — | 反序字节存在，但没有解码成带分支的 cmp 4CC。 |
| `CGLn` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CGLo` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CGLp` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CGMc` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CGMd` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CGMg` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CGMn` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CGMo` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CGMp` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CHAa` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CHAc` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CHAd` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CHAo` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CHFd` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CHFf` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CHFn` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CHFp` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CHFs` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CHGc` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CHGg` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CHGn` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CHGp` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CHLa` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CHLc` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CHLd` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CHLf` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CHLo` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CHRb` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CHRd` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CHRf` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CHRn` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CHRp` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CHSa` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CHSc` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CHSd` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CHSf` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CHSo` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CIcl` | `unresolved` | 是 | 0xe838cd je; 0xe843b0 no-jcc; 0xe843cd no-jcc; 0xe8c18e jne | 分支块未发现五类形态之一的直接访问 |
| `CLAa` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CLAc` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CLAd` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CLAo` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CLRe` | `unresolved` | 是 | 0x11f13eb je; 0x11f4d18 je; 0x11f4d19 je | 分支块未发现五类形态之一的直接访问 |
| `CLRg` | `unresolved` | 是 | 0x11f13f7 jne; 0x11f4d25 je; 0x11f4d26 je | 分支块未发现五类形态之一的直接访问 |
| `CLRs` | `unresolved` | 是 | 0x11f29e7 jne; 0x11f4d32 jne; 0x11f4d33 jne | 分支块未发现五类形态之一的直接访问 |
| `CLon` | `unresolved` | 是 | 0xe8afc4 jne | 分支块未发现五类形态之一的直接访问 |
| `CMAp` | `unresolved` | 是 | 0xe8463d jne; 0xe8b88a jne; 0xec2d2f jne; 0xecb60a jne | 分支块未发现五类形态之一的直接访问 |
| `CMCd` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CMCn` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CMCp` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CMCs` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CMOp` | `unresolved` | 是 | 0xe83a3b jne; 0xe8b665 jne | 分支块未发现五类形态之一的直接访问 |
| `CNse` | `unresolved` | 是 | 0xe84263 jne | 分支块未发现五类形态之一的直接访问 |
| `COPc` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `COPd` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `COPm` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `COPn` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `COPo` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `COPp` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `COSc` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `COSd` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `COSm` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `COSn` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `COSo` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `COSp` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CWCe` | `unresolved` | 是 | 0x11f1332 je; 0x11f4bed je; 0x11f4bee je | 分支块未发现五类形态之一的直接访问 |
| `CWCg` | `unresolved` | 是 | 0x11f133e je; 0x11f4bfa jne; 0x11f4bfb jne | 分支块未发现五类形态之一的直接访问 |
| `CWCs` | `unresolved` | 是 | 0x11f134a jne; 0x11f4edf je; 0x11f4ee0 je | 分支块未发现五类形态之一的直接访问 |
| `CWLe` | `unresolved` | 是 | 0x11f0e02 je; 0x11f4eec jne; 0x11f4eed jne | 分支块未发现五类形态之一的直接访问 |
| `CWLg` | `unresolved` | 是 | 0x11f0e0e jne; 0x11f4de9 je; 0x11f4dea je | 分支块未发现五类形态之一的直接访问 |
| `CWLs` | `unresolved` | 是 | 0x11f1413 je; 0x11f4df6 jne; 0x11f4df7 jne | 分支块未发现五类形态之一的直接访问 |
| `CWRe` | `unresolved` | 是 | 0x11f141f jne; 0x11f4b59 je; 0x11f4b5a je | 分支块未发现五类形态之一的直接访问 |
| `CWRg` | `unresolved` | 是 | 0x11f1366 je; 0x11f4b66 je; 0x11f4b67 je | 分支块未发现五类形态之一的直接访问 |
| `CWRs` | `unresolved` | 是 | 0x11f1372 je; 0x11f4b73 jne; 0x11f4b74 jne | 分支块未发现五类形态之一的直接访问 |
| `CWSe` | `unresolved` | 是 | 0x11f137e jne; 0x11f49b5 je; 0x11f49b6 je | 分支块未发现五类形态之一的直接访问 |
| `CWSg` | `unresolved` | 是 | 0x11f0f84 je; 0x11f49c2 je; 0x11f49c3 je | 分支块未发现五类形态之一的直接访问 |
| `CWSs` | `unresolved` | 是 | 0x11f0f90 jne; 0x11f49cf jne; 0x11f49d0 jne | 分支块未发现五类形态之一的直接访问 |
| `CWWe` | `unresolved` | 是 | 0x11f143b je; 0x11f4d4f je; 0x11f4d50 je | 分支块未发现五类形态之一的直接访问 |
| `CWWg` | `unresolved` | 是 | 0x11f1447 jne; 0x11f4d5c je; 0x11f4d5d je | 分支块未发现五类形态之一的直接访问 |
| `CWWs` | `unresolved` | 是 | 0x11f18b9 jne; 0x11f4d69 jne; 0x11f4d6a jne | 分支块未发现五类形态之一的直接访问 |
| `CYPc` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CYPd` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CYPm` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CYPn` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CYPo` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CYPp` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CYSc` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CYSd` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CYSm` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CYSn` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CYSo` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CYSp` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `Ca3n` | `unresolved` | 是 | 0xe580b6 je; 0xe580b7 je; 0xe834a5 je; 0xe8b708 jne | 分支块未发现五类形态之一的直接访问 |
| `Camc` | `unresolved` | 是 | 0xe580c3 jne; 0xe580c4 jne; 0xe83922 je; 0xe8b4b1 jne | 分支块未发现五类形态之一的直接访问 |
| `Ccja` | `unresolved` | 是 | — | 反序字节存在，但没有解码成带分支的 cmp 4CC。 |
| `Ccjc` | `unresolved` | 是 | — | 反序字节存在，但没有解码成带分支的 cmp 4CC。 |
| `Ccjd` | `unresolved` | 是 | — | 反序字节存在，但没有解码成带分支的 cmp 4CC。 |
| `Ccjg` | `unresolved` | 是 | — | 反序字节存在，但没有解码成带分支的 cmp 4CC。 |
| `Ccjh` | `unresolved` | 是 | — | 反序字节存在，但没有解码成带分支的 cmp 4CC。 |
| `Ccji` | `unresolved` | 是 | — | 反序字节存在，但没有解码成带分支的 cmp 4CC。 |
| `Ccjm` | `unresolved` | 是 | — | 反序字节存在，但没有解码成带分支的 cmp 4CC。 |
| `Ccjp` | `unresolved` | 是 | — | 反序字节存在，但没有解码成带分支的 cmp 4CC。 |
| `Ccjs` | `unresolved` | 是 | — | 反序字节存在，但没有解码成带分支的 cmp 4CC。 |
| `Ccjt` | `unresolved` | 是 | — | 反序字节存在，但没有解码成带分支的 cmp 4CC。 |
| `Ccjy` | `unresolved` | 是 | — | 反序字节存在，但没有解码成带分支的 cmp 4CC。 |
| `Ccsb` | `unresolved` | 是 | 0xeeb9d8 jg; 0xeeb9f0 jne; 0xef0187 je | 边界比较；目标块与 fall-through 均不得归属本 4CC |
| `Ccsf` | `unresolved` | 是 | — | 反序字节存在，但没有解码成带分支的 cmp 4CC。 |
| `Ccsh` | `unresolved` | 是 | — | 反序字节存在，但没有解码成带分支的 cmp 4CC。 |
| `Ccsk` | `unresolved` | 是 | — | 反序字节存在，但没有解码成带分支的 cmp 4CC。 |
| `Ccsp` | `unresolved` | 是 | — | 反序字节存在，但没有解码成带分支的 cmp 4CC。 |
| `Ccsr` | `unresolved` | 是 | — | 反序字节存在，但没有解码成带分支的 cmp 4CC。 |
| `Ccsy` | `unresolved` | 是 | — | 反序字节存在，但没有解码成带分支的 cmp 4CC。 |
| `Cdbt` | `unresolved` | 是 | 0xe5815e je; 0xe5815f je; 0xe830af je; 0xe8c238 jne | 分支块未发现五类形态之一的直接访问 |
| `Cffp` | `unresolved` | 是 | 0xe5816b je; 0xe5816c je; 0xe840bf je; 0xe8cb62 jne | 分支块未发现五类形态之一的直接访问 |
| `Chrd` | `unresolved` | 是 | 0xe8b550 jne | 分支块未发现五类形态之一的直接访问 |
| `Clgl` | `unresolved` | 是 | 0xe840dc je; 0xe89f79 jne | 分支块未发现五类形态之一的直接访问 |
| `Cndi` | `unresolved` | 是 | 0xe82d8d jne; 0xe8ab0d jne | 分支块未发现五类形态之一的直接访问 |
| `Cnod` | `unresolved` | 是 | 0xe841bf jne | 分支块未发现五类形态之一的直接访问 |
| `Crdl` | `unresolved` | 是 | 0xe833a8 jne; 0xe8a201 jne | 分支块未发现五类形态之一的直接访问 |
| `Cren` | `unresolved` | 是 | 0xe8c37d jne; 0x11cfa8d je; 0x11f47d7 je; 0x11f47d8 je | 分支块未发现五类形态之一的直接访问 |
| `Crvc` | `unresolved` | 是 | 0xe82b64 jne; 0xe8c59e je | 分支块未发现五类形态之一的直接访问 |
| `Csoc` | `unresolved` | 是 | 0xe5835f je; 0xe58360 je; 0xe8340f je; 0xe8b1c0 je | 分支块未发现五类形态之一的直接访问 |
| `Cspb` | `unresolved` | 是 | 0xe5836c jne; 0xe5836d jne | 分支块未发现五类形态之一的直接访问 |
| `CssE` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CssP` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CssS` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `CssT` | `unresolved` | 是 | — | 反序字节存在，但没有解码成带分支的 cmp 4CC。 |
| `Cstc` | `unresolved` | 是 | — | 反序字节存在，但没有解码成带分支的 cmp 4CC。 |
| `Csth` | `unresolved` | 是 | 0xe581b7 je; 0xe581b8 je | 分支块未发现五类形态之一的直接访问 |
| `Csti` | `unresolved` | 是 | — | 反序字节存在，但没有解码成带分支的 cmp 4CC。 |
| `Ctsi` | `unresolved` | 是 | 0xe84400 jne; 0xe8c57d jne | 分支块未发现五类形态之一的直接访问 |
| `Cuf1` | `unresolved` | 是 | — | 反序字节存在，但没有解码成带分支的 cmp 4CC。 |
| `Cuf2` | `unresolved` | 是 | — | 反序字节存在，但没有解码成带分支的 cmp 4CC。 |
| `Cuf3` | `unresolved` | 是 | — | 反序字节存在，但没有解码成带分支的 cmp 4CC。 |
| `Cuf4` | `unresolved` | 是 | — | 反序字节存在，但没有解码成带分支的 cmp 4CC。 |
| `Cuf5` | `unresolved` | 是 | — | 反序字节存在，但没有解码成带分支的 cmp 4CC。 |
| `Cuf6` | `unresolved` | 是 | — | 反序字节存在，但没有解码成带分支的 cmp 4CC。 |
| `Cuf7` | `unresolved` | 是 | — | 反序字节存在，但没有解码成带分支的 cmp 4CC。 |
| `Cuf8` | `unresolved` | 是 | — | 反序字节存在，但没有解码成带分支的 cmp 4CC。 |
| `Cuf9` | `unresolved` | 是 | — | 反序字节存在，但没有解码成带分支的 cmp 4CC。 |
| `Cvfl` | `unresolved` | 是 | 0xe8c1e8 jne | 分支块未发现五类形态之一的直接访问 |
| `Melf` | `unresolved` | 是 | 0xeb00dc je; 0xeb0585 je; 0xeb060c je; 0x4381577 je | 分支块未发现五类形态之一的直接访问 |
| `Msid` | `unresolved` | 是 | 0xeb00e3 jne; 0xeb058c jne; 0xeb0613 jne; 0x438157f jne | 分支块未发现五类形态之一的直接访问 |
| `PUnI` | `unresolved` | 是 | — | 反序字节存在，但没有解码成带分支的 cmp 4CC。 |
| `PUnJ` | `unresolved` | 是 | — | 反序字节存在，但没有解码成带分支的 cmp 4CC。 |
| `PUnP` | `unresolved` | 是 | — | 反序字节存在，但没有解码成带分支的 cmp 4CC。 |
| `PUnT` | `unresolved` | 是 | — | 反序字节存在，但没有解码成带分支的 cmp 4CC。 |
| `RJ00` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ01` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ02` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ03` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ04` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ05` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ06` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ07` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ08` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ09` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ10` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ11` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ12` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ13` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ14` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ15` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ16` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ17` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ18` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ19` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ20` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ21` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ22` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ23` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ24` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ25` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ26` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ27` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ28` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ29` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ30` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ31` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ32` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ33` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ34` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ35` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ36` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ37` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ38` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ39` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ40` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ41` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ42` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ43` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ44` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ45` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ46` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ47` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ48` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RJ64` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP00` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP01` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP02` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP03` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP04` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP05` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP06` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP07` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP08` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP09` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP10` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP11` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP12` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP13` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP14` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP15` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP16` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP17` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP18` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP19` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP20` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP21` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP22` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP23` | `unresolved` | 是 | — | 反序字节存在，但没有解码成带分支的 cmp 4CC。 |
| `RP24` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP25` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP26` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP27` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP28` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP29` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP30` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP31` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP32` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP33` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP34` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP35` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP36` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP37` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP38` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP39` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP40` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP41` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP42` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP43` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP44` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP45` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP46` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP47` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP48` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `RP64` | `absent` | 否 | — | 全 exe 未找到该 4CC 的反序四字节序列。 |
| `TCrs` | `unresolved` | 是 | 0x11cfa56 jne; 0x11f15ab je; 0x11f4e37 je; 0x11f4e38 je | 分支块未发现五类形态之一的直接访问 |
| `Tcap` | `unresolved` | 是 | 0x11b03bc je; 0x11b4f1e je; 0x11f153c jne; 0x11f4db2 je; 0x11f4db3 je | 分支块未发现五类形态之一的直接访问 |
| `Tkg1` | `unresolved` | 是 | 0x11cf9ce je; 0x11f0706 je | 分支块未发现五类形态之一的直接访问 |
| `Tkg2` | `unresolved` | 是 | 0x11cf9da je; 0x11f06c4 jle; 0x11f0712 jne | 分支块未发现五类形态之一的直接访问 |
| `Tkg3` | `unresolved` | 是 | 0x11cf9e6 jne; 0x11f06d4 je | 分支块未发现五类形态之一的直接访问 |
| `Tko1` | `unresolved` | 是 | 0x11cface jne; 0x11f06cc jg; 0x11f06e0 jne | 分支块未发现五类形态之一的直接访问 |
| `Tko2` | `unresolved` | 是 | 0x11cfac2 je; 0x11f0730 je | 分支块未发现五类形态之一的直接访问 |
| `Tko3` | `unresolved` | 是 | 0x11cfab6 je; 0x11f073c jne | 分支块未发现五类形态之一的直接访问 |
| `Tvcp` | `unresolved` | 是 | 0x11b03fa je; 0x11b4e60 je; 0x11f1141 je; 0x11f4dcc jne; 0x11f4dcd jne | 分支块未发现五类形态之一的直接访问 |
| `allr` | `unresolved` | 是 | 0x153f525 je; 0x153fea9 je | 分支块未发现五类形态之一的直接访问 |
| `alls` | `unresolved` | 是 | 0x153f531 je; 0x153feb5 je; 0x28b7fad jne | 分支块未发现五类形态之一的直接访问 |
| `clfr` | `unresolved` | 是 | 0x43656ca jne | 分支块未发现五类形态之一的直接访问 |
| `cmid` | `unresolved` | 是 | 0x11f89b9 je; 0x11fd28a je; 0x11fd28b je; 0x3ec3d09 je; 0x3ec4617 je | 分支块未发现五类形态之一的直接访问 |
| `dAPw` | `unresolved` | 是 | 0xfe3751 je | 分支块未发现五类形态之一的直接访问 |
| `dral` | `unresolved` | 是 | 0x153f642 je; 0x153ff9d je | 分支块未发现五类形态之一的直接访问 |
| `edal` | `unresolved` | 是 | 0x153f64e je; 0x153ffa9 je | 分支块未发现五类形态之一的直接访问 |
| `exis` | `unresolved` | 是 | 0x153f65a jne; 0x153ffb5 jne; 0x15e669a jne; 0x44d2b44 je | 分支块未发现五类形态之一的直接访问 |
| `fri%` | `unresolved` | 是 | — | 反序字节存在，但没有解码成带分支的 cmp 4CC。 |
| `insl` | `unresolved` | 是 | 0x153f5f0 je; 0x153ff4b je | 分支块未发现五类形态之一的直接访问 |
| `ipRP` | `unresolved` | 是 | 0xfe3a38 je; 0xfe3d8c je; 0xfe3d9d je | 分支块未发现五类形态之一的直接访问 |
| `ipRS` | `unresolved` | 是 | 0xfe3946 je; 0xfe3da5 jne; 0xfe3e3a je | 分支块未发现五类形态之一的直接访问 |
| `ismc` | `unresolved` | 是 | 0x15264e5 je; 0x1527a5a je | 分支块未发现五类形态之一的直接访问 |
| `lpRP` | `unresolved` | 是 | 0xfe3952 je; 0xfe3adf je; 0xfe3e42 je | 分支块未发现五类形态之一的直接访问 |
| `lpRS` | `unresolved` | 是 | 0xfe3aeb je; 0xfe3b39 je; 0xfe3bab je | 分支块未发现五类形态之一的直接访问 |
| `ottm` | `unresolved` | 是 | 0x100be9b je; 0x10229d4 jne; 0x153f5fc je; 0x153ff57 je | 分支块未发现五类形态之一的直接访问 |
| `pcpt` | `unresolved` | 是 | 0xe583ab je; 0xe583ac je; 0xe8306e je; 0xe8b2d8 jne | 分支块未发现五类形态之一的直接访问 |
| `per2` | `unresolved` | 是 | 0xeac617 je; 0xeacbae je; 0xeacc55 je; 0x1524af8 je | 分支块未发现五类形态之一的直接访问 |
| `pers` | `unresolved` | 是 | 0x1077332 jne; 0x1077dd8 jne; 0x1106dbf jne; 0x3da2c8d jne; 0x3da2c8e jne; 0x3e1c955 jne | 分支块未发现五类形态之一的直接访问 |
| `plar` | `unresolved` | 是 | 0x153f608 jne; 0x153ff63 jne | 分支块未发现五类形态之一的直接访问 |
| `plde` | `unresolved` | 是 | 0x153f697 je; 0x153fff2 je | 分支块未发现五类形态之一的直接访问 |
| `plrl` | `unresolved` | 是 | 0x153f6a3 je; 0x153fffe je | 分支块未发现五类形态之一的直接访问 |
| `plrr` | `unresolved` | 是 | 0x153f6af jne; 0x154000a jne | 分支块未发现五类形态之一的直接访问 |
| `rdui` | `unresolved` | 是 | 0xfe1eea je; 0xfe3862 jne | 分支块未发现五类形态之一的直接访问 |
| `rsnn` | `unresolved` | 是 | 0x11fdff3 je; 0x3ec4a07 je; 0x3ecadc8 je | 分支块未发现五类形态之一的直接访问 |
| `rsnp` | `unresolved` | 是 | 0x11fe001 jne; 0x3ec4a17 jne; 0x3ecadd6 jne | 分支块未发现五类形态之一的直接访问 |
| `rsnr` | `unresolved` | 是 | 0x11fdffa je; 0x3ec4a0f je; 0x3ecadcf je | 分支块未发现五类形态之一的直接访问 |
| `slsn` | `unresolved` | 是 | 0xeaf37d je; 0xeaf940 je; 0x3b0ea28 je | 分支块未发现五类形态之一的直接访问 |
| `stco` | `unresolved` | 是 | 0xeaf38b jne; 0xeaf94f jne; 0xeaf950 jne; 0x3b0ea36 jne | 分支块未发现五类形态之一的直接访问 |

## 平表命名与回归

- T08 链命名原始值：138/240（有 schema 违规/错归属，不作为验收基线）。
- T11 schema 约束基线：129/240；chain_unique 68 / ambiguous 11 / readpair 37 / ref_only 8 / ref_pair 3 / schema_fixed 2 / unresolved 111；schema-illegal=0。
- T12 重跑：134/240；full_shape_unique 新增 5 个具体槽；schema-illegal=0；t07 45/45 保留。
- t12 命名摘要：{'slots': 240, 'named_slots': 134, 'confidence': {'chain_ambiguous': 11, 'chain_unique': 68, 'full_shape_unique': 5, 'readpair': 37, 'ref_only': 8, 'ref_pair': 3, 'schema_fixed': 2, 'unresolved': 106}, 'rejected_codes': 18, 'emptied_slots': 14, 'rescued_slots': 2, 'ref_ptr_added': 3}。
- 小表归属按稀有码 `1/df` 投票，并对 11 个零命名实体强制约束 schema 非通用字段数 ∈ [槽数, 3×槽数]。未满足门限者留空，不靠放宽阈值补名。
- `Sold/Snew/Salt` 分别命名为 object_off 32/40/72；injury 13/13、city 6/6；t07 命名 45/45；schema-illegal=0。

## 独立反汇编核验

- verify.py 对每条实例在 access_va 处重新 Capstone 解码，instruction 逐字匹配；file_off 处 cmp immediate 反序解码与 code 匹配。
- JE/JZ 只走目标，JNE/JNZ 只走 fall-through；jle/jl/jg/jae/ja/jb/jbe 均不挂访问。ScYK 两处 jle 陷阱均通过，后续 ScYL 独立命中。
- 验收结果：club 覆盖为唯一硬失败；逐码缺口如上，不把候选写成结论。
