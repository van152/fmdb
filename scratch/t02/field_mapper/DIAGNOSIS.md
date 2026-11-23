# field_mapper 可行性诊断(指挥官 17:35 独立验证)

## 宽度指令机械识别:可行

用 capstone 扫 comp 真正读主体 `0xeb7000..0xeb7600`(注意:census 的 unwrapped `0x3b3f0d0` 只是中间环,需继续沿 e8/e9 跟进到读主体):

- `mov r8d, N` 宽度点:**28 个**
- `call qword ptr [rax+0x28]` 流传输:**28 个**
- **28:28 完美配对**,宽度序列:`[1×8, 4×7, 2×2, 4, 1, 2×3, 8×3, ...]`

这正是 t01f 人工解出的 COMP 18 字段结构。结论:**宽度累加机械化完全可行**,`mov r8d,N` + `call [rax+0x28]` 的配对是稳定的机器可识别模式。

## 三个真实难点(脚本必须处理)

1. **thunk 链**:census `reader.entry_file_offset` 有时不是读主体。comp 链 = `0xed0a40(e9 jmp) → 0x3b3f0d0(设arg8=0, e8 call) → 0xeb7000(读主体)`。脚本要沿 e9/e8 rel32 跟进,找有密集 `call [rax+0x28]` 的函数。
2. **互斥臂**:某些字段宽度是 4B/8B 二选一(t01k 的 W 选择器),两条 `mov r8d` 不能相加,要按分支分别记。
3. **helper 内宽度**:宽度指令可能在被调用的 helper 里(weat 季节 helper、nation 集合 helper),需跟进一层 callee。

## 夹具复现目标

`fixtures.json` 7 实体/173 字段,覆盖 5 模式。验收:≥5/7 实体复现 ≥80% 偏移。直线型(comp/stad/pers)应近乎全复现;计数循环(nati)与 mixed(club)允许部分。

## 判断

"通用映射结构"不难——方法(E20)已验证,机械识别已证明。唯一门槛是把人工步骤写成脚本,这是本任务的内容。
