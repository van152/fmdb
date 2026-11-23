__int64 __fastcall sub_143F5D2C0(__int64 a1, int a2)
{
  __int64 v4; // rbx
  __int64 v5; // rcx
  __int64 v6; // rbx
  __int64 v7; // rax
  volatile signed __int32 *v8; // rcx
  __int64 v9; // rcx
  __int64 v10; // rcx
  __int64 v11; // r8
  unsigned int v12; // esi
  void (__fastcall ***v13)(_QWORD, __int64); // rcx
  void (__fastcall ***v14)(_QWORD, __int64); // rcx
  __int64 v15; // rcx
  char v17; // [rsp+47h] [rbp-51h] BYREF
  __int64 v18; // [rsp+48h] [rbp-50h] BYREF
  __int64 v19; // [rsp+50h] [rbp-48h] BYREF
  __int64 v20; // [rsp+58h] [rbp-40h] BYREF
  __int64 v21; // [rsp+60h] [rbp-38h] BYREF
  _BYTE v22[48]; // [rsp+68h] [rbp-30h] BYREF

  v19 = 0;
  sub_14080D0E0(a1: v22, a2: 0x1418E2C24LL);
  v17 = *(_BYTE *)(a1 + 32);
  sub_140808120(a1: &v21, a2: &v17);
  v20 = 0;
  v4 = sub_1412EC810(a1: 264, a2: 11);
  *(_QWORD *)v4 = 0xB00000000LL;
  strcpy((char *)(v4 + 8), "name_table_");
  if ( v20 != 0 )
  {
    v5 = v20 - 4;
    if ( _InterlockedDecrement((volatile signed __int32 *)(v20 - 4)) == 0 )
      sub_1412EC9A0(a1: v5);
  }
  v20 = 0;
  _InterlockedIncrement((volatile signed __int32 *)v4);
  v20 = v4 + 4;
  sub_140809550(a1: &v20, a2: &v18, a3: &v21);
  v6 = v18;
  if ( v18 != 0 )
  {
    _InterlockedIncrement((volatile signed __int32 *)(v18 - 4));
    v7 = v19;
    if ( v19 == v6 )
    {
      if ( _InterlockedDecrement((volatile signed __int32 *)(v6 - 4)) == 0 )
        sub_1412EC9A0(a1: v6 - 4);
LABEL_13:
      v6 = v18;
      goto LABEL_14;
    }
LABEL_9:
    v8 = (volatile signed __int32 *)(v7 - 4);
    if ( v7 != 0 && _InterlockedDecrement(v8) == 0 )
      sub_1412EC9A0(a1: v8);
    v19 = v6;
    goto LABEL_13;
  }
  v7 = v19;
  if ( v19 != 0 )
    goto LABEL_9;
LABEL_14:
  if ( v6 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v6 - 4)) == 0 )
    sub_1412EC9A0(a1: v6 - 4);
  v9 = v20;
  if ( v20 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v20 - 4)) == 0 )
    sub_1412EC9A0(a1: v9 - 4);
  v10 = v21;
  if ( v21 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v21 - 4)) == 0 )
    sub_1412EC9A0(a1: v10 - 4);
  v18 = 0x80100004E554C4CLL;
  sub_1407D0F70(
    a1: (unsigned int)&v18,
    a2: (unsigned int)&v21,
    a3: a2,
    a4: (unsigned int)&v19,
    a5: (__int64)v22,
    a6: 0,
    a7: 0,
    0);
  if ( v21 != 0 )
  {
    v18 = v21;
    _InterlockedIncrement((volatile signed __int32 *)(v21 + 8));
    LOBYTE(v11) = 1;
    v12 = sub_1410BA080(a1, a2: &v18, a3: v11);
    v13 = (void (__fastcall ***)(_QWORD, __int64))v18;
    if ( v18 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v18 + 8)) == 0 )
      (**v13)(a1: v13, a2: 1);
    v14 = (void (__fastcall ***)(_QWORD, __int64))v21;
    if ( v21 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v21 + 8)) == 0 )
      (**v14)(a1: v14, a2: 1);
  }
  else
  {
    v12 = 0;
  }
  v15 = v19;
  if ( v19 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v19 - 4)) == 0 )
    sub_1412EC9A0(a1: v15 - 4);
  return v12;
}
