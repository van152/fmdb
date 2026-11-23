__int64 __fastcall sub_143D00E30(__int64 a1, int a2, unsigned int a3)
{
  __int64 v6; // rax
  __int64 v7; // rdi
  __int64 v8; // rcx
  __int64 v9; // rax
  __int64 v10; // rsi
  void (__fastcall ***v11)(_QWORD, __int64); // rcx
  void (__fastcall ***v12)(_QWORD, __int64); // rcx
  unsigned int v13; // esi
  __int64 v14; // rdi
  void (__fastcall ***v15)(_QWORD, __int64); // rcx
  __int64 v17; // [rsp+40h] [rbp-48h] BYREF
  __int64 v18; // [rsp+48h] [rbp-40h] BYREF
  __int64 v19; // [rsp+50h] [rbp-38h] BYREF
  __int64 v20; // [rsp+58h] [rbp-30h] BYREF

  v6 = *(_QWORD *)(a1 + 1160);
  if ( v6 != *(_QWORD *)(a1 + 1168) )
    *(_QWORD *)(a1 + 1168) = v6;
  v20 = 0x80100004E554C4CLL;
  sub_14080D0E0(a1: &v17, a2: 0x1418E2C24LL);
  v7 = sub_1412EC810(a1: 264, a2: 13);
  *(_QWORD *)v7 = 0xD00000000LL;
  strcpy((char *)(v7 + 8), "pl_hist_index");
  _InterlockedIncrement((volatile signed __int32 *)v7);
  v18 = 0;
  _InterlockedIncrement((volatile signed __int32 *)v7);
  v18 = v7 + 4;
  sub_1407D0F70(
    a1: (unsigned int)&v20,
    a2: (unsigned int)&v19,
    a3: a2,
    a4: (unsigned int)&v18,
    a5: (__int64)&v17,
    a6: 0,
    a7: 0,
    0);
  v8 = v18;
  if ( v18 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v18 - 4)) == 0 )
    sub_1412EC9A0(a1: v8 - 4);
  if ( _InterlockedDecrement((volatile signed __int32 *)v7) == 0 )
    sub_1412EC9A0(a1: v7);
  v9 = v19;
  if ( v19 == 0 )
    return 0;
  v10 = a1 + 1160;
  if ( WORD2(v20) <= 0xDC6u )
  {
    v17 = v19;
LABEL_22:
    _InterlockedIncrement((volatile signed __int32 *)(v9 + 8));
    v14 = v17;
    v13 = sub_140F3AF50(a1: &v17, a2: v10, a3, a4: 0);
    if ( v14 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v14 + 8)) == 0 )
      (**(void (__fastcall ***)(__int64, __int64))v14)(a1: v14, a2: 1);
    goto LABEL_25;
  }
  v18 = v19;
  _InterlockedIncrement((volatile signed __int32 *)(v19 + 8));
  sub_1407CC0B0(a1: &v17, a2: &v18);
  v11 = (void (__fastcall ***)(_QWORD, __int64))v19;
  if ( v19 == v17 )
  {
    if ( v19 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v19 + 8)) == 0 )
      (**v11)(a1: v11, a2: 1);
  }
  else
  {
    if ( v19 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v19 + 8)) == 0 )
      (**v11)(a1: v11, a2: 1);
    v19 = v17;
    v17 = 0;
  }
  v12 = (void (__fastcall ***)(_QWORD, __int64))v18;
  if ( v18 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v18 + 8)) == 0 )
    (**v12)(a1: v12, a2: 1);
  v9 = v19;
  v17 = v19;
  if ( v19 != 0 )
    goto LABEL_22;
  v13 = sub_140F3AF50(a1: &v17, a2: v10, a3, a4: 0);
LABEL_25:
  v15 = (void (__fastcall ***)(_QWORD, __int64))v19;
  if ( v19 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v19 + 8)) == 0 )
    (**v15)(a1: v15, a2: 1);
  return v13;
}
