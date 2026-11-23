__int64 __fastcall sub_143D0EDF0(__int64 a1, int a2, __int64 a3, unsigned int a4)
{
  unsigned int v4; // esi
  void (__fastcall ***v9)(_QWORD, __int64); // rcx
  void (__fastcall ***v10)(_QWORD, __int64); // rcx
  __int64 v11; // rcx
  char v13; // [rsp+38h] [rbp-60h]
  __int64 v14; // [rsp+40h] [rbp-58h] BYREF
  __int64 v15; // [rsp+48h] [rbp-50h] BYREF
  __int64 v16; // [rsp+50h] [rbp-48h] BYREF
  _BYTE v17[64]; // [rsp+58h] [rbp-40h] BYREF

  v16 = 0;
  if ( (*(_BYTE *)(a1 + 92) & 2) != 0 )
  {
    *(_BYTE *)(a1 + 89) = 1;
    LOBYTE(v4) = 1;
  }
  else
  {
    sub_14080D0E0(a1: v17, a2: 0x1418E2C24LL);
    v4 = 0;
    sub_140FFADB0(a1, a2: &v16, a3: 0, a4: 0);
    v13 = 0;
    sub_1407D0F70(
      a1: (unsigned int)&v14,
      a2: (unsigned int)&v15,
      a3: a2,
      a4: (unsigned int)&v16,
      a5: (__int64)v17,
      a6: 0,
      a7: 0,
      v13,
      0x80100004E554C4CLL);
    if ( v15 != 0 )
    {
      v14 = v15;
      _InterlockedIncrement((volatile signed __int32 *)(v15 + 8));
      v4 = sub_140F2E6D0(a1, a2: &v14, a3, a4);
      v9 = (void (__fastcall ***)(_QWORD, __int64))v14;
      if ( v14 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v14 + 8)) == 0 )
        (**v9)(a1: v9, a2: 1);
      v10 = (void (__fastcall ***)(_QWORD, __int64))v15;
      if ( v15 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v15 + 8)) == 0 )
        (**v10)(a1: v10, a2: 1);
    }
    v11 = v16;
    if ( v16 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v16 - 4)) == 0 )
      sub_1412EC9A0(a1: v11 - 4);
  }
  return v4;
}
