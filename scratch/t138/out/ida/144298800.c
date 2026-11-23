__int64 __fastcall sub_144298800(__int64 a1, int a2)
{
  __int64 v4; // rdi
  __int64 v5; // rcx
  volatile signed __int32 *v6; // rdi
  int v7; // esi
  volatile signed __int32 *v8; // rsi
  volatile signed __int32 *v9; // rcx
  volatile signed __int32 *v11; // [rsp+48h] [rbp-40h] BYREF
  __int64 v12; // [rsp+50h] [rbp-38h] BYREF
  __int64 v13; // [rsp+58h] [rbp-30h] BYREF
  _BYTE v14[40]; // [rsp+60h] [rbp-28h] BYREF

  v13 = 0x80100004E554C4CLL;
  sub_14080D0E0(a1: v14, a2: 0x1418E2C24LL);
  v4 = sub_1412EC810(a1: 264, a2: 13);
  *(_QWORD *)v4 = 0xD00000000LL;
  strcpy((char *)(v4 + 8), "fifa_rankings");
  _InterlockedIncrement((volatile signed __int32 *)v4);
  v12 = 0;
  _InterlockedIncrement((volatile signed __int32 *)v4);
  v12 = v4 + 4;
  sub_1407D0F70(
    a1: (unsigned int)&v13,
    a2: (unsigned int)&v11,
    a3: a2,
    a4: (unsigned int)&v12,
    a5: (__int64)v14,
    a6: 0,
    a7: 0,
    0);
  v5 = v12;
  if ( v12 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v12 - 4)) == 0 )
    sub_1412EC9A0(a1: v5 - 4);
  if ( _InterlockedDecrement((volatile signed __int32 *)v4) == 0 )
    sub_1412EC9A0(a1: v4);
  v6 = v11;
  if ( v11 == nullptr )
  {
    LODWORD(v8) = 0;
    return (unsigned int)v8;
  }
  _InterlockedIncrement(v11 + 2);
  _InterlockedIncrement(v6 + 2);
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v6 + 40LL))(a1: v6, a2: a1, a3: 4);
  v7 = *((_DWORD *)v6 + 4);
  if ( _InterlockedDecrement(v6 + 2) != 0 )
  {
    if ( _InterlockedDecrement(v6 + 2) != 0 )
    {
LABEL_9:
      if ( v7 != 0 )
        goto LABEL_14;
      goto LABEL_13;
    }
  }
  else
  {
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v6)(a1: v6, a2: 1);
    if ( _InterlockedDecrement(v6 + 2) != 0 )
      goto LABEL_9;
  }
  (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v6)(a1: v6, a2: 1);
  if ( v7 == 0 )
  {
LABEL_13:
    v8 = v11;
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v11 + 40LL))(
      a1: v11,
      a2: a1 + 4,
      a3: 2);
    if ( *((_DWORD *)v8 + 4) == 0 )
    {
      if ( WORD2(v13) < 2u
        || (v8 = v11,
            (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v11 + 40LL))(
              a1: v11,
              a2: a1 + 6,
              a3: 2),
            *((_DWORD *)v8 + 4) == 0) )
      {
        LOBYTE(v8) = 1;
        goto LABEL_15;
      }
    }
  }
LABEL_14:
  LODWORD(v8) = 0;
LABEL_15:
  v9 = v11;
  if ( v11 != nullptr && _InterlockedDecrement(v11 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v9)(a1: v9, a2: 1);
  return (unsigned int)v8;
}
