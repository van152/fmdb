__int64 __fastcall sub_143D0E270(int a1, int a2, int a3, int a4)
{
  __int64 v8; // rsi
  __int64 v9; // rcx
  unsigned int v10; // esi
  void (__fastcall ***v11)(_QWORD, __int64); // rcx
  void (__fastcall ***v12)(_QWORD, __int64); // rcx
  __int64 v14; // [rsp+48h] [rbp-50h] BYREF
  __int64 v15; // [rsp+50h] [rbp-48h] BYREF
  __int64 v16; // [rsp+58h] [rbp-40h] BYREF
  _BYTE v17[56]; // [rsp+60h] [rbp-38h] BYREF

  sub_14080D0E0(a1: v17, a2: 0x1418E2C24LL);
  v8 = sub_1412EC810(a1: 264, a2: 11);
  *(_QWORD *)v8 = 0xB00000000LL;
  strcpy((char *)(v8 + 8), "simple_vars");
  _InterlockedIncrement((volatile signed __int32 *)v8);
  v15 = 0;
  _InterlockedIncrement((volatile signed __int32 *)v8);
  v15 = v8 + 4;
  v14 = 0x80100004E554C4CLL;
  sub_1407D0F70(
    a1: (unsigned int)&v14,
    a2: (unsigned int)&v16,
    a3: a2,
    a4: (unsigned int)&v15,
    a5: (__int64)v17,
    a6: 0,
    a7: 0,
    0);
  v9 = v15;
  if ( v15 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v15 - 4)) == 0 )
    sub_1412EC9A0(a1: v9 - 4);
  if ( _InterlockedDecrement((volatile signed __int32 *)v8) == 0 )
    sub_1412EC9A0(a1: v8);
  if ( v16 != 0 )
  {
    v14 = v16;
    _InterlockedIncrement((volatile signed __int32 *)(v16 + 8));
    v10 = sub_140F2B240(a1, a2: (unsigned int)&v14, a3, a4, a5: 1);
    v11 = (void (__fastcall ***)(_QWORD, __int64))v14;
    if ( v14 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v14 + 8)) == 0 )
      (**v11)(a1: v11, a2: 1);
    v12 = (void (__fastcall ***)(_QWORD, __int64))v16;
    if ( v16 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v16 + 8)) == 0 )
      (**v12)(a1: v12, a2: 1);
  }
  else
  {
    return 0;
  }
  return v10;
}
