__int64 __fastcall sub_140FE7D20(__int64 *a1, __int64 *a2)
{
  __int64 v3; // rdi
  __int64 result; // rax
  _BYTE v5[32]; // [rsp+28h] [rbp-20h] BYREF

  v3 = qword_141B5FDD0;
  sub_140FE7960((__int64)v5, a2, 0x4E6E6174u);
  result = sub_14002F670(v3, v5);
  *a1 = result;
  return result;
}
