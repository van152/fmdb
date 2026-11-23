__int64 __fastcall sub_1438ACFE0(__int64 a1, __int64 *a2, __int64 *a3)
{
  __int64 v5; // rax
  int v6; // eax
  __int64 v7; // rbx
  __int64 v8; // rcx
  __int64 v9; // rcx
  __int64 v10; // rbx
  __int64 v11; // rax
  volatile signed __int32 *v12; // rcx
  __int64 result; // rax
  __int64 v14; // rcx
  __int64 v15; // [rsp+28h] [rbp-40h] BYREF
  __int64 v16; // [rsp+30h] [rbp-38h] BYREF
  int v17; // [rsp+3Ch] [rbp-2Ch] BYREF
  __int64 v18[5]; // [rsp+40h] [rbp-28h] BYREF

  v5 = *(_QWORD *)(a1 + 288);
  if ( v5 != 0 )
    v6 = *(_DWORD *)(v5 + 12);
  else
    v6 = -1;
  v17 = v6;
  sub_1408085A0(a1: &v16, a2: &v17);
  v15 = 0;
  v7 = sub_1412EC810(a1: 264, a2: 5);
  *(_QWORD *)v7 = 0x500000000LL;
  *(_BYTE *)(v7 + 12) = MEMORY[0x1419241FE];
  *(_DWORD *)(v7 + 8) = MEMORY[0x1419241FA];
  *(_BYTE *)(v7 + 13) = 0;
  if ( v15 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v15 - 4)) == 0 )
    sub_1412EC9A0(a1: v15 - 4);
  v15 = 0;
  _InterlockedIncrement((volatile signed __int32 *)v7);
  v15 = v7 + 4;
  sub_140809550(a1: &v15, a2: v18, a3: &v16);
  v8 = v15;
  if ( v15 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v15 - 4)) == 0 )
    sub_1412EC9A0(a1: v8 - 4);
  v9 = v16;
  if ( v16 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v16 - 4)) == 0 )
    sub_1412EC9A0(a1: v9 - 4);
  v10 = v18[0];
  if ( v18[0] != 0 )
  {
    _InterlockedIncrement((volatile signed __int32 *)(v18[0] - 4));
    v11 = *a2;
    if ( *a2 == v10 )
    {
      if ( _InterlockedDecrement((volatile signed __int32 *)(v10 - 4)) == 0 )
        sub_1412EC9A0(a1: v10 - 4);
      goto LABEL_22;
    }
  }
  else
  {
    v11 = *a2;
    if ( *a2 == 0 )
      goto LABEL_22;
  }
  v12 = (volatile signed __int32 *)(v11 - 4);
  if ( v11 != 0 && _InterlockedDecrement(v12) == 0 )
    sub_1412EC9A0(a1: v12);
  *a2 = v10;
LABEL_22:
  sub_14080D0E0(a1: &v16, a2: 0x1418E2C24LL);
  result = v16;
  *a3 = v16;
  v14 = v18[0];
  if ( v18[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v18[0] - 4)) == 0 )
    return sub_1412EC9A0(a1: v14 - 4);
  return result;
}
