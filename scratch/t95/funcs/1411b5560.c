// THUNK ALIAS -> sub_143FF5300 (jmp:0x1411b5560->0x143ff5300)
__int64 __fastcall sub_143FF5300(__int64 a1, __int64 *a2, char a3, int *a4)
{
  unsigned int v7; // r15d
  __int64 v8; // rcx
  __int64 v10[3]; // [rsp+68h] [rbp-50h] BYREF
  int v11[14]; // [rsp+80h] [rbp-38h] BYREF

  v7 = 0;
  sub_140FE7960((__int64)v11, a2, 0);
  sub_1407C9510(v10);
  LOBYTE(v8) = *(_BYTE *)(a1 + 47) == 0;
  if ( sub_141037A60(v8, v11, a4, a3, a3, v10) != 0 )
    v7 = sub_140F47AD0((__int64)&qword_141B5FDA8, v10, 1, 0, 1, 0, 1, nullptr, nullptr, 1, 0, 0);
  sub_140833970(v10);
  return v7;
}
