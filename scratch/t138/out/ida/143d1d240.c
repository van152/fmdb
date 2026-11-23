__int64 __fastcall sub_143D1D240(__int64 a1, int a2, __int64 a3)
{
  unsigned int v3; // esi
  void (__fastcall ***v7)(_QWORD, __int64); // rcx
  void (__fastcall ***v8)(_QWORD, __int64); // rcx
  __int64 v9; // rcx
  char v11; // [rsp+38h] [rbp-60h]
  __int64 v12; // [rsp+48h] [rbp-50h] BYREF
  __int64 v13; // [rsp+50h] [rbp-48h] BYREF
  __int64 v14; // [rsp+58h] [rbp-40h] BYREF
  _BYTE v15[56]; // [rsp+60h] [rbp-38h] BYREF

  v14 = 0;
  if ( (*(_BYTE *)(a1 + 92) & 2) != 0 )
  {
    *(_BYTE *)(a1 + 89) = 1;
    LOBYTE(v3) = 1;
  }
  else
  {
    sub_14080D0E0(a1: v15, a2: 0x1418E2C24LL);
    v3 = 0;
    sub_140FFADB0(a1, a2: &v14, a3: 0, a4: 0);
    v12 = 0x80100004E554C4CLL;
    v11 = 0;
    sub_1407D0F70(
      a1: (unsigned int)&v12,
      a2: (unsigned int)&v13,
      a3: a2,
      a4: (unsigned int)&v14,
      a5: (__int64)v15,
      a6: 0,
      a7: 0,
      v11);
    if ( v13 != 0 )
    {
      v12 = v13;
      _InterlockedIncrement((volatile signed __int32 *)(v13 + 8));
      v3 = sub_140F37650(a1, a2: &v12, a3);
      v7 = (void (__fastcall ***)(_QWORD, __int64))v12;
      if ( v12 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v12 + 8)) == 0 )
        (**v7)(a1: v7, a2: 1);
      v8 = (void (__fastcall ***)(_QWORD, __int64))v13;
      if ( v13 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v13 + 8)) == 0 )
        (**v8)(a1: v8, a2: 1);
    }
    v9 = v14;
    if ( v14 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v14 - 4)) == 0 )
      sub_1412EC9A0(a1: v9 - 4);
  }
  return v3;
}
