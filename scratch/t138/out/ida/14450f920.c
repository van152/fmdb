char __fastcall sub_14450F920(__int64 a1, int a2)
{
  __int64 v4; // rdi
  __int64 v5; // rcx
  __int64 v6; // rsi
  void (__fastcall ***v7)(_QWORD, __int64); // rcx
  void (__fastcall ***v8)(_QWORD, __int64); // rcx
  char v10; // [rsp+38h] [rbp-50h]
  __int64 v11; // [rsp+48h] [rbp-40h] BYREF
  __int64 v12; // [rsp+50h] [rbp-38h] BYREF
  __int64 v13; // [rsp+58h] [rbp-30h] BYREF
  _BYTE v14[40]; // [rsp+60h] [rbp-28h] BYREF

  sub_14080D0E0(a1: v14, a2: 0x1418E2C24LL);
  v4 = sub_1412EC810(a1: 264, a2: 15);
  *(_QWORD *)v4 = 0xF00000000LL;
  strcpy((char *)(v4 + 8), "non_player_bans");
  _InterlockedIncrement((volatile signed __int32 *)v4);
  v12 = 0;
  _InterlockedIncrement((volatile signed __int32 *)v4);
  v12 = v4 + 4;
  v11 = 0x80100004E554C4CLL;
  v10 = 0;
  sub_1407D0F70(
    a1: (unsigned int)&v11,
    a2: (unsigned int)&v13,
    a3: a2,
    a4: (unsigned int)&v12,
    a5: (__int64)v14,
    a6: 0,
    a7: 0,
    v10);
  v5 = v12;
  if ( v12 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v12 - 4)) == 0 )
    sub_1412EC9A0(a1: v5 - 4);
  if ( _InterlockedDecrement((volatile signed __int32 *)v4) == 0 )
    sub_1412EC9A0(a1: v4);
  v6 = v13;
  if ( v13 != 0 )
  {
    v11 = v13;
    _InterlockedIncrement((volatile signed __int32 *)(v13 + 8));
    LOBYTE(a2) = sub_14156F860(a1, a2: &v11);
    v7 = (void (__fastcall ***)(_QWORD, __int64))v11;
    if ( v11 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v11 + 8)) == 0 )
      (**v7)(a1: v7, a2: 1);
    v8 = (void (__fastcall ***)(_QWORD, __int64))v13;
    if ( v13 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v13 + 8)) == 0 )
      (**v8)(a1: v8, a2: 1);
  }
  return a2 & (v6 != 0);
}
