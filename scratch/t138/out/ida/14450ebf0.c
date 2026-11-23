__int64 __fastcall sub_14450EBF0(__int64 a1, int a2)
{
  __int64 v4; // rdi
  __int64 v5; // rcx
  unsigned int v6; // esi
  void (__fastcall ***v7)(_QWORD, __int64); // rcx
  void (__fastcall ***v8)(_QWORD, __int64); // rcx
  __int64 v10; // [rsp+48h] [rbp-40h] BYREF
  __int64 v11; // [rsp+50h] [rbp-38h] BYREF
  __int64 v12; // [rsp+58h] [rbp-30h] BYREF
  _BYTE v13[40]; // [rsp+60h] [rbp-28h] BYREF

  sub_14080D0E0(a1: v13, a2: 0x1418E2C24LL);
  v4 = sub_1412EC810(a1: 264, a2: 26);
  *(_QWORD *)v4 = 0x1A00000000LL;
  strcpy((char *)(v4 + 8), "manager_player_preferences");
  _InterlockedIncrement((volatile signed __int32 *)v4);
  v11 = 0;
  _InterlockedIncrement((volatile signed __int32 *)v4);
  v11 = v4 + 4;
  v10 = 0x80100004E554C4CLL;
  sub_1407D0F70(
    a1: (unsigned int)&v10,
    a2: (unsigned int)&v12,
    a3: a2,
    a4: (unsigned int)&v11,
    a5: (__int64)v13,
    a6: 0,
    a7: 0,
    0);
  v5 = v11;
  if ( v11 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v11 - 4)) == 0 )
    sub_1412EC9A0(a1: v5 - 4);
  if ( _InterlockedDecrement((volatile signed __int32 *)v4) == 0 )
    sub_1412EC9A0(a1: v4);
  if ( v12 != 0 )
  {
    v10 = v12;
    _InterlockedIncrement((volatile signed __int32 *)(v12 + 8));
    v6 = sub_14156EDD0(a1, a2: &v10);
    v7 = (void (__fastcall ***)(_QWORD, __int64))v10;
    if ( v10 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v10 + 8)) == 0 )
      (**v7)(a1: v7, a2: 1);
    v8 = (void (__fastcall ***)(_QWORD, __int64))v12;
    if ( v12 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v12 + 8)) == 0 )
      (**v8)(a1: v8, a2: 1);
  }
  else
  {
    return 0;
  }
  return v6;
}
