__int64 __fastcall sub_143ABECA0(__int64 a1, _QWORD *a2)
{
  __int64 v4; // rbx
  int v5; // r9d
  void (__fastcall ***v6)(_QWORD, __int64); // rcx
  __int64 v7; // rcx
  void (__fastcall ***v8)(_QWORD, __int64); // rcx
  unsigned int v9; // esi
  void (__fastcall ***v10)(_QWORD, __int64); // rcx
  __int64 v12; // [rsp+28h] [rbp-28h] BYREF
  char v13[8]; // [rsp+30h] [rbp-20h] BYREF
  __int64 v14; // [rsp+38h] [rbp-18h] BYREF
  __int64 v15; // [rsp+40h] [rbp-10h] BYREF
  _QWORD v16[5]; // [rsp+48h] [rbp-8h] BYREF

  v16[1] = -2;
  sub_14080D0E0(a1: v13, a2: 0x1418E2C24LL);
  v4 = sub_1412EC810(a1: 264, a2: 14);
  *(_QWORD *)v4 = 0xE00000000LL;
  strcpy((char *)(v4 + 8), "national_teams");
  _InterlockedIncrement((volatile signed __int32 *)v4);
  v14 = 0;
  _InterlockedIncrement((volatile signed __int32 *)v4);
  v14 = v4 + 4;
  v12 = 0x80100004E554C4CLL;
  if ( *a2 != 0
    && ((*(void (__fastcall **)(_QWORD, __int64 *, __int64 *, char *))(*(_QWORD *)*a2 + 224LL))(
          a1: *a2,
          a2: &v15,
          a3: &v14,
          a4: v13),
        v15 != 0) )
  {
    LOWORD(v5) = 6;
    sub_1407D1280(a1: (unsigned int)&v12, a2: (unsigned int)v16, a3: (unsigned int)&v15, a4: v5, a5: 0);
    v6 = (void (__fastcall ***)(_QWORD, __int64))v15;
    if ( v15 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v15 + 8)) == 0 )
      (**v6)(a1: v6, a2: 1);
  }
  else
  {
    v16[0] = 0;
  }
  v7 = v14;
  if ( v14 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v14 - 4)) == 0 )
    sub_1412EC9A0(a1: v7 - 4);
  if ( _InterlockedDecrement((volatile signed __int32 *)v4) == 0 )
    sub_1412EC9A0(a1: v4);
  if ( v16[0] != 0 )
  {
    if ( (*(unsigned __int8 (__fastcall **)(__int64, _QWORD *))(*(_QWORD *)a1 + 160LL))(a1, a2: v16) != 0 )
    {
      v8 = (void (__fastcall ***)(_QWORD, __int64))v16[0];
      if ( v16[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v16[0] + 8LL)) == 0 )
        (**v8)(a1: v8, a2: 1);
      v16[0] = 0;
      v9 = sub_1413B3AE0(a1: a1 + 8, a2);
    }
    else
    {
      v9 = 0;
    }
    v10 = (void (__fastcall ***)(_QWORD, __int64))v16[0];
    if ( v16[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v16[0] + 8LL)) == 0 )
      (**v10)(a1: v10, a2: 1);
  }
  else
  {
    return 0;
  }
  return v9;
}
