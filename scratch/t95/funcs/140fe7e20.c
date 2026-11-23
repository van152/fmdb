__int64 __fastcall sub_140FE7E20(__int64 *a1, __int64 *a2)
{
  __int64 v3; // rdi
  __int64 result; // rax
  int v5[8]; // [rsp+28h] [rbp-20h] BYREF

  v3 = qword_141B5FE40;
  sub_140FE7960((__int64)v5, a2, 0x54746561u);
  result = sub_140FA3700(v3, v5);
  *a1 = result;
  return result;
}
