__int64 __fastcall sub_144298A10(__int64 a1, _QWORD *a2)
{
  __int64 v4; // rdi
  int v5; // r9d
  void (__fastcall ***v6)(_QWORD, __int64); // rcx
  __int64 v7; // rcx
  __int64 v8; // rdi
  __int64 v9; // rdi
  __int64 v10; // rdi
  __int64 v11; // rsi
  void (__fastcall ***v12)(_QWORD, __int64); // rcx
  __int64 v14; // rdi
  __int64 v15; // [rsp+28h] [rbp-28h] BYREF
  char v16[8]; // [rsp+30h] [rbp-20h] BYREF
  __int64 v17; // [rsp+38h] [rbp-18h] BYREF
  __int64 v18; // [rsp+40h] [rbp-10h] BYREF
  _QWORD v19[5]; // [rsp+48h] [rbp-8h] BYREF

  v19[1] = -2;
  sub_14080D0E0(a1: v16, a2: 0x1418E2C24LL);
  v4 = sub_1412EC810(a1: 264, a2: 13);
  *(_QWORD *)v4 = 0xD00000000LL;
  strcpy((char *)(v4 + 8), "fifa_rankings");
  _InterlockedIncrement((volatile signed __int32 *)v4);
  v17 = 0;
  _InterlockedIncrement((volatile signed __int32 *)v4);
  v17 = v4 + 4;
  v15 = 0x80100004E554C4CLL;
  if ( *a2 != 0
    && ((*(void (__fastcall **)(_QWORD, __int64 *, __int64 *, char *))(*(_QWORD *)*a2 + 224LL))(
          a1: *a2,
          a2: &v18,
          a3: &v17,
          a4: v16),
        v18 != 0) )
  {
    LOWORD(v5) = 2;
    sub_1407D1280(a1: (unsigned int)&v15, a2: (unsigned int)v19, a3: (unsigned int)&v18, a4: v5, a5: 0);
    v6 = (void (__fastcall ***)(_QWORD, __int64))v18;
    if ( v18 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v18 + 8)) == 0 )
      (**v6)(a1: v6, a2: 1);
  }
  else
  {
    v19[0] = 0;
  }
  v7 = v17;
  if ( v17 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v17 - 4)) == 0 )
    sub_1412EC9A0(a1: v7 - 4);
  if ( _InterlockedDecrement((volatile signed __int32 *)v4) == 0 )
    sub_1412EC9A0(a1: v4);
  v8 = v19[0];
  if ( v19[0] != 0 )
  {
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v19[0] + 40LL))(a1: v19[0], a2: a1, a3: 2);
    if ( *(_DWORD *)(v8 + 16) != 0
      || (v9 = v19[0],
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v19[0] + 40LL))(a1: v19[0], a2: a1 + 2, a3: 2),
          *(_DWORD *)(v9 + 16) != 0)
      || (v10 = v19[0],
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v19[0] + 40LL))(a1: v19[0], a2: a1 + 4, a3: 2),
          *(_DWORD *)(v10 + 16) != 0) )
    {
      LODWORD(v11) = 0;
    }
    else
    {
      v14 = v19[0];
      v11 = a1 + 6;
      (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)v19[0] + 40LL))(a1: v19[0], a2: v11, a3: 2);
      LOBYTE(v11) = *(_DWORD *)(v14 + 16) == 0;
    }
    v12 = (void (__fastcall ***)(_QWORD, __int64))v19[0];
    if ( v19[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v19[0] + 8LL)) == 0 )
      (**v12)(a1: v12, a2: 1);
  }
  else
  {
    LODWORD(v11) = 0;
  }
  return (unsigned int)v11;
}
